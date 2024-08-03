# ruff: noqa: S101

from src.api.adapters.database_orm import SatelliteDb, TLEDb
from src.api.adapters.repositories.satellite_repository import (
    SqlAlchemySatelliteRepository,
)
from src.api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from tests.factories import SatelliteFactory, TLEFactory


def test_get_satellite_by_id(sqlite_session_factory):
    session = sqlite_session_factory()
    repository = SqlAlchemySatelliteRepository(session)
    satellite = SatelliteFactory(sat_name="ISS")
    satellite_number = satellite.sat_number
    repository.add(satellite)
    session.commit()

    repo_sat = repository.get(satellite_number)
    assert repo_sat.sat_name == "ISS"
    session.close()


def test_get_satellite_by_id_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    repository = SqlAlchemySatelliteRepository(session)
    session.commit()

    repo_sat = repository.get("12345")
    assert repo_sat is None
    session.close()


def test_add_satellite(sqlite_session_factory):
    session = sqlite_session_factory()
    repository = SqlAlchemySatelliteRepository(session)
    satellite = SatelliteFactory(sat_name="ISS")
    satellite_number = satellite.sat_number
    repository.add(satellite)
    session.commit()

    repo_sat = session.query(SatelliteDb).filter_by(sat_number=satellite_number).one()
    assert repo_sat.sat_name == "ISS"
    session.close()


def test_get_satellite_by_id_multiple(sqlite_session_factory):
    session = sqlite_session_factory()
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


def test_add_tle(sqlite_session_factory):
    session = sqlite_session_factory()
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = SqlAlchemyTLERepository._to_domain(session.query(TLEDb).one())
    assert repo_tle.tle_line1 == tle.tle_line1
    session.close()


def test_add_tle_existing_satellite(sqlite_session_factory):
    session = sqlite_session_factory()
    tle = TLEFactory()
    satellite = SatelliteFactory()

    tle_repository = SqlAlchemyTLERepository(session)
    satellite_repository = SqlAlchemySatelliteRepository(session)

    satellite_repository.add(satellite)

    tle.tle_satellite = satellite
    tle_repository.add(tle)
    session.commit()

    repo_tle = SqlAlchemyTLERepository._to_domain(session.query(TLEDb).one())
    assert repo_tle.tle_line1 == tle.tle_line1
    session.close()


def test_get_tle_by_satellite_number(sqlite_session_factory):
    session = sqlite_session_factory()
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = tle_repository.get_by_satellite_number(
        tle.tle_satellite.sat_number, tle.epoch, tle.data_source
    )
    assert repo_tle.tle_line1 == tle.tle_line1
    session.close()


def test_get_tle_by_satellite_name(sqlite_session_factory):
    session = sqlite_session_factory()
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = tle_repository.get_by_satellite_name(
        tle.tle_satellite.sat_name, tle.epoch, tle.data_source
    )
    assert repo_tle.tle_line1 == tle.tle_line1
    session.close()


def test_get_tle_by_satellite_number_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    tle_repository = SqlAlchemyTLERepository(session)

    session.commit()

    repo_tle = tle_repository.get_by_satellite_number(
        "12345", "2021-01-01", "data_source"
    )
    assert repo_tle is None
    session.close()


def test_get_tle_by_satellite_name_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    tle_repository = SqlAlchemyTLERepository(session)

    session.commit()

    repo_tle = tle_repository.get_by_satellite_name(
        "NO_MATCH", "2021-01-01", "data_source"
    )
    assert repo_tle is None
    session.close()
