# ruff: noqa: S101

from datetime import datetime, timedelta, timezone

import pytest
from src.api.adapters.database_orm import TLEDb
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


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_adjacent_tles(session):
    tle_repository = SqlAlchemyTLERepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc) - timedelta(days=3)
    tle_1 = TLEFactory(epoch=epoch - timedelta(days=2), satellite=satellite)
    tle_2 = TLEFactory(epoch=epoch, satellite=satellite)
    tle_3 = TLEFactory(epoch=epoch + timedelta(days=2), satellite=satellite)
    tle_4 = TLEFactory(epoch=epoch + timedelta(days=4), satellite=satellite)
    tle_5 = TLEFactory(epoch=epoch - timedelta(days=5), satellite=satellite)
    tle_repository.add(tle_1)
    tle_repository.add(tle_2)
    tle_repository.add(tle_3)
    tle_repository.add(tle_4)
    tle_repository.add(tle_5)
    session.commit()

    results = tle_repository.get_adjacent_tles(satellite.sat_number, "catalog", epoch)

    # Before and after TLEs are returned
    assert len(results) == 2

    # All TLEs are for the same satellite
    assert all(
        result.satellite.sat_number == satellite.sat_number for result in results
    )

    # One TLE is before the requested epoch and one is after
    requested_epoch = datetime.now(timezone.utc) - timedelta(days=2)
    epochs = [result.epoch for result in results]
    epochs.sort()  # Sort chronologically
    assert epochs[0] <= requested_epoch <= epochs[1]

    # The TLEs are the correct ones from above
    expected_epochs = [tle_1.epoch, tle_3.epoch]
    expected_epochs.sort()
    assert abs((epochs[0] - expected_epochs[0]).total_seconds()) < 1
    assert abs((epochs[1] - expected_epochs[1]).total_seconds()) < 1

    results = tle_repository.get_adjacent_tles(-1, "catalog", epoch)
    assert len(results) == 0


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_adjacent_tles_no_after(session):
    tle_repository = SqlAlchemyTLERepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc)
    tle_1 = TLEFactory(epoch=epoch - timedelta(days=1), satellite=satellite)
    tle_2 = TLEFactory(epoch=epoch, satellite=satellite)

    tle_repository.add(tle_1)
    tle_repository.add(tle_2)
    session.commit()

    results = tle_repository.get_adjacent_tles(satellite.sat_number, "catalog", epoch)

    # No TLE after the requested epoch is returned
    assert len(results) == 1
    assert abs((results[0].epoch - tle_1.epoch).total_seconds()) < 1


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_adjacent_tles_no_before(session):
    tle_repository = SqlAlchemyTLERepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc) - timedelta(days=1)
    tle_1 = TLEFactory(epoch=epoch + timedelta(days=1), satellite=satellite)
    tle_2 = TLEFactory(epoch=epoch, satellite=satellite)

    tle_repository.add(tle_1)
    tle_repository.add(tle_2)
    session.commit()

    results = tle_repository.get_adjacent_tles(satellite.sat_number, "catalog", epoch)

    # No TLE after the requested epoch is returned
    assert len(results) == 1
    assert abs((results[0].epoch - tle_1.epoch).total_seconds()) < 1


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_adjacent_tles_multiple_satellites(session):
    tle_repository = SqlAlchemyTLERepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS", sat_number=1)
    satellite_2 = SatelliteFactory(sat_name="TBA", sat_number=1)
    sat_repository.add(satellite)
    sat_repository.add(satellite_2)
    session.commit()

    epoch = datetime.now(timezone.utc)
    tle_1 = TLEFactory(epoch=epoch - timedelta(days=1), satellite=satellite)
    tle_2 = TLEFactory(epoch=epoch, satellite=satellite)
    tle_3 = TLEFactory(epoch=epoch + timedelta(days=1), satellite=satellite)

    tle_4 = TLEFactory(epoch=epoch - timedelta(days=1), satellite=satellite_2)
    tle_5 = TLEFactory(epoch=epoch, satellite=satellite_2)
    tle_6 = TLEFactory(epoch=epoch + timedelta(days=1), satellite=satellite_2)

    tle_repository.add(tle_1)
    tle_repository.add(tle_2)
    tle_repository.add(tle_3)
    tle_repository.add(tle_4)
    tle_repository.add(tle_5)
    tle_repository.add(tle_6)
    session.commit()

    results = tle_repository.get_adjacent_tles(satellite.sat_number, "catalog", epoch)

    # Only the TLEs for the requested satellite are returned
    assert len(results) == 2
    assert all(result.satellite.sat_name == satellite.sat_name for result in results)


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tles_around_epoch(session):
    tle_repository = SqlAlchemyTLERepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc)
    tle_1 = TLEFactory(epoch=epoch - timedelta(days=4), satellite=satellite)
    tle_2 = TLEFactory(epoch=epoch - timedelta(days=3), satellite=satellite)
    tle_3 = TLEFactory(epoch=epoch - timedelta(days=2), satellite=satellite)
    tle_4 = TLEFactory(epoch=epoch - timedelta(days=1), satellite=satellite)
    tle_5 = TLEFactory(epoch=epoch, satellite=satellite)
    tle_6 = TLEFactory(epoch=epoch + timedelta(days=1), satellite=satellite)
    tle_7 = TLEFactory(epoch=epoch + timedelta(days=2), satellite=satellite)
    tle_8 = TLEFactory(epoch=epoch + timedelta(days=3), satellite=satellite)
    tle_9 = TLEFactory(epoch=epoch + timedelta(days=4), satellite=satellite)

    tle_repository.add(tle_1)
    tle_repository.add(tle_2)
    tle_repository.add(tle_3)
    tle_repository.add(tle_4)
    tle_repository.add(tle_5)
    tle_repository.add(tle_6)
    tle_repository.add(tle_7)
    tle_repository.add(tle_8)
    tle_repository.add(tle_9)

    session.commit()

    results = tle_repository.get_tles_around_epoch(
        satellite.sat_number, "catalog", epoch, 2, 2
    )
    assert len(results) == 4

    result_identifiers = [
        (result.satellite.sat_number, result.epoch) for result in results
    ]

    assert (tle_3.satellite.sat_number, tle_3.epoch) in result_identifiers
    assert (tle_4.satellite.sat_number, tle_4.epoch) in result_identifiers
    assert (tle_6.satellite.sat_number, tle_6.epoch) in result_identifiers
    assert (tle_7.satellite.sat_number, tle_7.epoch) in result_identifiers

    results = tle_repository.get_tles_around_epoch(
        satellite.sat_number, "catalog", epoch, 1, 3
    )
    assert len(results) == 4

    result_identifiers = [
        (result.satellite.sat_number, result.epoch) for result in results
    ]

    assert (tle_4.satellite.sat_number, tle_4.epoch) in result_identifiers
    assert (tle_6.satellite.sat_number, tle_6.epoch) in result_identifiers
    assert (tle_7.satellite.sat_number, tle_7.epoch) in result_identifiers
    assert (tle_8.satellite.sat_number, tle_8.epoch) in result_identifiers

    results = tle_repository.get_tles_around_epoch(-1, "catalog", epoch, 1, 1)
    assert len(results) == 0


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_nearest_tle(session):
    tle_repository = SqlAlchemyTLERepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS", sat_number=25544)
    satellite_2 = SatelliteFactory(sat_name="ISS (ZARYA)", sat_number=25544)
    sat_repository.add(satellite)
    sat_repository.add(satellite_2)
    session.commit()

    epoch = datetime.now(timezone.utc)
    tle = TLEFactory(epoch=epoch, satellite=satellite)
    tle_2 = TLEFactory(epoch=epoch - timedelta(days=14), satellite=satellite_2)
    tle_repository.add(tle)
    tle_repository.add(tle_2)
    session.commit()

    result = tle_repository.get_nearest_tle(satellite.sat_number, "catalog", epoch)
    assert result.satellite.sat_name == satellite.sat_name

    result = tle_repository.get_nearest_tle(
        satellite_2.sat_number, "catalog", epoch - timedelta(days=8)
    )
    assert result.satellite.sat_name == satellite_2.sat_name

    result = tle_repository.get_nearest_tle(
        satellite.sat_number, "catalog", epoch + timedelta(days=100)
    )
    assert result.satellite.sat_name == satellite.sat_name

    result = tle_repository.get_nearest_tle(-1, "catalog", epoch)
    assert result is None
