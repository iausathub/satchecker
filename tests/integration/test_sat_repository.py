# ruff: noqa: S101

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
