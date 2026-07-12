# ruff: noqa: S101

import json
from datetime import timedelta
from unittest.mock import Mock
from urllib.parse import urlparse

import psycopg2
import pytest
import requests
from skyfield.api import EarthSatellite, load
from sqlalchemy import text
from tests.conftest import FIXTURES_DIR
from tle_utils import add_orbital_data_list_to_db

from api.adapters.repositories.orbital_elements_repository import (
    SqlAlchemyOrbitalElementsRepository,
)
from api.domain.models.tle import TLE

CELESTRAK_STARLINK_SUP_URL = (
    "https://celestrak.org/NORAD/elements/supplemental/sup-gp.php"
    "?FILE=starlink&FORMAT=json"
)


@pytest.fixture(scope="module")
def celestrak_starlink_supplemental_records():
    try:
        response = requests.get(CELESTRAK_STARLINK_SUP_URL, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        pytest.skip(f"Celestrak unavailable: {exc}")

    records = response.json()
    if not records:
        pytest.skip("Celestrak returned no Starlink supplemental records")

    return records[:2]


@pytest.fixture
def pg_connection(app):
    db_url = app.config["SQLALCHEMY_DATABASE_URI"]
    parsed = urlparse(db_url)
    connection = psycopg2.connect(
        dbname=parsed.path.lstrip("/"),
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port,
    )
    cursor = connection.cursor()
    try:
        yield connection, cursor
    finally:
        cursor.close()
        connection.close()


def _ingest_starlink_supplemental(connection, cursor, records):
    response = Mock()
    response.json.return_value = records
    add_orbital_data_list_to_db(
        response,
        "starlink",
        cursor,
        connection,
        "true",
        "celestrak",
        True,
    )


def test_celestrak_starlink_supplemental_omm_ingest(
    session,
    services_available,
    pg_connection,
    celestrak_starlink_supplemental_records,
):
    connection, cursor = pg_connection
    sample = celestrak_starlink_supplemental_records
    n = len(sample)

    _ingest_starlink_supplemental(connection, cursor, sample)
    session.expire_all()

    assert session.execute(text("SELECT COUNT(*) FROM satellites")).scalar() == n
    assert session.execute(text("SELECT COUNT(*) FROM orbital_elements")).scalar() == n
    assert session.execute(text("SELECT COUNT(*) FROM tle")).scalar() == 0

    first = sample[0]
    row = session.execute(
        text("""
            SELECT oe.mean_motion, s.sat_name, s.constellation, oe.data_source
            FROM orbital_elements oe
            JOIN satellites s ON s.id = oe.sat_id
            WHERE s.sat_number = :norad_id
            """),
        {"norad_id": int(first["NORAD_CAT_ID"])},
    ).one()

    assert row.sat_name == first["OBJECT_NAME"]
    assert row.constellation == "starlink"
    assert row.data_source == "celestrak"
    assert row.mean_motion == pytest.approx(float(first["MEAN_MOTION"]))

    _ingest_starlink_supplemental(connection, cursor, sample)
    session.expire_all()
    assert session.execute(text("SELECT COUNT(*) FROM orbital_elements")).scalar() == n
    assert session.execute(text("SELECT COUNT(*) FROM tle")).scalar() == 0


def _synthetic_omm_record(norad_id, **overrides):
    """A minimal, valid Celestrak/Space-Track-style OMM record."""
    record = {
        "OBJECT_NAME": f"TESTSAT-{norad_id}",
        "OBJECT_ID": "2024-001A",
        "EPOCH": "2024-10-01T18:19:13.000000",
        "MEAN_MOTION": 14.5,
        "ECCENTRICITY": 0.001,
        "INCLINATION": 53.0,
        "RA_OF_ASC_NODE": 10.0,
        "ARG_OF_PERICENTER": 20.0,
        "MEAN_ANOMALY": 30.0,
        "EPHEMERIS_TYPE": 0,
        "CLASSIFICATION_TYPE": "U",
        "NORAD_CAT_ID": norad_id,
        "ELEMENT_SET_NO": 1,
        "REV_AT_EPOCH": 1,
        "BSTAR": 0.0001,
        "MEAN_MOTION_DOT": 0.00001,
        "MEAN_MOTION_DDOT": 0.0,
    }
    record.update(overrides)
    return record


def test_celestrak_ingest_skips_bad_records_without_losing_good_ones(
    session, services_available, pg_connection
):
    """
    A single malformed record must not roll back the whole ingestion batch.
    """
    connection, cursor = pg_connection

    good_1 = _synthetic_omm_record(900001)
    missing_epoch = _synthetic_omm_record(900002, EPOCH=None)
    missing_bstar = _synthetic_omm_record(900003, BSTAR=None)
    good_2 = _synthetic_omm_record(900004)
    records = [good_1, missing_epoch, missing_bstar, good_2]

    response = Mock()
    response.json.return_value = records
    add_orbital_data_list_to_db(
        response,
        "test",
        cursor,
        connection,
        "false",
        "celestrak",
        True,
    )
    session.expire_all()

    assert session.execute(text("SELECT COUNT(*) FROM satellites")).scalar() == 2
    assert session.execute(text("SELECT COUNT(*) FROM orbital_elements")).scalar() == 2

    stored_norad_ids = {
        row[0]
        for row in session.execute(
            text("SELECT sat_number FROM satellites ORDER BY sat_number")
        )
    }
    assert stored_norad_ids == {900001, 900004}


def test_ingested_orbital_elements_match_equivalent_tle_propagation(
    session, services_available, pg_connection
):
    """
    End-to-end cross-check: ingest a Celestrak OMM record
    through the actual production path -- add_orbital_data_list_to_db ->
    Postgres -> SqlAlchemyOrbitalElementsRepository -> OrbitalElements ->
    to_earth_satellite() -- and confirm it propagates to the same sky
    position as Celestrak's own equivalent TLE for the same object and
    epoch, parsed directly.
    """
    connection, cursor = pg_connection

    omm_record = json.loads((FIXTURES_DIR / "iss_omm.json").read_text())[0]
    tle_lines = (FIXTURES_DIR / "iss_tle.txt").read_text().splitlines()
    tle_line1, tle_line2 = tle_lines[1], tle_lines[2]

    response = Mock()
    response.json.return_value = [omm_record]
    add_orbital_data_list_to_db(
        response,
        None,
        cursor,
        connection,
        "false",
        "celestrak",
        True,
    )
    session.expire_all()

    ts = load.timescale()
    tle_epoch = EarthSatellite(tle_line1, tle_line2, ts=ts).epoch.utc_datetime()

    orbital_elements_repo = SqlAlchemyOrbitalElementsRepository(session)
    ingested = orbital_elements_repo.get_nearest_orbital_elements(
        str(omm_record["NORAD_CAT_ID"]), "catalog", tle_epoch
    )
    assert ingested is not None

    tle = TLE(
        satellite=ingested.satellite,
        tle_line1=tle_line1,
        tle_line2=tle_line2,
        epoch=tle_epoch,
        date_collected=tle_epoch,
        data_source="celestrak",
        is_supplemental=False,
    )

    sat_from_db = ingested.to_earth_satellite(ts)
    sat_from_tle = tle.to_earth_satellite(ts)

    observation_time = tle_epoch + timedelta(hours=1)
    t = ts.from_datetime(observation_time)

    ra_db, dec_db, _ = sat_from_db.at(t).radec()
    ra_tle, dec_tle, _ = sat_from_tle.at(t).radec()

    assert ra_db._degrees == pytest.approx(ra_tle._degrees, abs=1e-3)
    assert dec_db._degrees == pytest.approx(dec_tle._degrees, abs=1e-3)
