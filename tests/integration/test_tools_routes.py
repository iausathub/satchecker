# ruff: noqa: E501, S101, F841
import io
import time
import zipfile
from datetime import datetime, timedelta, timezone

import pyarrow.parquet as pq
import pytest
from astropy.time import Time
from tests.factories.ephemeris_factory import InterpolableEphemerisFactory
from tests.factories.orbital_elements_factory import OrbitalElementsFactory
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.adapters.database_orm import SatelliteDb
from api.adapters.repositories import (
    ephemeris_repository,
    orbital_elements_repository,
    satellite_repository,
    tle_repository,
)
from api.entrypoints.extensions import db
from api.utils.output_utils import EPHEMERIS_PARQUET_COLUMNS

# A fixed epoch before ORBITAL_ELEMENTS_CUTOFF (2026-07-13) so these TLE-store
# tests stay deterministic; without it, `datetime.now()` has drifted past the
# cutoff and the endpoints correctly source from the (empty) OMM store instead.
PRE_CUTOFF_EPOCH = datetime(2026, 6, 1)


def test_get_tle_data(client, session, services_available):
    satellite = SatelliteFactory(sat_name="ISS")

    tle = TLEFactory(satellite=satellite)
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)

    session.commit()
    response = client.get("/tools/get-tle-data/?id=ISS&id_type=name")
    assert response.status_code == 200


def test_get_tle_data_no_match(client, services_available):
    response = client.get("/tools/get-tle-data/?id=ISS&id_type=name")

    assert response.status_code == 200
    assert response.json["count"] == 0


def test_get_names_from_norad_id(client, services_available):
    satellite = SatelliteFactory(sat_number="25544")
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/names-from-norad-id/?id=25544")
    assert response.status_code == 200
    assert response.json["count"] == 1
    # id is parsed to an integer NORAD ID by validate_parameters
    assert response.json["data"][0]["norad_id"] == 25544


def test_get_names_from_norad_id_no_match(client, services_available):
    response = client.get("/tools/names-from-norad-id/?id=25544")
    assert response.status_code == 200
    assert response.json["count"] == 0


def test_get_norad_ids_from_name(client, services_available):
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/norad-ids-from-name/?name=ISS")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["name"] == "ISS"


def test_get_norad_ids_from_name_no_match(client, services_available):
    response = client.get("/tools/norad-ids-from-name/?name=ISS")
    assert response.status_code == 200
    assert response.json["count"] == 0


def test_get_satellite_data(client, services_available):
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/get-satellite-data/?id=ISS&id_type=name")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"


def test_get_satellite_data_no_match(client, services_available):
    response = client.get("/tools/get-satellite-data/?id=ISS&id_type=name")
    assert response.status_code == 200
    assert response.json == []


def test_get_tles_at_epoch(client, session, services_available):
    satellite = SatelliteFactory(
        sat_name="ISS",
        decay_date=None,
        has_current_sat_number=True,
        launch_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
    )
    epoch_date = datetime.strptime("2024-10-21", "%Y-%m-%d")
    tle = TLEFactory(satellite=satellite, epoch=epoch_date)
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    epoch_date = 2460605
    response = client.get(f"/tools/tles-at-epoch/?epoch={epoch_date}")
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["data"][0]["satellite_name"] == "ISS"

    # test that older TLEs ( > 2 weeks ) are not returned
    epoch_date = 2460505
    response = client.get(f"/tools/tles-at-epoch/?epoch={epoch_date}")
    assert response.status_code == 200
    assert len(response.json[0]["data"]) == 0


def test_get_tles_at_epoch_pagination(client, session, services_available):
    satellite = SatelliteFactory(
        sat_name="ISS",
        decay_date=None,
        has_current_sat_number=True,
        launch_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
    )
    epoch_date = datetime.strptime("2024-10-22", "%Y-%m-%d")
    tle = TLEFactory(satellite=satellite, epoch=epoch_date)
    print(tle.epoch)
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()
    epoch_date = 2460606
    response = client.get(f"/tools/tles-at-epoch/?epoch={epoch_date}&page=1&per_page=1")
    tles = response.json[0]["data"]
    assert response.status_code == 200
    assert len(response.json) == 1
    assert tles[0]["satellite_name"] == "ISS"


def test_get_tles_at_epoch_optional_epoch_date(client, session, services_available):
    # With no epoch provided the endpoint defaults to "now", which is after the
    # orbital-elements cutoff, so the data comes from the OMM store and is
    # converted to TLE format transparently.
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    omm = OrbitalElementsFactory(
        satellite=satellite,
        epoch=datetime.now(),
        mean_motion=15.5,
        eccentricity=0.0001,
        inclination=51.6,
        ra_of_ascending_node=100.0,
        arg_of_pericenter=90.0,
        mean_anomaly=270.0,
        bstar=0.0001,
        mean_motion_dot=0.0,
        mean_motion_ddot=0.0,
    )
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    omm_repo.add(omm)
    session.commit()
    response = client.get("/tools/tles-at-epoch/")
    tles = response.json[0]["data"]
    assert response.status_code == 200
    assert len(response.json) > 0
    assert tles[0]["satellite_name"] == "ISS"
    assert "tle_line1" in tles[0]
    assert "tle_line2" in tles[0]


def test_get_tles_at_epoch_zipped(client, session, services_available):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    # Pre-cutoff epoch so the TLE store (not the OMM store) serves the request.
    epoch_date = PRE_CUTOFF_EPOCH
    tle = TLEFactory(
        satellite=satellite,
        epoch=epoch_date,
    )
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()
    epoch_jd = Time(epoch_date).jd
    response = client.get(f"/tools/tles-at-epoch/?epoch={epoch_jd}&format=zip")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/zip"
    assert (
        response.headers["Content-Disposition"] == "attachment; filename=tle_data.zip"
    )


# A fixed epoch for the ephemeris endpoint; the ephemeris window is built tz-aware
# around it below.
EPHEMERIS_EPOCH = datetime(2026, 7, 1)


def _add_covering_ephemeris(session, epoch_dt, sat_number=88888):
    """Persist a satellite and one ephemeris record whose window covers epoch_dt."""
    satellite = SatelliteFactory(
        sat_name="STARLINK-TEST",
        sat_number=sat_number,
        decay_date=None,
        has_current_sat_number=True,
        launch_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
    )
    db_satellite = SatelliteDb(
        sat_number=satellite.sat_number,
        sat_name=satellite.sat_name,
        constellation=satellite.constellation,
        generation=satellite.generation,
        rcs_size=satellite.rcs_size,
        launch_date=satellite.launch_date,
        decay_date=satellite.decay_date,
        object_id=satellite.object_id,
        object_type=satellite.object_type,
        has_current_sat_number=satellite.has_current_sat_number,
    )
    session.add(db_satellite)
    session.commit()

    ephemeris = InterpolableEphemerisFactory(
        satellite=satellite,
        generated_at=(epoch_dt - timedelta(minutes=30)).replace(tzinfo=timezone.utc),
        ephemeris_start=(epoch_dt - timedelta(hours=1)).replace(tzinfo=timezone.utc),
        ephemeris_stop=(epoch_dt + timedelta(hours=1)).replace(tzinfo=timezone.utc),
    )
    ephemeris_repository.SqlAlchemyEphemerisRepository(session).add(ephemeris)
    session.commit()
    return ephemeris


def test_get_ephemeris_data_at_epoch_parquet(client, session, services_available):
    ephemeris = _add_covering_ephemeris(session, EPHEMERIS_EPOCH)
    epoch_jd = Time(EPHEMERIS_EPOCH).jd

    # No ephemeris_format -> defaults to Parquet.
    response = client.get(f"/tools/ephemeris-data-at-epoch/?epoch={epoch_jd}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/vnd.apache.parquet"
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=ephemeris_data.parquet"
    )
    table = pq.read_table(io.BytesIO(response.data))
    assert table.schema.names == EPHEMERIS_PARQUET_COLUMNS
    assert table.num_rows == len(ephemeris.points)
    assert 88888 in table.column("satellite_id").to_pylist()


def test_get_ephemeris_data_at_epoch_zip(client, session, services_available):
    _add_covering_ephemeris(session, EPHEMERIS_EPOCH)
    epoch_jd = Time(EPHEMERIS_EPOCH).jd

    response = client.get(
        f"/tools/ephemeris-data-at-epoch/?epoch={epoch_jd}&ephemeris_format=zip"
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/zip"
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=ephemeris_data.zip"
    )
    with zipfile.ZipFile(io.BytesIO(response.data)) as zip_file:
        assert zip_file.namelist() == ["88888.csv"]


def test_get_ephemeris_data_at_epoch_invalid_format(client, services_available):
    response = client.get("/tools/ephemeris-data-at-epoch/?ephemeris_format=xml")
    assert response.status_code == 500


def test_get_omms_at_epoch(client, session, services_available):
    satellite = SatelliteFactory(
        sat_name="ISS",
        decay_date=None,
        has_current_sat_number=True,
        launch_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
    )
    epoch_date = datetime.strptime("2024-10-21", "%Y-%m-%d")
    omm = OrbitalElementsFactory(satellite=satellite, epoch=epoch_date)
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    omm_repo.add(omm)
    session.commit()

    epoch_date = 2460605
    response = client.get(f"/tools/omms-at-epoch/?epoch={epoch_date}")
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["data"][0]["orbital_elements"]["OBJECT_NAME"] == "ISS"

    # test that older OMMs ( > 2 weeks ) are not returned
    epoch_date = 2460505
    response = client.get(f"/tools/omms-at-epoch/?epoch={epoch_date}")
    assert response.status_code == 200
    assert len(response.json[0]["data"]) == 0


def test_get_omms_at_epoch_pagination(client, session, services_available):
    satellite = SatelliteFactory(
        sat_name="ISS",
        decay_date=None,
        has_current_sat_number=True,
        launch_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
    )
    epoch_date = datetime.strptime("2024-10-22", "%Y-%m-%d")
    omm = OrbitalElementsFactory(satellite=satellite, epoch=epoch_date)
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    omm_repo.add(omm)
    session.commit()
    epoch_date = 2460606
    response = client.get(f"/tools/omms-at-epoch/?epoch={epoch_date}&page=1&per_page=1")
    omms = response.json[0]["data"]
    assert response.status_code == 200
    assert len(response.json) == 1
    assert omms[0]["orbital_elements"]["OBJECT_NAME"] == "ISS"


def test_get_omms_at_epoch_optional_epoch_date(client, session, services_available):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    # get current date for OMM epoch
    epoch_date = datetime.now()
    omm = OrbitalElementsFactory(
        satellite=satellite,
        epoch=epoch_date,
    )
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    omm_repo.add(omm)
    session.commit()
    response = client.get("/tools/omms-at-epoch/")
    omms = response.json[0]["data"]
    assert response.status_code == 200
    assert len(response.json) > 0
    assert omms[0]["orbital_elements"]["OBJECT_NAME"] == "ISS"


def test_get_omms_at_epoch_zipped(client, session, services_available):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    # get current date for OMM epoch
    epoch_date = datetime.now()
    omm = OrbitalElementsFactory(
        satellite=satellite,
        epoch=epoch_date,
    )
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    omm_repo.add(omm)
    session.commit()
    response = client.get("/tools/omms-at-epoch/?format=zip")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/zip"
    assert (
        response.headers["Content-Disposition"] == "attachment; filename=omm_data.zip"
    )


def test_get_adjacent_tles(client, session, services_available):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = PRE_CUTOFF_EPOCH
    tle = TLEFactory(satellite=satellite, epoch=epoch - timedelta(days=1))
    tle2 = TLEFactory(satellite=satellite, epoch=epoch + timedelta(days=1))
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    tle_repo.add(tle2)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-adjacent-tles/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 2


def test_get_adjacent_tles_nonexistent_satellite(client, session, services_available):
    """Test get_adjacent_tles with a satellite that doesn't exist."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use a satellite ID that doesn't exist in the database
    response = client.get(
        f"/tools/get-adjacent-tles/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )

    # Should return success but with empty tle_data
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 0


def test_get_adjacent_tles_errors(client, session, services_available):
    """Test get_adjacent_tles with various error conditions."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use an invalid id_type
    response = client.get(
        f"/tools/get-adjacent-tles/?id=25544&id_type=invalid&epoch={epoch_jd}"
    )

    # Should return a bad request status
    assert response.status_code == 400
    assert "Error" in response.json["message"]

    # Missing id parameter
    response = client.get("/tools/get-adjacent-tles/?id_type=catalog&epoch=2460000.5")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Missing id_type parameter
    response = client.get("/tools/get-adjacent-tles/?id=25544&epoch=2460000.5")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Missing epoch parameter
    response = client.get("/tools/get-adjacent-tles/?id=25544&id_type=catalog")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Using a non-numeric value for epoch
    response = client.get(
        "/tools/get-adjacent-tles/?id=25544&id_type=catalog&epoch=10-01-2024"
    )
    assert response.status_code == 500
    assert "ValidationError" in response.json["error_type"]


def test_get_nearest_tle(client, session, services_available):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = PRE_CUTOFF_EPOCH
    tle = TLEFactory(satellite=satellite, epoch=epoch - timedelta(days=1))
    tle2 = TLEFactory(satellite=satellite, epoch=epoch + timedelta(days=1))
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    tle_repo.add(tle2)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-nearest-tle/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 1

    # Use a satellite ID that doesn't exist in the database
    response = client.get(
        f"/tools/get-nearest-tle/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )

    # Should return success but with empty tle_data
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 0


def test_get_nearest_tle_nonexistent_satellite(client, session, services_available):
    """Test get_nearest_tle with a satellite that doesn't exist."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use a satellite ID that doesn't exist in the database
    response = client.get(
        f"/tools/get-nearest-tle/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )

    # Should return success but with empty tle_data
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 0


@pytest.mark.parametrize(
    "params,status_code,expected_message,expected_error_type",
    [
        # Invalid id_type
        (
            {"id": "25544", "id_type": "invalid", "epoch": "2460000.5"},
            400,
            "Error",
            None,
        ),
        # Missing id parameter
        ({"id_type": "catalog", "epoch": "2460000.5"}, 400, "Missing parameter", None),
        # Missing id_type parameter
        ({"id": "25544", "epoch": "2460000.5"}, 400, "Missing parameter", None),
        # Missing epoch parameter
        ({"id": "25544", "id_type": "catalog"}, 400, "Missing parameter", None),
        # Non-numeric epoch
        (
            {"id": "25544", "id_type": "catalog", "epoch": "10-01-2024"},
            500,
            None,
            "ValidationError",
        ),
    ],
)
def test_get_nearest_tle_errors(
    client,
    session,
    params,
    status_code,
    expected_message,
    expected_error_type,
    services_available,
):
    """Test get_nearest_tle with various error conditions."""

    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    url = f"/tools/get-nearest-tle/?{query_string}"

    response = client.get(url)

    assert response.status_code == status_code

    if expected_message:
        assert expected_message in response.json["message"]

    if expected_error_type:
        assert expected_error_type in response.json["error_type"]


def test_get_nearest_tle_name_id_type(client, session, services_available):
    """Test get_nearest_tle with id_type=name."""
    # Create a satellite with a specific name
    satellite = SatelliteFactory(
        sat_name="TEST_SAT", decay_date=None, has_current_sat_number=True
    )
    epoch = PRE_CUTOFF_EPOCH
    tle = TLEFactory(satellite=satellite, epoch=epoch)
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-nearest-tle/?id=TEST_SAT&id_type=name&epoch={epoch_jd}"
    )

    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 1
    assert response.json[0]["orbital_data"][0]["satellite_name"] == "TEST_SAT"


def test_get_tles_around_epoch(client, session, services_available):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = PRE_CUTOFF_EPOCH
    tle = TLEFactory(satellite=satellite, epoch=epoch - timedelta(days=1))
    tle2 = TLEFactory(satellite=satellite, epoch=epoch + timedelta(days=1))
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    tle_repo.add(tle2)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 2


def test_get_tles_around_epoch_nonexistent_satellite(
    client, session, services_available
):
    """Test get_tles_around_epoch with a satellite that doesn't exist."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use a satellite ID that doesn't exist in the database
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )

    # Should return success but with empty tle_data
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 0


@pytest.mark.parametrize(
    "query_params,expected_status,expected_message,expected_error_type",
    [
        # Invalid id_type
        (
            {"id": "25544", "id_type": "invalid", "epoch": "2460000.5"},
            400,
            "Error",
            None,
        ),
        # Missing id parameter
        ({"id_type": "catalog", "epoch": "2460000.5"}, 400, "Missing parameter", None),
        # Missing id_type parameter
        ({"id": "25544", "epoch": "2460000.5"}, 400, "Missing parameter", None),
        # Missing epoch parameter
        ({"id": "25544", "id_type": "catalog"}, 400, "Missing parameter", None),
        # Non-numeric epoch
        (
            {"id": "25544", "id_type": "catalog", "epoch": "10-01-2024"},
            500,
            None,
            "ValidationError",
        ),
    ],
    ids=[
        "invalid id_type",
        "missing id",
        "missing id_type",
        "missing epoch",
        "non-numeric epoch",
    ],
)
def test_get_tles_around_epoch_errors(
    client,
    session,
    query_params,
    expected_status,
    expected_message,
    expected_error_type,
    services_available,
):
    """Test get_tles_around_epoch with various error conditions."""

    query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
    url = f"/tools/get-tles-around-epoch/?{query_string}"

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_message:
        assert expected_message in response.json["message"]

    if expected_error_type:
        assert expected_error_type in response.json["error_type"]


def test_get_tles_around_epoch_custom_counts(client, session, services_available):
    """Test get_tles_around_epoch with custom count_before and count_after parameters."""
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = PRE_CUTOFF_EPOCH

    # Create 5 TLEs before and 5 TLEs after the epoch
    tles_before = []
    tles_after = []
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)

    for i in range(1, 6):
        tle_before = TLEFactory(satellite=satellite, epoch=epoch - timedelta(days=i))
        tle_after = TLEFactory(satellite=satellite, epoch=epoch + timedelta(days=i))
        tles_before.append(tle_before)
        tles_after.append(tle_after)
        tle_repo.add(tle_before)
        tle_repo.add(tle_after)

    session.commit()

    epoch_jd = Time(epoch).jd

    # Test with default counts (2 before, 2 after)
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 4

    # Test with custom counts (3 before, 1 after)
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}&count_before=3&count_after=1"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 4

    # Test with custom counts (0 before, 4 after)
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}&count_before=0&count_after=4"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 4

    # Test with invalid counts
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}&count_before=-1&count_after=-2"
    )
    assert response.status_code == 500
    assert "Error" in response.json["message"]


def test_get_active_satellites(client, services_available):
    satellite = SatelliteFactory(
        sat_name="ISS",
        has_current_sat_number=True,
        decay_date=None,
        object_type="PAYLOAD",
    )
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/get-active-satellites/?object_type=payload")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/get-active-satellites/?object_type=invalid")
    assert response.status_code == 400


def test_get_starlink_generations(client, services_available):
    satellite = SatelliteFactory(
        sat_name="starlink1",
        has_current_sat_number=True,
        launch_date=datetime(2019, 5, 10),
        generation="gen1",
    )
    satellite2 = SatelliteFactory(
        sat_name="starlink2",
        has_current_sat_number=True,
        launch_date=datetime(2019, 5, 20),
        generation="gen1",
    )
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    sat_repo.add(satellite2)
    db.session.commit()

    response = client.get("/tools/get-starlink-generations/")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["generation"] == "gen1"


def test_get_starlink_generations_empty(client, session, services_available):
    """Test get_starlink_generations with no Starlink satellites in database."""
    # Ensure no Starlink satellites exist
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(session)
    response = client.get("/tools/get-starlink-generations/")
    assert response.status_code == 200
    assert response.json["count"] == 0
    assert response.json["data"] == []


def test_get_starlink_generations_invalid_data(client, session, services_available):
    """Test get_starlink_generations with invalid satellite data."""
    # Create a satellite with invalid generation data
    satellite = SatelliteFactory(
        sat_name="invalid_starlink",
        has_current_sat_number=True,
        launch_date=datetime(2019, 5, 10),
        generation=None,  # Invalid generation
    )
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(session)
    sat_repo.add(satellite)
    session.commit()

    response = client.get("/tools/get-starlink-generations/")
    assert response.status_code == 200
    # Should still return valid response, just without the invalid satellite
    assert isinstance(response.json["count"], int)
    assert isinstance(response.json["data"], list)


def test_get_starlink_generations_multiple_generations(
    client, session, services_available
):
    """Test get_starlink_generations with multiple generations."""
    # Create satellites from different generations
    gen1_sat = SatelliteFactory(
        sat_name="starlink_gen1",
        has_current_sat_number=True,
        launch_date=datetime(2019, 5, 10),
        generation="gen1",
    )
    gen2_sat = SatelliteFactory(
        sat_name="starlink_gen2",
        has_current_sat_number=True,
        launch_date=datetime(2020, 5, 10),
        generation="gen2",
    )
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(session)
    sat_repo.add(gen1_sat)
    sat_repo.add(gen2_sat)
    session.commit()

    response = client.get("/tools/get-starlink-generations/")
    assert response.status_code == 200
    assert response.json["count"] == 2
    generations = [gen["generation"] for gen in response.json["data"]]
    assert "gen1" in generations
    assert "gen2" in generations


def test_rate_limiting(client, session, services_available):
    """Test rate limiting on a TLE endpoint."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Create a valid request URL
    url = f"/tools/get-nearest-tle/?id=25544&id_type=catalog&epoch={epoch_jd}"

    num_requests = 110  # Slightly over the per-second limit of 100

    responses = []
    for _ in range(num_requests):
        responses.append(client.get(url))

    success_count = sum(1 for r in responses if r.status_code == 200)
    rate_limited_count = sum(1 for r in responses if r.status_code == 429)

    assert success_count > 0
    assert rate_limited_count > 0

    # The last request should be rate limited
    assert responses[-1].status_code == 429

    time.sleep(5)
    response = client.get(url)
    assert response.status_code == 200


def test_get_starlink_generations_db_error(client, session, mocker, services_available):
    """Test get_starlink_generations with repository connection error."""
    # Mock the repository's get_starlink_generations method to raise an exception
    mocker.patch.object(
        satellite_repository.SqlAlchemySatelliteRepository,
        "get_starlink_generations",
        side_effect=Exception("Simulated database connection failure"),
    )

    response = client.get("/tools/get-starlink-generations/")
    assert response.status_code == 500
    assert response.json["error"] == "Internal server error"
    assert "message" in response.json


def test_search_satellites(client, services_available):
    satellite = SatelliteFactory(
        sat_name="ISS",
        has_current_sat_number=True,
        decay_date=datetime.strptime("2024-10-21", "%Y-%m-%d"),
        launch_date=datetime.strptime("2024-08-21", "%Y-%m-%d"),
        object_type="PAYLOAD",
        rcs_size="LARGE",
        object_id="2024-001A",
        sat_number=25544,
    )
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/search-satellites/?name=ISS")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/search-satellites/?name=IS")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/search-satellites/?name=invalid")
    assert response.status_code == 200
    assert response.json["count"] == 0

    response = client.get("/tools/search-satellites/?norad_id=25544")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/search-satellites/?object_id=2024-001A")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/search-satellites/?decay_date_start=2451571.517396")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get(
        "/tools/search-satellites/?decay_date_start=2451571.517396&decay_date_end=2451573.517396"
    )
    assert response.status_code == 200
    assert response.json["count"] == 0

    response = client.get("/tools/search-satellites/?object_type=payload")
    assert response.status_code == 200
    assert response.json["count"] == 1

    response = client.get("/tools/search-satellites/?object_type=debris")
    assert response.status_code == 200
    assert response.json["count"] == 0

    response = client.get("/tools/search-satellites/?rcs_size=large")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/search-satellites/?rcs_size=small")
    assert response.status_code == 200
    assert response.json["count"] == 0

    response = client.get("/tools/search-satellites/?launch_date_start=2451571.517396")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/search-satellites/?launch_date_end=2460544.517396")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/search-satellites/?launch_id=2024-001")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/search-satellites/?launch_id=2024-002")
    assert response.status_code == 200
    assert response.json["count"] == 0


def test_search_satellites_validation_error(client, services_available):
    response = client.get("/tools/search-satellites/?launch_date_start=invalid-date")
    assert response.status_code != 200
    assert "message" in response.json
    assert "Invalid Julian Date" in response.json["message"]


def test_get_omm_data(client, session, services_available):
    satellite = SatelliteFactory(sat_name="ISS")
    omm = OrbitalElementsFactory(satellite=satellite)
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    omm_repo.add(omm)
    session.commit()

    response = client.get("/tools/get-omm-data/?id=ISS&id_type=name")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["orbital_elements"]["OBJECT_NAME"] == "ISS"


def test_get_omm_data_no_match(client, services_available):
    response = client.get("/tools/get-omm-data/?id=ISS&id_type=name")
    assert response.status_code == 200
    assert response.json["count"] == 0


def test_get_nearest_omm(client, session, services_available):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = datetime.now()
    omm = OrbitalElementsFactory(satellite=satellite, epoch=epoch - timedelta(days=1))
    omm2 = OrbitalElementsFactory(satellite=satellite, epoch=epoch + timedelta(days=1))
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    omm_repo.add(omm)
    omm_repo.add(omm2)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-nearest-omm/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 1
    assert "orbital_elements" in response.json[0]["orbital_data"][0]


def test_get_nearest_omm_nonexistent_satellite(client, session, services_available):
    epoch_jd = Time(datetime.now()).jd
    response = client.get(
        f"/tools/get-nearest-omm/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 0


@pytest.mark.parametrize(
    "params,status_code,expected_message,expected_error_type",
    [
        (
            {"id": "25544", "id_type": "invalid", "epoch": "2460000.5"},
            400,
            "Error",
            None,
        ),
        ({"id_type": "catalog", "epoch": "2460000.5"}, 400, "Missing parameter", None),
        ({"id": "25544", "epoch": "2460000.5"}, 400, "Missing parameter", None),
        ({"id": "25544", "id_type": "catalog"}, 400, "Missing parameter", None),
        (
            {"id": "25544", "id_type": "catalog", "epoch": "10-01-2024"},
            500,
            None,
            "ValidationError",
        ),
    ],
)
def test_get_nearest_omm_errors(
    client,
    session,
    params,
    status_code,
    expected_message,
    expected_error_type,
    services_available,
):
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    response = client.get(f"/tools/get-nearest-omm/?{query_string}")
    assert response.status_code == status_code
    if expected_message:
        assert expected_message in response.json["message"]
    if expected_error_type:
        assert expected_error_type in response.json["error_type"]


def test_get_adjacent_omms(client, session, services_available):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = datetime.now()
    omm = OrbitalElementsFactory(satellite=satellite, epoch=epoch - timedelta(days=1))
    omm2 = OrbitalElementsFactory(satellite=satellite, epoch=epoch + timedelta(days=1))
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    omm_repo.add(omm)
    omm_repo.add(omm2)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-adjacent-omms/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 2
    assert "orbital_elements" in response.json[0]["orbital_data"][0]


def test_get_adjacent_omms_nonexistent_satellite(client, session, services_available):
    epoch_jd = Time(datetime.now()).jd
    response = client.get(
        f"/tools/get-adjacent-omms/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 0


def test_get_adjacent_omms_errors(client, session, services_available):
    epoch_jd = Time(datetime.now()).jd

    # Invalid id_type
    response = client.get(
        f"/tools/get-adjacent-omms/?id=25544&id_type=invalid&epoch={epoch_jd}"
    )
    assert response.status_code == 400
    assert "Error" in response.json["message"]

    # Missing id parameter
    response = client.get("/tools/get-adjacent-omms/?id_type=catalog&epoch=2460000.5")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Missing epoch parameter
    response = client.get("/tools/get-adjacent-omms/?id=25544&id_type=catalog")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Non-numeric epoch
    response = client.get(
        "/tools/get-adjacent-omms/?id=25544&id_type=catalog&epoch=10-01-2024"
    )
    assert response.status_code == 500
    assert "ValidationError" in response.json["error_type"]


def test_get_omms_around_epoch(client, session, services_available):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = datetime.now()
    omm = OrbitalElementsFactory(satellite=satellite, epoch=epoch - timedelta(days=1))
    omm2 = OrbitalElementsFactory(satellite=satellite, epoch=epoch + timedelta(days=1))
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    omm_repo.add(omm)
    omm_repo.add(omm2)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-omms-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 2


def test_get_omms_around_epoch_nonexistent_satellite(
    client, session, services_available
):
    epoch_jd = Time(datetime.now()).jd
    response = client.get(
        f"/tools/get-omms-around-epoch/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 0


def test_get_omms_around_epoch_custom_counts(client, session, services_available):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = datetime.now()
    omm_repo = orbital_elements_repository.SqlAlchemyOrbitalElementsRepository(session)
    for i in range(1, 6):
        omm_repo.add(
            OrbitalElementsFactory(satellite=satellite, epoch=epoch - timedelta(days=i))
        )
        omm_repo.add(
            OrbitalElementsFactory(satellite=satellite, epoch=epoch + timedelta(days=i))
        )
    session.commit()

    epoch_jd = Time(epoch).jd

    # Default counts (2 before, 2 after)
    response = client.get(
        f"/tools/get-omms-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 4

    # Custom counts (3 before, 1 after)
    response = client.get(
        f"/tools/get-omms-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}&count_before=3&count_after=1"
    )
    assert response.status_code == 200
    assert len(response.json[0]["orbital_data"]) == 4


@pytest.mark.parametrize(
    "params,status_code,expected_message,expected_error_type",
    [
        (
            {"id": "25544", "id_type": "invalid", "epoch": "2460000.5"},
            400,
            "Error",
            None,
        ),
        ({"id_type": "catalog", "epoch": "2460000.5"}, 400, "Missing parameter", None),
        ({"id": "25544", "epoch": "2460000.5"}, 400, "Missing parameter", None),
        ({"id": "25544", "id_type": "catalog"}, 400, "Missing parameter", None),
        (
            {"id": "25544", "id_type": "catalog", "epoch": "10-01-2024"},
            500,
            None,
            "ValidationError",
        ),
    ],
)
def test_get_omms_around_epoch_errors(
    client,
    session,
    params,
    status_code,
    expected_message,
    expected_error_type,
    services_available,
):
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    response = client.get(f"/tools/get-omms-around-epoch/?{query_string}")
    assert response.status_code == status_code
    if expected_message:
        assert expected_message in response.json["message"]
    if expected_error_type:
        assert expected_error_type in response.json["error_type"]
