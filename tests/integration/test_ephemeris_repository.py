# ruff: noqa: S101
from datetime import datetime, timedelta, timezone

import pytest
from tests.conftest import cannot_connect_to_services
from tests.factories import InterpolableEphemerisFactory, SatelliteFactory

from api.adapters.database_orm import InterpolableEphemerisDb, SatelliteDb
from api.adapters.repositories.ephemeris_repository import SqlAlchemyEphemerisRepository


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_add_ephemeris(session):
    # Create a satellite first
    satellite = SatelliteFactory()
    db_satellite = SatelliteDb(
        sat_number=satellite.sat_number,
        sat_name=satellite.sat_name,
        has_current_sat_number=satellite.has_current_sat_number,
    )
    session.add(db_satellite)
    session.commit()

    # Create ephemeris with the satellite's ID
    ephemeris = InterpolableEphemerisFactory(satellite=db_satellite.id)
    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    ephemeris_repository.add(ephemeris)
    session.commit()

    repo_ephemeris = SqlAlchemyEphemerisRepository._to_domain(
        session.query(InterpolableEphemerisDb).one()
    )
    assert repo_ephemeris.ephemeris_start == ephemeris.ephemeris_start


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_closest_by_satellite_number(session):
    # Create a satellite first
    satellite = SatelliteFactory()
    db_satellite = SatelliteDb(
        sat_number=satellite.sat_number,
        sat_name=satellite.sat_name,
        has_current_sat_number=satellite.has_current_sat_number,
    )
    session.add(db_satellite)
    session.commit()

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    ephemeris1 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    ephemeris2 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=2),
    )
    ephemeris3 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=3),
    )
    ephemeris_repository.add(ephemeris1)
    ephemeris_repository.add(ephemeris2)
    ephemeris_repository.add(ephemeris3)
    session.commit()

    repo_ephemeris = ephemeris_repository.get_closest_by_satellite_number(
        satellite.sat_number, datetime.now(timezone.utc)
    )
    assert repo_ephemeris == ephemeris1

    repo_ephemeris2 = ephemeris_repository.get_closest_by_satellite_number(
        satellite.sat_number, datetime.now(timezone.utc) - timedelta(days=4)
    )
    assert repo_ephemeris2 is None

    repo_ephemeris3 = ephemeris_repository.get_closest_by_satellite_number(
        satellite.sat_number, datetime.now(timezone.utc) - timedelta(days=2.75)
    )
    assert repo_ephemeris3 == ephemeris3


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_closest_by_satellite_name(session):
    # Create a satellite first
    satellite = SatelliteFactory()
    db_satellite = SatelliteDb(
        sat_number=satellite.sat_number,
        sat_name=satellite.sat_name,
        has_current_sat_number=satellite.has_current_sat_number,
    )
    session.add(db_satellite)
    session.commit()

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    ephemeris1 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    ephemeris2 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=2),
    )
    ephemeris3 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=3),
    )
    ephemeris_repository.add(ephemeris1)
    ephemeris_repository.add(ephemeris2)
    ephemeris_repository.add(ephemeris3)
    session.commit()

    repo_ephemeris = ephemeris_repository.get_closest_by_satellite_name(
        satellite.sat_name, datetime.now(timezone.utc)
    )
    assert repo_ephemeris == ephemeris1

    repo_ephemeris2 = ephemeris_repository.get_closest_by_satellite_name(
        satellite.sat_name, datetime.now(timezone.utc) - timedelta(days=4)
    )
    assert repo_ephemeris2 is None

    repo_ephemeris3 = ephemeris_repository.get_closest_by_satellite_name(
        satellite.sat_name, datetime.now(timezone.utc) - timedelta(days=2.75)
    )
    assert repo_ephemeris3 == ephemeris3


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_latest_by_satellite_number(session):
    # Create a satellite first
    satellite = SatelliteFactory()
    db_satellite = SatelliteDb(
        sat_number=satellite.sat_number,
        sat_name=satellite.sat_name,
        has_current_sat_number=satellite.has_current_sat_number,
    )
    session.add(db_satellite)
    session.commit()

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    ephemeris1 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    ephemeris2 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=2),
    )
    ephemeris_repository.add(ephemeris1)
    ephemeris_repository.add(ephemeris2)

    session.commit()

    repo_ephemeris = ephemeris_repository.get_latest_by_satellite_number(
        satellite.sat_number
    )
    assert repo_ephemeris == ephemeris1


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_latest_by_satellite_name(session):
    # Create a satellite first
    satellite = SatelliteFactory()
    db_satellite = SatelliteDb(
        sat_number=satellite.sat_number,
        sat_name=satellite.sat_name,
        has_current_sat_number=satellite.has_current_sat_number,
    )
    session.add(db_satellite)
    session.commit()

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    ephemeris1 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    ephemeris2 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=2),
    )
    ephemeris_repository.add(ephemeris1)
    ephemeris_repository.add(ephemeris2)

    session.commit()

    repo_ephemeris = ephemeris_repository.get_latest_by_satellite_name(
        satellite.sat_name
    )
    assert repo_ephemeris == ephemeris1


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_closest_by_satellite_number_no_match(session):
    ephemeris_repository = SqlAlchemyEphemerisRepository(session)
    repo_ephemeris = ephemeris_repository.get_closest_by_satellite_number(
        "12345", datetime.now(timezone.utc)
    )
    assert repo_ephemeris is None


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_closest_by_satellite_name_no_match(session):
    ephemeris_repository = SqlAlchemyEphemerisRepository(session)
    repo_ephemeris = ephemeris_repository.get_closest_by_satellite_name(
        "NO_MATCH", datetime.now(timezone.utc)
    )
    assert repo_ephemeris is None


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_closest_by_satellite_number_with_data_source(session):
    # Create a satellite first
    satellite = SatelliteFactory()
    db_satellite = SatelliteDb(
        sat_number=satellite.sat_number,
        sat_name=satellite.sat_name,
        has_current_sat_number=satellite.has_current_sat_number,
    )
    session.add(db_satellite)
    session.commit()

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    # Create ephemeris with different data sources
    ephemeris1 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
        data_source="source1",
    )
    ephemeris2 = InterpolableEphemerisFactory(
        satellite=db_satellite.id,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
        data_source="source2",
    )
    ephemeris_repository.add(ephemeris1)
    ephemeris_repository.add(ephemeris2)
    session.commit()

    # Test getting ephemeris with specific data source
    repo_ephemeris = ephemeris_repository.get_closest_by_satellite_number(
        satellite.sat_number, datetime.now(timezone.utc), data_source="source1"
    )
    assert repo_ephemeris == ephemeris1

    # Test getting ephemeris with different data source
    repo_ephemeris = ephemeris_repository.get_closest_by_satellite_number(
        satellite.sat_number, datetime.now(timezone.utc), data_source="source2"
    )
    assert repo_ephemeris == ephemeris2
