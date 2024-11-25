# ruff: noqa: S101

from datetime import datetime, timedelta

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

    tle.satellite = satellite
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

    repo_tle = tle_repository.get_closest_by_satellite_number(
        tle.satellite.sat_number, tle.epoch, tle.data_source
    )
    assert repo_tle.tle_line1 == tle.tle_line1
    session.close()


def test_get_tle_by_satellite_name(sqlite_session_factory):
    session = sqlite_session_factory()
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_name(
        tle.satellite.sat_name, tle.epoch, tle.data_source
    )
    assert repo_tle.tle_line1 == tle.tle_line1
    session.close()


def test_get_tle_by_satellite_number_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    tle_repository = SqlAlchemyTLERepository(session)

    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_number(
        "12345", "2021-01-01", "data_source"
    )
    assert repo_tle is None
    session.close()


def test_get_tle_by_satellite_name_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    tle_repository = SqlAlchemyTLERepository(session)

    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_name(
        "NO_MATCH", "2021-01-01", "data_source"
    )
    assert repo_tle is None
    session.close()


def test_get_all_for_date_range_by_satellite_number(sqlite_session_factory):
    session = sqlite_session_factory()

    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

    tle = TLEFactory(satellite=satellite)
    tle_2 = TLEFactory(satellite=satellite)
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    tle_repository.add(tle_2)
    session.commit()

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_number(
        tle.satellite.sat_number, None, None
    )
    assert tle in repo_tles
    assert tle_2 in repo_tles
    session.close()


def test_get_all_for_date_range_by_satellite_name(sqlite_session_factory):
    session = sqlite_session_factory()

    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

    tle = TLEFactory(satellite=satellite)
    tle_2 = TLEFactory(satellite=satellite)
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    tle_repository.add(tle_2)
    session.commit()

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_name(
        tle.satellite.sat_name, None, None
    )
    assert tle in repo_tles
    assert tle_2 in repo_tles
    session.close()


def test_get_all_for_date_range_by_satellite_number_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    tle_repository = SqlAlchemyTLERepository(session)

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_number(
        "12345", None, None
    )
    assert repo_tles == []
    session.close()


def test_get_all_for_date_range_by_satellite_name_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    tle_repository = SqlAlchemyTLERepository(session)

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_name(
        "NO_MATCH", None, None
    )
    assert repo_tles == []
    session.close()


def test_get_all_for_date_range_with_dates(sqlite_session_factory):
    session = sqlite_session_factory()

    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

    tle = TLEFactory(satellite=satellite)
    tle_2 = TLEFactory(satellite=satellite)
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    tle_repository.add(tle_2)
    session.commit()

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_number(
        tle.satellite.sat_number,
        tle.epoch - timedelta(days=1),
        tle.epoch + timedelta(days=1),
    )
    assert tle in repo_tles
    assert tle_2 not in repo_tles

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_name(
        tle_2.satellite.sat_name,
        tle_2.epoch - timedelta(days=1),
        tle_2.epoch + timedelta(days=1),
    )

    assert tle_2 in repo_tles
    assert tle not in repo_tles
    session.close()


def test_get_norad_ids_from_satellite_name(sqlite_session_factory):
    session = sqlite_session_factory()
    satellite = SatelliteFactory()
    satellite_new = SatelliteFactory(sat_name=satellite.sat_name)
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    sat_repository.add(satellite_new)
    session.commit()

    results = sat_repository.get_norad_ids_from_satellite_name(satellite.sat_name)

    # Extract ids from results
    sat_numbers = [result[0] for result in results]
    assert satellite.sat_number in sat_numbers
    assert satellite_new.sat_number in sat_numbers
    session.close()


def test_get_satellite_names_from_norad_id(sqlite_session_factory):
    session = sqlite_session_factory()
    satellite = SatelliteFactory()
    satellite_new = SatelliteFactory(sat_number=satellite.sat_number)
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    sat_repository.add(satellite_new)
    session.commit()

    results = sat_repository.get_satellite_names_from_norad_id(satellite.sat_number)

    # Extract names from results
    sat_names = [result[0] for result in results]
    assert satellite.sat_name in sat_names
    assert satellite_new.sat_name in sat_names
    session.close()


def test_get_satellite_names_from_norad_id_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    sat_repository = SqlAlchemySatelliteRepository(session)

    results = sat_repository.get_satellite_names_from_norad_id("12345")
    assert results == []

    satellite = SatelliteFactory(sat_number="25544")
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_satellite_names_from_norad_id("12345")
    assert results == []

    session.close()


def test_get_norad_ids_from_satellite_name_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    sat_repository = SqlAlchemySatelliteRepository(session)

    results = sat_repository.get_norad_ids_from_satellite_name("NO_MATCH")
    assert results == []

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_norad_ids_from_satellite_name("NO_MATCH")
    assert results == []

    session.close()


def test_get_satellite_data_by_id(sqlite_session_factory):
    session = sqlite_session_factory()
    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_satellite_data_by_id(satellite.sat_number)
    assert results.sat_name == satellite.sat_name
    session.close()


def test_get_satellite_data_by_id_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    session.commit()

    results = sat_repository.get_satellite_data_by_id("12345")
    assert results is None
    session.close()


def test_get_satellite_data_by_name(sqlite_session_factory):
    session = sqlite_session_factory()
    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_satellite_data_by_name(satellite.sat_name)
    assert results.sat_number == satellite.sat_number
    session.close()


def test_get_satellite_data_by_name_no_match(sqlite_session_factory):
    session = sqlite_session_factory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    session.commit()

    results = sat_repository.get_satellite_data_by_name("NO_MATCH")
    assert results is None
    session.close()


def test_get_all_tles_at_epoch(sqlite_session_factory):
    session = sqlite_session_factory()
    tle_repository = SqlAlchemyTLERepository(session)

    satellite = SatelliteFactory(decay_date=None)
    satellite_2 = SatelliteFactory(decay_date=None)
    satellite_3 = SatelliteFactory(decay_date=None)
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

    # add 2 tles to the database, one with one epoch, one with another outside the range
    tle_1 = TLEFactory(epoch=datetime.now(), satellite=satellite)
    tle_2 = TLEFactory(epoch=datetime.now() - timedelta(days=30), satellite=satellite_2)
    tle_repository.add(tle_1)
    tle_repository.add(tle_2)
    session.commit()

    results = tle_repository.get_all_tles_at_epoch(datetime.now(), 1, 10, "zip")
    assert len(results[0]) == 1

    tle_3 = TLEFactory(epoch=datetime.now() - timedelta(days=12), satellite=satellite_3)
    tle_repository.add(tle_3)
    session.commit()

    results = tle_repository.get_all_tles_at_epoch(datetime.now(), 1, 10, "zip")
    assert len(results[0]) == 2
    session.close()
