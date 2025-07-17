# ruff: noqa: S101

from datetime import datetime, timezone

from src.api.adapters.database_orm import SatelliteDb, SatelliteDesignationDb
from src.api.adapters.repositories.satellite_repository import (
    SqlAlchemySatelliteRepository,
)
from tests.factories import SatelliteFactory
from tests.factories.satellite_factory import SatelliteDesignationFactory


def test_get_satellite_by_id(session):
    repository = SqlAlchemySatelliteRepository(session)
    designation = SatelliteDesignationFactory(sat_name="ISS")
    satellite = SatelliteFactory(designations=[designation])
    satellite_number = satellite.get_current_designation().sat_number
    repository.add(satellite)
    session.commit()

    repo_sat = repository.get(satellite_number)
    assert repo_sat.get_current_designation().sat_name == "ISS"


def test_get_satellite_by_id_no_match(session, services_available):
    repository = SqlAlchemySatelliteRepository(session)
    session.commit()

    repo_sat = repository.get("12345")
    assert repo_sat is None


def test_add_satellite(session, services_available):
    repository = SqlAlchemySatelliteRepository(session)
    designation = SatelliteDesignationFactory(sat_name="ISS")
    satellite = SatelliteFactory(designations=[designation])
    satellite_number = satellite.get_current_designation().sat_number
    repository.add(satellite)
    session.commit()

    repo_sat = (
        session.query(SatelliteDb)
        .join(SatelliteDesignationDb)
        .filter(SatelliteDesignationDb.sat_number == satellite_number)
        .one()
    )
    assert repo_sat.designations[0].sat_name == "ISS"


def test_get_satellite_by_id_multiple(session, services_available):
    repository = SqlAlchemySatelliteRepository(session)
    designation1 = SatelliteDesignationFactory(
        sat_name="TBA",
        sat_number=1,
        valid_from=datetime(2020, 1, 1),
        valid_to=datetime(2020, 1, 2),
    )
    designation2 = SatelliteDesignationFactory(
        sat_name="ISS", sat_number=1, valid_from=datetime(2020, 1, 3), valid_to=None
    )
    designation3 = SatelliteDesignationFactory(
        sat_name="NO_MATCH",
        sat_number=1,
        valid_from=datetime(2020, 1, 4),
        valid_to=datetime(2020, 1, 5),
    )
    satellite = SatelliteFactory(
        designations=[designation1, designation2, designation3]
    )

    repository.add(satellite)
    session.commit()

    repo_sat = repository.get(1)
    assert repo_sat.get_current_designation().sat_name == "ISS"


def test_get_starlink_generations(session, services_available):
    repository = SqlAlchemySatelliteRepository(session)

    generations = repository.get_starlink_generations()
    assert len(generations) == 0

    # Create test data for two Starlink generations
    satellites = [
        SatelliteFactory(
            generation="gen1",
            launch_date=datetime(2019, 5, 10),
            designations=[
                SatelliteDesignationFactory(sat_name="starlink1", sat_number=1)
            ],
        ),
        SatelliteFactory(
            generation="gen1",
            launch_date=datetime(2019, 5, 20),
            designations=[
                SatelliteDesignationFactory(sat_name="starlink2", sat_number=2)
            ],
        ),
        SatelliteFactory(
            generation="gen2",
            launch_date=datetime(2020, 6, 10),
            designations=[
                SatelliteDesignationFactory(sat_name="starlink3", sat_number=3)
            ],
        ),
        SatelliteFactory(
            generation="gen2",
            launch_date=datetime(2020, 6, 20),
            designations=[
                SatelliteDesignationFactory(sat_name="starlink4", sat_number=4)
            ],
        ),
    ]

    for satellite in satellites:
        repository.add(satellite)
    session.commit()

    generations = repository.get_starlink_generations()
    assert len(generations) == 2
    assert generations[0].generation == "gen1"
    assert generations[0].earliest_launch == datetime(2019, 5, 10, tzinfo=timezone.utc)
    assert generations[0].latest_launch == datetime(2019, 5, 20, tzinfo=timezone.utc)
    assert generations[1].generation == "gen2"
    assert generations[1].earliest_launch == datetime(2020, 6, 10, tzinfo=timezone.utc)
    assert generations[1].latest_launch == datetime(2020, 6, 20, tzinfo=timezone.utc)
