# ruff: noqa: S101

from datetime import datetime, timedelta

import pytest
from src.api.adapters.database_orm import SatelliteDb, TLEDb
from src.api.adapters.repositories.satellite_repository import (
    SqlAlchemySatelliteRepository,
)
from src.api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from tests.conftest import cannot_connect_to_services
from tests.factories import SatelliteFactory, TLEFactory


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
def test_add_tle(session):
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = SqlAlchemyTLERepository._to_domain(session.query(TLEDb).one())
    assert repo_tle.tle_line1 == tle.tle_line1


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_add_tle_existing_satellite(session):
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


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tle_by_satellite_number(session):
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_number(
        tle.satellite.sat_number, tle.epoch, tle.data_source
    )
    assert repo_tle.tle_line1 == tle.tle_line1


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tle_by_satellite_name(session):
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_name(
        tle.satellite.sat_name, tle.epoch, tle.data_source
    )
    assert repo_tle.tle_line1 == tle.tle_line1


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tle_by_satellite_number_no_match(session):
    tle_repository = SqlAlchemyTLERepository(session)

    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_number(
        "12345", "2021-01-01", "data_source"
    )
    assert repo_tle is None


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tle_by_satellite_name_no_match(session):
    tle_repository = SqlAlchemyTLERepository(session)

    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_name(
        "NO_MATCH", "2021-01-01", "data_source"
    )
    assert repo_tle is None


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_all_for_date_range_by_satellite_number(session):

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
    assert any(t.tle_line1 == tle.tle_line1 for t in repo_tles)
    assert any(t.tle_line1 == tle_2.tle_line1 for t in repo_tles)
    assert len(repo_tles) == 2


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_all_for_date_range_by_satellite_name(session):
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
    assert any(t.tle_line1 == tle.tle_line1 for t in repo_tles)
    assert any(t.tle_line1 == tle_2.tle_line1 for t in repo_tles)
    assert len(repo_tles) == 2


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_all_for_date_range_by_satellite_number_no_match(session):
    tle_repository = SqlAlchemyTLERepository(session)

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_number(
        "12345", None, None
    )
    assert repo_tles == []


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_all_for_date_range_by_satellite_name_no_match(session):
    tle_repository = SqlAlchemyTLERepository(session)

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_name(
        "NO_MATCH", None, None
    )
    assert repo_tles == []


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_all_for_date_range_with_dates(session):
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
    assert any(t.tle_line1 == tle.tle_line1 for t in repo_tles)
    assert len(repo_tles) == 1

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_name(
        tle_2.satellite.sat_name,
        tle_2.epoch - timedelta(days=1),
        tle_2.epoch + timedelta(days=1),
    )

    assert any(t.tle_line1 == tle_2.tle_line1 for t in repo_tles)
    assert len(repo_tles) == 1


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_norad_ids_from_satellite_name(session):
    satellite = SatelliteFactory()
    satellite_new = SatelliteFactory(sat_name=satellite.sat_name)
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    sat_repository.add(satellite_new)
    session.commit()

    results = sat_repository.get_norad_ids_from_satellite_name(satellite.sat_name)
    sat_numbers = [result[0] for result in results]
    assert satellite.sat_number in sat_numbers
    assert satellite_new.sat_number in sat_numbers


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_names_from_norad_id(session):
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


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_names_from_norad_id_no_match(session):
    sat_repository = SqlAlchemySatelliteRepository(session)

    results = sat_repository.get_satellite_names_from_norad_id("12345")
    assert results == []

    satellite = SatelliteFactory(sat_number="25544")
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_satellite_names_from_norad_id("12345")
    assert results == []


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_norad_ids_from_satellite_name_no_match(session):
    sat_repository = SqlAlchemySatelliteRepository(session)

    results = sat_repository.get_norad_ids_from_satellite_name("NO_MATCH")
    assert results == []

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_norad_ids_from_satellite_name("NO_MATCH")
    assert results == []


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_data_by_id(session):
    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_satellite_data_by_id(satellite.sat_number)
    assert results.sat_name == satellite.sat_name


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_data_by_id_no_match(session):
    sat_repository = SqlAlchemySatelliteRepository(session)
    session.commit()

    results = sat_repository.get_satellite_data_by_id("12345")
    assert results is None


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_data_by_name(session):
    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_satellite_data_by_name(satellite.sat_name)
    assert results.sat_number == satellite.sat_number


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_data_by_name_no_match(session):
    sat_repository = SqlAlchemySatelliteRepository(session)
    session.commit()

    results = sat_repository.get_satellite_data_by_name("NO_MATCH")
    assert results is None


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_all_tles_at_epoch(session):
    tle_repository = SqlAlchemyTLERepository(session)

    satellite = SatelliteFactory(decay_date=None)
    satellite_2 = SatelliteFactory(decay_date=None)
    satellite_3 = SatelliteFactory(decay_date=None)
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

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
