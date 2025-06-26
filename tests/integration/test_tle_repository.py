# ruff: noqa: S101

import time
from datetime import datetime, timedelta, timezone

from src.api.adapters.database_orm import TLEDb
from src.api.adapters.repositories.satellite_repository import (
    SqlAlchemySatelliteRepository,
)
from src.api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from tests.factories import SatelliteFactory, TLEFactory


def test_add_tle(session, services_available):
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = SqlAlchemyTLERepository._to_domain(session.query(TLEDb).one())
    assert repo_tle.tle_line1 == tle.tle_line1


def test_add_tle_existing_satellite(session, services_available):
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


def test_get_tle_by_satellite_number(session, services_available):
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_number(
        tle.satellite.sat_number, tle.epoch, tle.data_source
    )
    assert repo_tle.tle_line1 == tle.tle_line1


def test_get_tle_by_satellite_name(session, services_available):
    tle = TLEFactory()
    tle_repository = SqlAlchemyTLERepository(session)

    tle_repository.add(tle)
    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_name(
        tle.satellite.sat_name, tle.epoch, tle.data_source
    )
    assert repo_tle.tle_line1 == tle.tle_line1


def test_get_tle_by_satellite_number_no_match(session, services_available):
    tle_repository = SqlAlchemyTLERepository(session)

    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_number(
        "12345", "2021-01-01", "data_source"
    )
    assert repo_tle is None


def test_get_tle_by_satellite_name_no_match(session, services_available):
    tle_repository = SqlAlchemyTLERepository(session)

    session.commit()

    repo_tle = tle_repository.get_closest_by_satellite_name(
        "NO_MATCH", "2021-01-01", "data_source"
    )
    assert repo_tle is None


def test_get_all_for_date_range_by_satellite_number(session, services_available):

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


def test_get_all_for_date_range_by_satellite_name(session, services_available):
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


def test_get_all_for_date_range_by_satellite_number_no_match(
    session, services_available
):
    tle_repository = SqlAlchemyTLERepository(session)

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_number(
        "12345", None, None
    )
    assert repo_tles == []


def test_get_all_for_date_range_by_satellite_name_no_match(session, services_available):
    tle_repository = SqlAlchemyTLERepository(session)

    repo_tles = tle_repository.get_all_for_date_range_by_satellite_name(
        "NO_MATCH", None, None
    )
    assert repo_tles == []


def test_get_all_for_date_range_with_dates(session, services_available):
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


def test_get_norad_ids_from_satellite_name(session, services_available):
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


def test_get_satellite_names_from_norad_id(
    session,
):
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


def test_get_satellite_names_from_norad_id_no_match(session, services_available):
    sat_repository = SqlAlchemySatelliteRepository(session)

    results = sat_repository.get_satellite_names_from_norad_id("12345")
    assert results == []

    satellite = SatelliteFactory(sat_number="25544")
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_satellite_names_from_norad_id("12345")
    assert results == []


def test_get_norad_ids_from_satellite_name_no_match(session, services_available):
    sat_repository = SqlAlchemySatelliteRepository(session)

    results = sat_repository.get_norad_ids_from_satellite_name("NO_MATCH")
    assert results == []

    satellite = SatelliteFactory(sat_name="ISS")
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_norad_ids_from_satellite_name("NO_MATCH")
    assert results == []


def test_get_satellite_data_by_id(session, services_available):
    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_satellite_data_by_id(satellite.sat_number)
    assert results.sat_name == satellite.sat_name


def test_get_satellite_data_by_id_no_match(session, services_available):
    sat_repository = SqlAlchemySatelliteRepository(session)
    session.commit()

    results = sat_repository.get_satellite_data_by_id("12345")
    assert results is None


def test_get_satellite_data_by_name(session, services_available):
    satellite = SatelliteFactory()
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    session.commit()

    results = sat_repository.get_satellite_data_by_name(satellite.sat_name)
    assert results.sat_number == satellite.sat_number


def test_get_satellite_data_by_name_no_match(session, services_available):
    sat_repository = SqlAlchemySatelliteRepository(session)
    session.commit()

    results = sat_repository.get_satellite_data_by_name("NO_MATCH")
    assert results is None


def test_get_all_tles_at_epoch(session, services_available):
    tle_repository = SqlAlchemyTLERepository(session)

    satellite = SatelliteFactory(decay_date=None)
    satellite_2 = SatelliteFactory(decay_date=None)
    satellite_3 = SatelliteFactory(decay_date=None)
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)

    tle_1 = TLEFactory(epoch=datetime.now(timezone.utc), satellite=satellite)
    tle_2 = TLEFactory(
        epoch=datetime.now(timezone.utc) - timedelta(days=30), satellite=satellite_2
    )
    tle_repository.add(tle_1)
    tle_repository.add(tle_2)
    session.commit()

    results = tle_repository.get_all_tles_at_epoch(
        datetime.now(timezone.utc), 1, 10, "zip"
    )
    assert len(results[0]) == 1

    tle_3 = TLEFactory(
        epoch=datetime.now(timezone.utc) - timedelta(days=12), satellite=satellite_3
    )
    tle_repository.add(tle_3)
    session.commit()

    results = tle_repository.get_all_tles_at_epoch(
        datetime.now(timezone.utc), 1, 10, "zip"
    )
    assert len(results[0]) == 2


def test_get_adjacent_tles(session, services_available):
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


def test_get_adjacent_tles_no_after(session, services_available):
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


def test_get_adjacent_tles_no_before(session, services_available):
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


def test_get_adjacent_tles_multiple_satellites(session, services_available):
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


def test_get_tles_around_epoch(session, services_available):
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


def test_get_nearest_tle(session, services_available):
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


def test_get_all_tles_at_epoch_cache(session, app, services_available):
    tle_repository = SqlAlchemyTLERepository(session)

    # Empty cache, no TLEs added yet
    results = tle_repository.get_all_tles_at_epoch(
        datetime.now(timezone.utc), 1, 10, "zip"
    )
    assert len(results[0]) == 0

    # Add TLEs to repository
    satellite = SatelliteFactory(
        sat_name="ISS",
        decay_date=None,
        launch_date=datetime.now(timezone.utc) - timedelta(days=1000),
        has_current_sat_number=True,
    )
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    session.commit()

    tle = TLEFactory(epoch=datetime.now(timezone.utc), satellite=satellite)
    tle_repository.add(tle)
    tle2 = TLEFactory(
        epoch=datetime.now(timezone.utc) - timedelta(days=1), satellite=satellite
    )
    tle_repository.add(tle2)
    session.commit()

    # Import and use cache functions directly
    from api.services.cache_service import (
        RECENT_TLES_CACHE_KEY,
        batch_serialize_tles,
        set_cached_data,
    )

    # Explicitly initialize the cache with our test data for consistent testing
    with app.app_context():
        print("DEBUG - Manually initializing Redis cache with test data")
        cache_data = {
            "tles": batch_serialize_tles([tle]),
            "total_count": 1,
            "cached_at": datetime.now(timezone.utc).isoformat(),
        }
        set_cached_data(RECENT_TLES_CACHE_KEY, cache_data)

    # Check that TLEs are returned from cache
    try:
        results = tle_repository.get_all_tles_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        assert len(results[0]) == 1
        assert results[2] == "cache"
    except Exception as e:
        print(e)
        raise e

    # Check that TLEs are returned from database for an older date
    results = tle_repository.get_all_tles_at_epoch(
        datetime.now(timezone.utc) - timedelta(days=0.5), 1, 10, "zip"
    )
    assert len(results[0]) == 1
    assert results[2] == "database"

    # Check that TLEs are returned from cache for a future date
    results = tle_repository.get_all_tles_at_epoch(
        datetime.now(timezone.utc) + timedelta(days=1), 1, 10, "zip"
    )
    assert len(results[0]) == 1
    assert results[2] == "cache"

    # temporarily change cache storage time
    with app.app_context():
        tle_repository.cache_ttl = 5

        cache_data = {
            "tles": batch_serialize_tles([tle]),
            "total_count": 1,
            "cached_at": datetime.now(timezone.utc).isoformat(),
        }
        success = set_cached_data(RECENT_TLES_CACHE_KEY, cache_data, ttl=5)
        assert success

        results = tle_repository.get_all_tles_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        assert results[2] == "cache"

        # wait for cache to expire
        time.sleep(6)
        results = tle_repository.get_all_tles_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        assert results[2] == "database"

    # test that the TLEs load from the database if there are issues with the cache
    with app.app_context():
        cache_results = tle_repository.get_all_tles_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        tle_repository.cache_enabled = False

        db_results = tle_repository.get_all_tles_at_epoch(
            datetime.now(timezone.utc), 1, 10, "zip"
        )
        assert db_results[2] == "database"
        assert cache_results[0] == db_results[0]


def test_get_all_tles_at_epoch_with_constellation(session, services_available):
    """Test getting TLEs filtered by constellation."""
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

    # Create TLEs for both satellites with the same epoch
    epoch = datetime(2024, 6, 1, tzinfo=timezone.utc)
    starlink_tle = TLEFactory(satellite=starlink_sat, epoch=epoch)
    oneweb_tle = TLEFactory(satellite=oneweb_sat, epoch=epoch)

    tle_repository = SqlAlchemyTLERepository(session)
    tle_repository.add(starlink_tle)
    tle_repository.add(oneweb_tle)
    session.commit()

    # Test filtering by starlink constellation
    starlink_tles, count, _ = tle_repository.get_all_tles_at_epoch(
        epoch, 1, 10000, "zip", "starlink"
    )
    assert len(starlink_tles) == 1
    assert starlink_tles[0].satellite.constellation == "starlink"

    # Test filtering by oneweb constellation
    oneweb_tles, count, _ = tle_repository.get_all_tles_at_epoch(
        epoch, 1, 10000, "zip", "oneweb"
    )
    assert len(oneweb_tles) == 1
    assert oneweb_tles[0].satellite.constellation == "oneweb"

    # Test with no constellation filter
    all_tles, count, _ = tle_repository.get_all_tles_at_epoch(
        epoch, 1, 10000, "zip", None
    )
    assert len(all_tles) == 2


def test_get_all_tles_at_epoch_experimental_with_constellation(
    session, services_available
):
    """Test getting TLEs filtered by constellation using experimental method."""
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

    # Create TLEs for both satellites with the same epoch
    epoch = datetime(2024, 6, 1, tzinfo=timezone.utc)  # Fixed epoch date
    starlink_tle = TLEFactory(satellite=starlink_sat, epoch=epoch)
    oneweb_tle = TLEFactory(satellite=oneweb_sat, epoch=epoch)

    tle_repository = SqlAlchemyTLERepository(session)
    tle_repository.add(starlink_tle)
    tle_repository.add(oneweb_tle)
    session.commit()

    # Test filtering by starlink constellation
    starlink_tles, count, _ = tle_repository._get_all_tles_at_epoch_experimental(
        epoch, 1, 10000, "zip", "starlink"
    )
    assert len(starlink_tles) == 1
    assert starlink_tles[0].satellite.constellation == "starlink"

    # Test filtering by oneweb constellation
    oneweb_tles, count, _ = tle_repository._get_all_tles_at_epoch_experimental(
        epoch, 1, 10000, "zip", "oneweb"
    )
    assert len(oneweb_tles) == 1
    assert oneweb_tles[0].satellite.constellation == "oneweb"

    # Test with no constellation filter
    all_tles, count, _ = tle_repository._get_all_tles_at_epoch_experimental(
        epoch, 1, 10000, "zip", None
    )
    assert len(all_tles) == 2


def test_get_all_tles_at_epoch_experimental_with_data_source(
    session, services_available
):
    """Test getting TLEs filtered by data source using experimental method."""
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
    spacetrack_tle = TLEFactory(
        satellite=satellite, epoch=epoch, data_source="spacetrack"
    )
    celestrak_tle = TLEFactory(
        satellite=satellite_2, epoch=epoch, data_source="celestrak"
    )

    tle_repository = SqlAlchemyTLERepository(session)
    tle_repository.add(spacetrack_tle)
    tle_repository.add(celestrak_tle)
    session.commit()

    # Test filtering by spacetrack data source
    spacetrack_tles, count, _ = tle_repository._get_all_tles_at_epoch(
        epoch, 1, 10000, "zip", data_source="spacetrack"
    )
    assert len(spacetrack_tles) == 1
    assert spacetrack_tles[0].data_source == "spacetrack"

    # Test filtering by celestrak data source
    celestrak_tles, count, _ = tle_repository._get_all_tles_at_epoch(
        epoch, 1, 10000, "zip", data_source="celestrak"
    )
    assert len(celestrak_tles) == 1
    assert celestrak_tles[0].data_source == "celestrak"

    # Test filtering by any data source
    all_tles, count, _ = tle_repository._get_all_tles_at_epoch(
        epoch, 1, 10000, "zip", data_source="any"
    )
    assert len(all_tles) == 2
    assert all_tles[0].data_source == "spacetrack"
    assert all_tles[1].data_source == "celestrak"


def test_get_all_tles_at_epoch_with_data_source(session, services_available):
    """Test getting TLEs filtered by data source using experimental method."""
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
    spacetrack_tle = TLEFactory(
        satellite=satellite, epoch=epoch, data_source="spacetrack"
    )
    celestrak_tle = TLEFactory(
        satellite=satellite_2, epoch=epoch, data_source="celestrak"
    )

    tle_repository = SqlAlchemyTLERepository(session)
    tle_repository.add(spacetrack_tle)
    tle_repository.add(celestrak_tle)
    session.commit()

    # Test filtering by spacetrack data source
    spacetrack_tles, count, _ = tle_repository._get_all_tles_at_epoch(
        epoch, 1, 10000, "zip", data_source="spacetrack"
    )
    assert len(spacetrack_tles) == 1
    assert spacetrack_tles[0].data_source == "spacetrack"

    # Test filtering by celestrak data source
    celestrak_tles, count, _ = tle_repository._get_all_tles_at_epoch(
        epoch, 1, 10000, "zip", data_source="celestrak"
    )
    assert len(celestrak_tles) == 1
    assert celestrak_tles[0].data_source == "celestrak"

    # Test filtering by any data source
    all_tles, count, _ = tle_repository._get_all_tles_at_epoch(
        epoch, 1, 10000, "zip", data_source="any"
    )
    assert len(all_tles) == 2
    assert all_tles[0].data_source == "spacetrack"
    assert all_tles[1].data_source == "celestrak"
