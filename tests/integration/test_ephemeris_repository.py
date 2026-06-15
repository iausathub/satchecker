# ruff: noqa: S101
from datetime import datetime, timedelta, timezone

import pytest
from tests.conftest import cannot_connect_to_services
from tests.factories import InterpolableEphemerisFactory, SatelliteFactory
from tests.factories.ephemeris_factory import InterpolatorSplinesFactory

from api.adapters.database_orm import (
    InterpolableEphemerisDb,
    InterpolatedSplineDb,
    SatelliteDb,
)
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

    # Create ephemeris with the satellite object
    ephemeris = InterpolableEphemerisFactory(satellite=satellite)
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

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    ephemeris1 = InterpolableEphemerisFactory(
        id=1,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
        ephemeris_start=datetime.now(timezone.utc) - timedelta(days=1),
        ephemeris_stop=datetime.now(timezone.utc) + timedelta(days=1),
    )
    ephemeris2 = InterpolableEphemerisFactory(
        id=2,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=2),
        ephemeris_start=datetime.now(timezone.utc) - timedelta(days=2),
        ephemeris_stop=datetime.now(timezone.utc) + timedelta(days=2),
    )
    ephemeris3 = InterpolableEphemerisFactory(
        id=3,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=3),
        ephemeris_start=datetime.now(timezone.utc) - timedelta(days=3),
        ephemeris_stop=datetime.now(timezone.utc) + timedelta(days=3),
    )
    ephemeris_repository.add(ephemeris1)
    ephemeris_repository.add(ephemeris2)
    ephemeris_repository.add(ephemeris3)
    session.commit()

    repo_ephemeris = ephemeris_repository.get_closest_by_satellite_number(
        satellite.sat_number, datetime.now(timezone.utc)
    )
    assert repo_ephemeris.generated_at == ephemeris1.generated_at
    assert repo_ephemeris.ephemeris_start == ephemeris1.ephemeris_start
    assert repo_ephemeris.ephemeris_stop == ephemeris1.ephemeris_stop

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

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    ephemeris1 = InterpolableEphemerisFactory(
        id=1,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
        ephemeris_start=datetime.now(timezone.utc) - timedelta(days=1),
        ephemeris_stop=datetime.now(timezone.utc) + timedelta(days=1),
    )
    ephemeris2 = InterpolableEphemerisFactory(
        id=2,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=2),
        ephemeris_start=datetime.now(timezone.utc) - timedelta(days=2),
        ephemeris_stop=datetime.now(timezone.utc) + timedelta(days=2),
    )
    ephemeris3 = InterpolableEphemerisFactory(
        id=3,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=3),
        ephemeris_start=datetime.now(timezone.utc) - timedelta(days=3),
        ephemeris_stop=datetime.now(timezone.utc) + timedelta(days=3),
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

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    ephemeris1 = InterpolableEphemerisFactory(
        id=1,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    ephemeris2 = InterpolableEphemerisFactory(
        id=2,
        satellite=satellite,
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

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    ephemeris1 = InterpolableEphemerisFactory(
        id=1,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    ephemeris2 = InterpolableEphemerisFactory(
        id=2,
        satellite=satellite,
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

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)

    # Create ephemeris with different data sources
    ephemeris1 = InterpolableEphemerisFactory(
        id=1,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
        ephemeris_start=datetime.now(timezone.utc) - timedelta(days=1),
        ephemeris_stop=datetime.now(timezone.utc) + timedelta(days=1),
        data_source="source1",
    )
    ephemeris2 = InterpolableEphemerisFactory(
        id=2,
        satellite=satellite,
        generated_at=datetime.now(timezone.utc) - timedelta(days=1),
        ephemeris_start=datetime.now(timezone.utc) - timedelta(days=1),
        ephemeris_stop=datetime.now(timezone.utc) + timedelta(days=1),
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


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_add_interpolator_splines(session):
    # Create and persist a satellite first so FK constraints are satisfied
    satellite = SatelliteFactory()
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

    ephemeris_repository = SqlAlchemyEphemerisRepository(session)
    ephemeris = InterpolableEphemerisFactory(satellite=satellite)
    ephemeris_repository.add(ephemeris)
    session.commit()

    stored_ephemeris = session.query(InterpolableEphemerisDb).one()
    interpolator_splines = InterpolatorSplinesFactory()
    interpolator_splines.sat_id = db_satellite.id
    interpolator_splines.ephemeris_id = stored_ephemeris.id
    ephemeris_repository.add_interpolator_splines(interpolator_splines)
    assert (
        ephemeris_repository.get_interpolator_splines(stored_ephemeris.id)
        == interpolator_splines
    )
    session.query(InterpolatedSplineDb).delete()
    session.commit()


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellites_with_ephemeris(session):
    ephemeris_repository = SqlAlchemyEphemerisRepository(session)
    start_time = datetime.now(timezone.utc) - timedelta(days=1)
    end_time = datetime.now(timezone.utc) + timedelta(days=1)
    satellites = ephemeris_repository.get_satellites_with_ephemeris(
        start_time,
        end_time,
    )
    assert len(satellites) == 0

    # Add a satellite with ephemeris and check again.
    satellite = SatelliteFactory()
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
        generated_at=start_time - timedelta(hours=1),
        ephemeris_start=start_time - timedelta(hours=1),
        ephemeris_stop=end_time + timedelta(hours=1),
    )
    ephemeris_repository.add(ephemeris)
    session.commit()

    satellites = ephemeris_repository.get_satellites_with_ephemeris(
        start_time,
        end_time,
    )
    assert satellite.sat_number in satellites


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_closest_by_satellite_numbers(session):
    ephemeris_repository = SqlAlchemyEphemerisRepository(session)
    epoch = datetime.now(timezone.utc)
    data_source = "source1"
    satellite_numbers = ["12345", "67890"]
    repo_ephemeris = ephemeris_repository.get_closest_by_satellite_numbers(
        satellite_numbers, epoch, data_source
    )

    assert len(repo_ephemeris) == 0

    # Add one matching satellite/ephemeris and check again.
    satellite = SatelliteFactory(sat_number="12345")
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
        generated_at=epoch - timedelta(hours=1),
        ephemeris_start=epoch - timedelta(hours=1),
        ephemeris_stop=epoch + timedelta(hours=1),
        data_source=data_source,
    )
    ephemeris_repository.add(ephemeris)
    session.commit()

    repo_ephemeris = ephemeris_repository.get_closest_by_satellite_numbers(
        satellite_numbers, epoch, data_source
    )
    assert len(repo_ephemeris) == 1
    assert int(satellite.sat_number) in repo_ephemeris
    assert (
        repo_ephemeris[int(satellite.sat_number)].ephemeris_start
        == ephemeris.ephemeris_start
    )
    assert (
        repo_ephemeris[int(satellite.sat_number)].ephemeris_stop
        == ephemeris.ephemeris_stop
    )
    assert (
        repo_ephemeris[int(satellite.sat_number)].generated_at == ephemeris.generated_at
    )
    assert repo_ephemeris[int(satellite.sat_number)].data_source == data_source
