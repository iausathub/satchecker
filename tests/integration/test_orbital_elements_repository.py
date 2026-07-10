# ruff: noqa: S101

import time
from datetime import datetime, timedelta, timezone

import pytest
from src.api.adapters.database_orm import OrbitalElementsDb
from src.api.adapters.repositories.orbital_elements_repository import (
    SqlAlchemyOrbitalElementsRepository,
)
from src.api.adapters.repositories.satellite_repository import (
    SqlAlchemySatelliteRepository,
)
from tests.factories import OrbitalElementsFactory, SatelliteFactory

from api.services.cache_service import (
    RECENT_ORBITAL_ELEMENTS_CACHE_KEY,
    set_cached_data,
)


def test_add_orbital_elements(session, services_available):
    orbital_elements = OrbitalElementsFactory()
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    orbital_elements_repository.add(orbital_elements)
    session.commit()

    repo_orbital_elements = SqlAlchemyOrbitalElementsRepository._to_domain(
        session.query(OrbitalElementsDb).one()
    )
    assert repo_orbital_elements == orbital_elements


def test_add_orbital_elements_existing_satellite(session, services_available):
    orbital_elements = OrbitalElementsFactory()
    satellite = SatelliteFactory()

    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    satellite_repository = SqlAlchemySatelliteRepository(session)

    satellite_repository.add(satellite)

    orbital_elements.satellite = satellite
    orbital_elements_repository.add(orbital_elements)
    session.commit()

    repo_orbital_elements = SqlAlchemyOrbitalElementsRepository._to_domain(
        session.query(OrbitalElementsDb).one()
    )
    assert repo_orbital_elements.epoch == orbital_elements.epoch


def test_get_orbital_elements_by_satellite_number(session, services_available):
    orbital_elements = OrbitalElementsFactory()
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    orbital_elements_repository.add(orbital_elements)
    session.commit()

    repo_orbital_elements = orbital_elements_repository.get_closest_by_satellite_number(
        orbital_elements.satellite.sat_number,
        orbital_elements.epoch,
        orbital_elements.data_source,
    )
    assert repo_orbital_elements.epoch == orbital_elements.epoch


def test_get_orbital_elements_by_satellite_name(session, services_available):
    orbital_elements = OrbitalElementsFactory()
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    orbital_elements_repository.add(orbital_elements)
    session.commit()

    repo_orbital_elements = orbital_elements_repository.get_closest_by_satellite_name(
        orbital_elements.satellite.sat_name,
        orbital_elements.epoch,
        orbital_elements.data_source,
    )
    assert repo_orbital_elements.epoch == orbital_elements.epoch


def test_get_orbital_elements_by_satellite_number_no_match(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    session.commit()

    repo_tle = orbital_elements_repository.get_closest_by_satellite_number(
        "12345", "2021-01-01", "data_source"
    )
    assert repo_tle is None


def test_get_orbital_elements_by_satellite_name_no_match(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    session.commit()

    repo_tle = orbital_elements_repository.get_closest_by_satellite_name(
        "NO_MATCH", "2021-01-01", "data_source"
    )
    assert repo_tle is None


def test_get_all_for_date_range_by_satellite_number(session, services_available):

    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

    data_set1 = OrbitalElementsFactory(satellite=satellite)
    data_set2 = OrbitalElementsFactory(satellite=satellite)
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    session.commit()

    repo_orbital_elements = (
        orbital_elements_repository.get_all_for_date_range_by_satellite_number(
            data_set1.satellite.sat_number, None, None
        )
    )
    assert any(t.epoch == data_set1.epoch for t in repo_orbital_elements)
    assert any(t.epoch == data_set2.epoch for t in repo_orbital_elements)
    assert len(repo_orbital_elements) == 2


def test_get_all_for_date_range_by_satellite_name(session, services_available):
    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

    data_set1 = OrbitalElementsFactory(satellite=satellite)
    data_set2 = OrbitalElementsFactory(satellite=satellite)
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    session.commit()

    repo_orbital_elements = (
        orbital_elements_repository.get_all_for_date_range_by_satellite_name(
            data_set1.satellite.sat_name, None, None
        )
    )
    assert any(t.epoch == data_set1.epoch for t in repo_orbital_elements)
    assert any(t.epoch == data_set2.epoch for t in repo_orbital_elements)
    assert len(repo_orbital_elements) == 2


def test_get_all_for_date_range_by_satellite_number_no_match(
    session, services_available
):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    repo_orbital_elements = (
        orbital_elements_repository.get_all_for_date_range_by_satellite_number(
            "12345", None, None
        )
    )
    assert repo_orbital_elements == []


def test_get_all_for_date_range_by_satellite_name_no_match(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    repo_orbital_elements = (
        orbital_elements_repository.get_all_for_date_range_by_satellite_name(
            "NO_MATCH", None, None
        )
    )
    assert repo_orbital_elements == []


def test_get_all_for_date_range_with_dates(session, services_available):
    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

    data_set1 = OrbitalElementsFactory(satellite=satellite)
    data_set2 = OrbitalElementsFactory(satellite=satellite)
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    session.commit()

    repo_orbital_elements = (
        orbital_elements_repository.get_all_for_date_range_by_satellite_number(
            data_set1.satellite.sat_number,
            data_set1.epoch - timedelta(days=1),
            data_set1.epoch + timedelta(days=1),
        )
    )
    assert any(t.epoch == data_set1.epoch for t in repo_orbital_elements)
    assert len(repo_orbital_elements) == 1

    repo_orbital_elements = (
        orbital_elements_repository.get_all_for_date_range_by_satellite_name(
            data_set2.satellite.sat_name,
            data_set2.epoch - timedelta(days=1),
            data_set2.epoch + timedelta(days=1),
        )
    )

    assert any(t.epoch == data_set2.epoch for t in repo_orbital_elements)
    assert len(repo_orbital_elements) == 1


def test_get_all_orbital_elements_at_epoch(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    satellite = SatelliteFactory(decay_date=None)
    satellite_2 = SatelliteFactory(decay_date=None)
    satellite_3 = SatelliteFactory(decay_date=None)
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

    data_set1 = OrbitalElementsFactory(
        epoch=datetime.now(timezone.utc), satellite=satellite
    )
    data_set2 = OrbitalElementsFactory(
        epoch=datetime.now(timezone.utc) - timedelta(days=30), satellite=satellite_2
    )
    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    session.commit()

    results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
        datetime.now(timezone.utc), 1, 10, "zip"
    )
    assert len(results[0]) == 1

    data_set3 = OrbitalElementsFactory(
        epoch=datetime.now(timezone.utc) - timedelta(days=12), satellite=satellite_3
    )
    orbital_elements_repository.add(data_set3)
    session.commit()

    results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
        datetime.now(timezone.utc), 1, 10, "zip"
    )
    assert len(results[0]) == 2


def test_get_adjacent_orbital_elements(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc) - timedelta(days=3)
    data_set1 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=2), satellite=satellite
    )
    data_set2 = OrbitalElementsFactory(epoch=epoch, satellite=satellite)
    data_set3 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=2), satellite=satellite
    )
    data_set4 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=4), satellite=satellite
    )
    data_set5 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=5), satellite=satellite
    )
    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    orbital_elements_repository.add(data_set3)
    orbital_elements_repository.add(data_set4)
    orbital_elements_repository.add(data_set5)
    session.commit()

    results = orbital_elements_repository.get_adjacent_orbital_elements(
        satellite.sat_number, "catalog", epoch
    )

    # Before and after orbital elements are returned
    assert len(results) == 2

    # All orbital elements are for the same satellite
    assert all(
        result.satellite.sat_number == satellite.sat_number for result in results
    )

    # One orbital element is before the requested epoch and one is after
    requested_epoch = datetime.now(timezone.utc) - timedelta(days=2)
    epochs = [result.epoch for result in results]
    epochs.sort()  # Sort chronologically
    assert epochs[0] <= requested_epoch <= epochs[1]

    # The orbital elements are the correct ones from above
    expected_epochs = [data_set1.epoch, data_set3.epoch]
    expected_epochs.sort()
    assert abs((epochs[0] - expected_epochs[0]).total_seconds()) < 1
    assert abs((epochs[1] - expected_epochs[1]).total_seconds()) < 1

    results = orbital_elements_repository.get_adjacent_orbital_elements(
        -1, "catalog", epoch
    )
    assert len(results) == 0


def test_get_adjacent_orbital_elements_no_after(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc)
    data_set1 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=1), satellite=satellite
    )
    data_set2 = OrbitalElementsFactory(epoch=epoch, satellite=satellite)

    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    session.commit()

    results = orbital_elements_repository.get_adjacent_orbital_elements(
        satellite.sat_number, "catalog", epoch
    )

    # No TLE after the requested epoch is returned
    assert len(results) == 1
    assert abs((results[0].epoch - data_set1.epoch).total_seconds()) < 1


def test_get_adjacent_orbital_elements_no_before(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc) - timedelta(days=1)
    data_set1 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=1), satellite=satellite
    )
    data_set2 = OrbitalElementsFactory(epoch=epoch, satellite=satellite)

    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    session.commit()

    results = orbital_elements_repository.get_adjacent_orbital_elements(
        satellite.sat_number, "catalog", epoch
    )

    # No TLE after the requested epoch is returned
    assert len(results) == 1
    assert abs((results[0].epoch - data_set1.epoch).total_seconds()) < 1


def test_get_adjacent_orbital_elements_multiple_satellites(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS", sat_number=1)
    satellite_2 = SatelliteFactory(sat_name="TBA", sat_number=1)
    sat_repository.add(satellite)
    sat_repository.add(satellite_2)
    session.commit()

    epoch = datetime.now(timezone.utc)
    data_set1 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=1), satellite=satellite
    )
    data_set2 = OrbitalElementsFactory(epoch=epoch, satellite=satellite)
    data_set3 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=1), satellite=satellite
    )

    data_set4 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=1), satellite=satellite_2
    )
    data_set5 = OrbitalElementsFactory(epoch=epoch, satellite=satellite_2)
    data_set6 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=1), satellite=satellite_2
    )

    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    orbital_elements_repository.add(data_set3)
    orbital_elements_repository.add(data_set4)
    orbital_elements_repository.add(data_set5)
    orbital_elements_repository.add(data_set6)
    session.commit()

    results = orbital_elements_repository.get_adjacent_orbital_elements(
        satellite.sat_number, "catalog", epoch
    )

    # Only the TLEs for the requested satellite are returned
    assert len(results) == 2
    assert all(result.satellite.sat_name == satellite.sat_name for result in results)


def test_get_adjacent_orbital_elements_by_name(session, services_available):
    """id_type='name' must work the same as id_type='catalog'"""
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc) - timedelta(days=3)
    data_set1 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=2), satellite=satellite
    )
    data_set2 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=2), satellite=satellite
    )
    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    session.commit()

    results = orbital_elements_repository.get_adjacent_orbital_elements(
        satellite.sat_name, "name", epoch
    )

    assert len(results) == 2
    epochs = sorted(result.epoch for result in results)
    assert abs((epochs[0] - data_set1.epoch).total_seconds()) < 1
    assert abs((epochs[1] - data_set2.epoch).total_seconds()) < 1

    results = orbital_elements_repository.get_adjacent_orbital_elements(
        "NONEXISTENT", "name", epoch
    )
    assert len(results) == 0


def test_get_orbital_elements_around_epoch(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc)
    data_set1 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=4), satellite=satellite
    )
    data_set2 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=3), satellite=satellite
    )
    data_set3 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=2), satellite=satellite
    )
    data_set4 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=1), satellite=satellite
    )
    data_set5 = OrbitalElementsFactory(epoch=epoch, satellite=satellite)
    data_set6 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=1), satellite=satellite
    )
    data_set7 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=2), satellite=satellite
    )
    data_set8 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=3), satellite=satellite
    )
    data_set9 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=4), satellite=satellite
    )

    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    orbital_elements_repository.add(data_set3)
    orbital_elements_repository.add(data_set4)
    orbital_elements_repository.add(data_set5)
    orbital_elements_repository.add(data_set6)
    orbital_elements_repository.add(data_set7)
    orbital_elements_repository.add(data_set8)
    orbital_elements_repository.add(data_set9)

    session.commit()

    results = orbital_elements_repository.get_orbital_elements_around_epoch(
        satellite.sat_number, "catalog", epoch, 2, 2
    )
    assert len(results) == 4

    result_identifiers = [
        (result.satellite.sat_number, result.epoch) for result in results
    ]

    assert (data_set3.satellite.sat_number, data_set3.epoch) in result_identifiers
    assert (data_set4.satellite.sat_number, data_set4.epoch) in result_identifiers
    assert (data_set6.satellite.sat_number, data_set6.epoch) in result_identifiers
    assert (data_set7.satellite.sat_number, data_set7.epoch) in result_identifiers

    results = orbital_elements_repository.get_orbital_elements_around_epoch(
        satellite.sat_number, "catalog", epoch, 1, 3
    )
    assert len(results) == 4

    result_identifiers = [
        (result.satellite.sat_number, result.epoch) for result in results
    ]

    assert (data_set4.satellite.sat_number, data_set4.epoch) in result_identifiers
    assert (data_set6.satellite.sat_number, data_set6.epoch) in result_identifiers
    assert (data_set7.satellite.sat_number, data_set7.epoch) in result_identifiers
    assert (data_set8.satellite.sat_number, data_set8.epoch) in result_identifiers

    results = orbital_elements_repository.get_orbital_elements_around_epoch(
        -1, "catalog", epoch, 1, 1
    )
    assert len(results) == 0


def test_get_orbital_elements_around_epoch_by_name(session, services_available):
    """id_type='name' must work the same as id_type='catalog'"""
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)

    epoch = datetime.now(timezone.utc)
    data_set1 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=1), satellite=satellite
    )
    data_set2 = OrbitalElementsFactory(epoch=epoch, satellite=satellite)
    data_set3 = OrbitalElementsFactory(
        epoch=epoch + timedelta(days=1), satellite=satellite
    )

    orbital_elements_repository.add(data_set1)
    orbital_elements_repository.add(data_set2)
    orbital_elements_repository.add(data_set3)
    session.commit()

    results = orbital_elements_repository.get_orbital_elements_around_epoch(
        satellite.sat_name, "name", epoch, 1, 1
    )
    assert len(results) == 2
    result_epochs = sorted(result.epoch for result in results)
    assert abs((result_epochs[0] - data_set1.epoch).total_seconds()) < 1
    assert abs((result_epochs[1] - data_set3.epoch).total_seconds()) < 1

    results = orbital_elements_repository.get_orbital_elements_around_epoch(
        "NONEXISTENT", "name", epoch, 1, 1
    )
    assert len(results) == 0


def test_get_nearest_orbital_elements(session, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(sat_name="ISS", sat_number=25544)
    satellite_2 = SatelliteFactory(sat_name="ISS (ZARYA)", sat_number=25544)
    sat_repository.add(satellite)
    sat_repository.add(satellite_2)
    session.commit()

    epoch = datetime.now(timezone.utc)
    orbital_elements = OrbitalElementsFactory(epoch=epoch, satellite=satellite)
    orbital_elements_2 = OrbitalElementsFactory(
        epoch=epoch - timedelta(days=14), satellite=satellite_2
    )
    orbital_elements_repository.add(orbital_elements)
    orbital_elements_repository.add(orbital_elements_2)
    session.commit()

    result = orbital_elements_repository.get_nearest_orbital_elements(
        satellite.sat_number, "catalog", epoch
    )
    assert result.satellite.sat_name == satellite.sat_name

    result = orbital_elements_repository.get_nearest_orbital_elements(
        satellite_2.sat_number, "catalog", epoch - timedelta(days=8)
    )
    assert result.satellite.sat_name == satellite_2.sat_name

    result = orbital_elements_repository.get_nearest_orbital_elements(
        satellite.sat_number, "catalog", epoch + timedelta(days=100)
    )
    assert result.satellite.sat_name == satellite.sat_name

    result = orbital_elements_repository.get_nearest_orbital_elements(
        -1, "catalog", epoch
    )
    assert result is None


def test_get_all_orbital_elements_at_epoch_cache(session, app, services_available):
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)

    # Empty cache, no orbital elements added yet
    results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
        datetime.now(timezone.utc), 1, 10, "zip"
    )
    assert len(results[0]) == 0

    # Add orbital elements to repository
    satellite = SatelliteFactory(
        sat_name="ISS",
        decay_date=None,
        launch_date=datetime.now(timezone.utc) - timedelta(days=1000),
        has_current_sat_number=True,
    )
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    session.commit()

    data_set1 = OrbitalElementsFactory(
        epoch=datetime.now(timezone.utc), satellite=satellite
    )
    orbital_elements_repository.add(data_set1)
    data_set2 = OrbitalElementsFactory(
        epoch=datetime.now(timezone.utc) - timedelta(days=1), satellite=satellite
    )
    orbital_elements_repository.add(data_set2)
    session.commit()

    # Explicitly initialize the cache with our test data for consistent testing
    batch_serialize_orbital_elements = (
        SqlAlchemyOrbitalElementsRepository.batch_serialize_orbital_elements
    )
    with app.app_context():
        print("DEBUG - Manually initializing Redis cache with test data")
        cache_data = {
            "orbital_elements": batch_serialize_orbital_elements([data_set1]),
            "total_count": 1,
            "cached_at": datetime.now(timezone.utc).isoformat(),
        }
        set_cached_data(RECENT_ORBITAL_ELEMENTS_CACHE_KEY, cache_data)

    # Check that orbital elements are returned from cache
    try:
        results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        assert len(results[0]) == 1
        assert results[2] == "cache"
    except Exception as e:
        print(e)
        raise e

    # Check that orbital elements are returned from database for an older date
    results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
        datetime.now(timezone.utc) - timedelta(days=0.5), 1, 10, "zip"
    )
    assert len(results[0]) == 1
    assert results[2] == "database"

    # Check that orbital elements are returned from cache for a future date
    results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
        datetime.now(timezone.utc) + timedelta(days=1), 1, 10, "zip"
    )
    assert len(results[0]) == 1
    assert results[2] == "cache"

    # temporarily change cache storage time
    with app.app_context():
        orbital_elements_repository.cache_ttl = 5

        cache_data = {
            "orbital_elements": batch_serialize_orbital_elements([data_set1]),
            "total_count": 1,
            "cached_at": datetime.now(timezone.utc).isoformat(),
        }
        success = set_cached_data(RECENT_ORBITAL_ELEMENTS_CACHE_KEY, cache_data, ttl=5)
        assert success

        results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        assert results[2] == "cache"

        # wait for cache to expire
        time.sleep(6)
        results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        assert results[2] == "database"

    # test that the TLEs load from the database if there are issues with the cache
    with app.app_context():
        cache_results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        orbital_elements_repository.cache_enabled = False

        db_results = orbital_elements_repository.get_all_orbital_elements_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        assert db_results[2] == "database"
        assert cache_results[0] == db_results[0]


def test_get_all_orbital_elements_at_epoch_with_constellation(
    session, services_available
):
    """Test getting orbital elements filtered by constellation."""
    # Create satellites with different constellations
    starlink_sat = SatelliteFactory(
        constellation="starlink",
        launch_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        decay_date=None,
    )
    oneweb_sat = SatelliteFactory(
        constellation="oneweb",
        launch_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        decay_date=None,
    )

    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(starlink_sat)
    sat_repository.add(oneweb_sat)
    session.commit()

    # Create orbital elements for both satellites with the same epoch
    epoch = datetime(2024, 6, 1, tzinfo=timezone.utc)
    starlink_data_set = OrbitalElementsFactory(satellite=starlink_sat, epoch=epoch)
    oneweb_data_set = OrbitalElementsFactory(satellite=oneweb_sat, epoch=epoch)

    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    orbital_elements_repository.add(starlink_data_set)
    orbital_elements_repository.add(oneweb_data_set)
    session.commit()

    # Test filtering by starlink constellation
    starlink_tles, count, _ = (
        orbital_elements_repository.get_all_orbital_elements_at_epoch(
            epoch, 1, 10000, "zip", "starlink"
        )
    )
    assert len(starlink_tles) == 1
    assert starlink_tles[0].satellite.constellation == "starlink"

    # Test filtering by oneweb constellation
    oneweb_data, count, _ = (
        orbital_elements_repository.get_all_orbital_elements_at_epoch(
            epoch, 1, 10000, "zip", "oneweb"
        )
    )
    assert len(oneweb_data) == 1
    assert oneweb_data[0].satellite.constellation == "oneweb"

    # Test with no constellation filter
    all_data, count, _ = orbital_elements_repository.get_all_orbital_elements_at_epoch(
        epoch, 1, 10000, "zip", None
    )
    assert len(all_data) == 2


def test_get_all_orbital_elements_at_epoch_with_data_source(
    session, services_available
):
    """Test getting orbital elements filtered by data source"""
    # Create satellites with different data sources
    satellite = SatelliteFactory(
        launch_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        decay_date=None,
    )
    satellite_2 = SatelliteFactory(
        launch_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        decay_date=None,
    )
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    sat_repository.add(satellite_2)
    session.commit()

    # Create TLEs for both satellites with the same epoch
    epoch = datetime(2024, 6, 1, tzinfo=timezone.utc)
    spacetrack_data_set = OrbitalElementsFactory(
        satellite=satellite, epoch=epoch, data_source="spacetrack"
    )
    celestrak_data_set = OrbitalElementsFactory(
        satellite=satellite_2, epoch=epoch, data_source="celestrak"
    )
    orbital_elements_repository = SqlAlchemyOrbitalElementsRepository(session)
    orbital_elements_repository.add(spacetrack_data_set)
    orbital_elements_repository.add(celestrak_data_set)
    session.commit()

    # Test filtering by spacetrack data source
    spacetrack_data, count, _ = (
        orbital_elements_repository._get_all_orbital_elements_at_epoch(
            epoch, 1, 10000, "zip", data_source_limit="spacetrack"
        )
    )
    assert len(spacetrack_data) == 1
    assert spacetrack_data[0].data_source == "spacetrack"

    # Test filtering by celestrak data source
    celestrak_data, count, _ = (
        orbital_elements_repository._get_all_orbital_elements_at_epoch(
            epoch, 1, 10000, "zip", data_source_limit="celestrak"
        )
    )
    assert len(celestrak_data) == 1
    assert celestrak_data[0].data_source == "celestrak"

    # Test filtering by any data source
    all_data, count, _ = orbital_elements_repository._get_all_orbital_elements_at_epoch(
        epoch, 1, 10000, "zip", data_source_limit="any"
    )
    assert len(all_data) == 2
    assert all_data[0].data_source == "spacetrack"
    assert all_data[1].data_source == "celestrak"


def test_batch_serialize_orbital_elements_with_factory_data():
    """
    Test batch_serialize_orbital_elements with actual orbital elements factory data.
    """
    satellite = SatelliteFactory()
    data_set = OrbitalElementsFactory(satellite=satellite)

    result = SqlAlchemyOrbitalElementsRepository.batch_serialize_orbital_elements(
        [data_set]
    )

    assert len(result) == 1
    assert "mean_motion" in result[0]
    assert "eccentricity" in result[0]
    assert "inclination" in result[0]
    assert "ra_of_ascending_node" in result[0]
    assert "arg_of_pericenter" in result[0]
    assert "mean_anomaly" in result[0]
    assert "ephemeris_type" in result[0]
    assert "classification_type" in result[0]
    assert "element_set_no" in result[0]
    assert "rev_at_epoch" in result[0]
    assert "bstar" in result[0]
    assert "mean_motion_dot" in result[0]
    assert "mean_motion_ddot" in result[0]
    assert "epoch" in result[0]
    assert "date_collected" in result[0]
    assert "data_source" in result[0]
    assert "satellite" in result[0]


def test_batch_serialize_orbital_elements_missing_satellite_attribute(mocker):
    """Test handling of orbital elements with missing satellite attribute."""
    mock_orbital_elements = mocker.Mock()
    mock_orbital_elements.satellite = None
    mock_orbital_elements.mean_motion = 0
    mock_orbital_elements.eccentricity = 0
    mock_orbital_elements.inclination = 0
    mock_orbital_elements.ra_of_ascending_node = 0
    mock_orbital_elements.arg_of_pericenter = 0
    mock_orbital_elements.mean_anomaly = 0
    mock_orbital_elements.ephemeris_type = 0
    mock_orbital_elements.classification_type = "U"
    mock_orbital_elements.element_set_no = 0

    with pytest.raises(AttributeError):
        SqlAlchemyOrbitalElementsRepository.batch_serialize_orbital_elements(
            [mock_orbital_elements]
        )


def test_batch_serialize_orbital_elements_satellite_missing_attributes(mocker):
    """
    Test batch_serialize_orbital_elements with satellite missing has_current_sat_number.
    """
    mock_satellite = mocker.Mock()
    mock_satellite.sat_name = "TEST SAT"
    mock_satellite.sat_number = 12345
    mock_satellite.decay_date = None

    # Missing has_current_sat_number attribute
    del mock_satellite.has_current_sat_number

    mock_orbital_elements = mocker.Mock()
    mock_orbital_elements.satellite = mock_satellite
    mock_orbital_elements.mean_motion = 0
    mock_orbital_elements.eccentricity = 0
    mock_orbital_elements.inclination = 0
    mock_orbital_elements.ra_of_ascending_node = 0
    mock_orbital_elements.arg_of_pericenter = 0
    mock_orbital_elements.mean_anomaly = 0
    mock_orbital_elements.ephemeris_type = 0
    mock_orbital_elements.classification_type = "U"
    mock_orbital_elements.element_set_no = 0
    result = SqlAlchemyOrbitalElementsRepository.batch_serialize_orbital_elements(
        [mock_orbital_elements]
    )

    assert len(result) == 1
    assert result[0]["satellite"]["has_current_sat_number"] is True


def test_batch_serialize_orbital_elements_datetime_serialization_error(mocker):
    """Test batch_serialize_orbital_elements with invalid datetime."""
    mock_satellite = mocker.Mock()
    mock_satellite.sat_name = "TEST SAT"
    mock_satellite.sat_number = 12345
    mock_satellite.decay_date = None
    mock_satellite.has_current_sat_number = True

    mock_orbital_elements = mocker.Mock()
    mock_orbital_elements.satellite = mock_satellite
    mock_orbital_elements.epoch.isoformat.side_effect = AttributeError(
        "Invalid datetime"
    )
    mock_orbital_elements.date_collected = datetime.now(timezone.utc)

    with pytest.raises(AttributeError):
        SqlAlchemyOrbitalElementsRepository.batch_serialize_orbital_elements(
            [mock_orbital_elements]
        )
