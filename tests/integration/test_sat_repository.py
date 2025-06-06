# ruff: noqa: S101

from datetime import datetime, timezone

import pytest
from src.api.adapters.database_orm import SatelliteDb
from src.api.adapters.repositories.satellite_repository import (
    SqlAlchemySatelliteRepository,
)
from tests.conftest import cannot_connect_to_services
from tests.factories import SatelliteFactory


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_by_id(session):
    repository = SqlAlchemySatelliteRepository(session)
    satellite = SatelliteFactory(sat_name="ISS")
    satellite_number = satellite.sat_number
    repository.add(satellite)
    session.commit()

    repo_sat = repository.get(satellite_number)
    assert repo_sat.sat_name == "ISS"


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_by_id_no_match(session):
    repository = SqlAlchemySatelliteRepository(session)
    session.commit()

    repo_sat = repository.get("12345")
    assert repo_sat is None


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_add_satellite(session):
    repository = SqlAlchemySatelliteRepository(session)
    satellite = SatelliteFactory(sat_name="ISS")
    satellite_number = satellite.sat_number
    repository.add(satellite)
    session.commit()

    repo_sat = session.query(SatelliteDb).filter_by(sat_number=satellite_number).one()
    assert repo_sat.sat_name == "ISS"


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_by_id_multiple(session):
    repository = SqlAlchemySatelliteRepository(session)
    satellite1 = SatelliteFactory(
        sat_name="TBA", sat_number=1, has_current_sat_number=False
    )
    satellite2 = SatelliteFactory(
        sat_name="ISS", sat_number=1, has_current_sat_number=True
    )
    satellite3 = SatelliteFactory(
        sat_name="NO_MATCH", sat_number=1, has_current_sat_number=False
    )

    repository.add(satellite1)
    repository.add(satellite2)
    repository.add(satellite3)
    session.commit()

    repo_sat = repository.get(1)
    assert repo_sat.sat_name == "ISS"


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_starlink_generations(session):
    repository = SqlAlchemySatelliteRepository(session)

    generations = repository.get_starlink_generations()
    assert len(generations) == 0

    satellite1 = SatelliteFactory(
        sat_name="starlink1",
        sat_number=1,
        has_current_sat_number=False,
        generation="gen1",
        launch_date=datetime(2019, 5, 10),
    )
    satellite2 = SatelliteFactory(
        sat_name="starlink2",
        sat_number=2,
        has_current_sat_number=True,
        generation="gen1",
        launch_date=datetime(2019, 5, 20),
    )
    satellite3 = SatelliteFactory(
        sat_name="starlink3",
        sat_number=3,
        has_current_sat_number=False,
        generation="gen2",
        launch_date=datetime(2020, 6, 10),
    )
    satellite4 = SatelliteFactory(
        sat_name="starlink4",
        sat_number=4,
        has_current_sat_number=True,
        generation="gen2",
        launch_date=datetime(2020, 6, 20),
    )
    repository.add(satellite1)
    repository.add(satellite2)
    repository.add(satellite3)
    repository.add(satellite4)
    session.commit()

    generations = repository.get_starlink_generations()
    assert len(generations) == 2
    assert generations[0].generation == "gen1"
    assert generations[0].earliest_launch == datetime(2019, 5, 10, tzinfo=timezone.utc)
    assert generations[0].latest_launch == datetime(2019, 5, 20, tzinfo=timezone.utc)
    assert generations[1].generation == "gen2"
    assert generations[1].earliest_launch == datetime(2020, 6, 10, tzinfo=timezone.utc)
    assert generations[1].latest_launch == datetime(2020, 6, 20, tzinfo=timezone.utc)
