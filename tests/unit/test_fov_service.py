# ruff: noqa: S101
import logging

from astropy.time import Time
from tests.conftest import FakeTLERepository
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.services.fov_service import (
    get_satellite_passes_in_fov,
    get_satellites_above_horizon,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_satellite_in_fov(test_location, test_time):
    """Test when a satellite passes through FOV"""
    # Set up known satellite TLE that will pass through a specific FOV
    satellite = SatelliteFactory(
        sat_name="FENGYUN 1C DEB",
        sat_number=31746,
        decay_date=None,
        has_current_sat_number=True,
    )

    tle = TLEFactory(
        satellite=satellite,
        tle_line1="1 31746U 99025CEV 24275.73908890  .00035853  00000-0  86550-2 0  9990",  # noqa: E501
        tle_line2="2 31746  98.5847  13.2387 0030132 143.9377 216.3858 14.52723026906685",  # noqa: E501
    )

    tle_repo = FakeTLERepository([tle])

    result = get_satellite_passes_in_fov(
        tle_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=24.797270,
        dec=75.774139,
        fov_radius=2.0,
        group_by="satellite",
        api_source="test",
        api_version="1.0",
    )

    assert len(result["data"]["satellites"]) == 1
    assert result["data"]["total_position_results"] == 18

    result = get_satellite_passes_in_fov(
        tle_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=24.797270,
        dec=75.774139,
        fov_radius=2.0,
        group_by="time",
        api_source="test",
        api_version="1.0",
    )

    assert result["count"] == 18
    assert result["data"][0]["norad_id"] == 31746


def test_satellite_outside_fov(test_location, test_time):
    """Test when satellite never enters FOV"""
    # Set up with FOV pointing away from orbit - RA changed to 48.797270

    satellite = SatelliteFactory(
        sat_name="FENGYUN 1C DEB",
        sat_number=31746,
        decay_date=None,
        has_current_sat_number=True,
    )

    tle = TLEFactory(
        satellite=satellite,
        tle_line1="1 31746U 99025CEV 24275.73908890  .00035853  00000-0  86550-2 0  9990",  # noqa: E501
        tle_line2="2 31746  98.5847  13.2387 0030132 143.9377 216.3858 14.52723026906685",  # noqa: E501
    )

    tle_repo = FakeTLERepository([tle])

    result = get_satellite_passes_in_fov(
        tle_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=48.797270,
        dec=75.774139,
        fov_radius=2.0,
        group_by="satellite",
        api_source="test",
        api_version="1.0",
    )

    assert len(result["data"]["satellites"]) == 0
    assert result["data"]["total_position_results"] == 0


def test_empty_tle_list(test_location, test_time):
    """Test behavior with no TLEs available"""
    tle_repo = FakeTLERepository([])

    result = get_satellite_passes_in_fov(
        tle_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=48.797270,
        dec=75.774139,
        fov_radius=2.0,
        group_by="satellite",
        api_source="test",
        api_version="1.0",
    )

    assert len(result["data"]["satellites"]) == 0
    assert result["data"]["total_position_results"] == 0


def test_satellites_above_horizon(test_location, test_time):
    # Test for satellite above horizon
    satellite = SatelliteFactory(
        sat_name="FENGYUN 1C DEB",
        sat_number=31746,
        decay_date=None,
        has_current_sat_number=True,
    )

    tle = TLEFactory(
        satellite=satellite,
        tle_line1="1 31746U 99025CEV 24275.73908890  .00035853  00000-0  86550-2 0  9990",  # noqa: E501
        tle_line2="2 31746  98.5847  13.2387 0030132 143.9377 216.3858 14.52723026906685",  # noqa: E501
    )

    tle_repo = FakeTLERepository([tle])

    result = get_satellites_above_horizon(
        tle_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=0,
        max_range=1500000,
    )

    assert len(result["data"]) == 1
    assert result["data"][0]["altitude"] > 0

    # Test for satellite above horizon but below minimum altitude
    result = get_satellites_above_horizon(
        tle_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=30,
        min_range=0,
        max_range=1500000,
    )

    assert len(result["data"]) == 0

    # Test for satellite below horizon
    # Using a different time - 3 hours earlier
    different_time = Time("2024-10-01 15:19:13")
    result = get_satellites_above_horizon(
        tle_repo,
        location=test_location,
        julian_dates=[different_time],
        min_altitude=0,
        min_range=0,
        max_range=1500000,
    )

    assert len(result["data"]) == 0

    # range is 1292
    result = get_satellites_above_horizon(
        tle_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=0,
        max_range=1000,
    )

    assert len(result["data"]) == 0

    result = get_satellites_above_horizon(
        tle_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=1000,
        max_range=1500000,
    )

    assert len(result["data"]) == 1

    result = get_satellites_above_horizon(
        tle_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=1500,
        max_range=1500000,
    )

    assert len(result["data"]) == 0


def test_fov_caching_cycle(mocker, test_location, test_time):
    """Test the complete caching cycle: miss, compute, store, then hit."""
    # Create a simple dictionary to act as our cache storage
    fake_cache = {}

    def mock_get(key):
        return fake_cache.get(key)

    def mock_setex(key, expiry, value):
        fake_cache[key] = value
        return True

    mock_redis_client = mocker.patch("api.services.fov_service.redis_client")
    mock_redis_client.get.side_effect = mock_get
    mock_redis_client.setex.side_effect = mock_setex

    tle_repo = FakeTLERepository([])

    # First call - should compute and cache (cache miss)
    first_result = get_satellite_passes_in_fov(
        tle_repo,
        test_location,
        None,
        test_time,
        3600,
        100.0,
        -20.0,
        10.0,
        "time",
        "test",
        "v1",
    )

    # Verify result was computed and cached
    assert len(fake_cache) == 1  # Something was stored in cache
    assert mock_redis_client.get.call_count == 1
    assert mock_redis_client.setex.call_count == 1
    assert "from_cache" not in first_result["performance"]

    # Get the cache key for later verification
    cache_key = mock_redis_client.get.call_args[0][0]

    # Second call with same parameters - should use cache (cache hit)
    mock_redis_client.reset_mock()  # Reset call counts

    second_result = get_satellite_passes_in_fov(
        tle_repo,
        test_location,
        None,
        test_time,
        3600,
        100.0,
        -20.0,
        10.0,
        "time",
        "test",
        "v1",
    )

    # Verify cache was used
    assert mock_redis_client.get.call_count == 1
    assert mock_redis_client.setex.call_count == 0  # No new caching
    assert second_result["performance"]["from_cache"] is True

    # Results should match
    assert second_result["data"] == first_result["data"]

    # Same cache key should be used
    assert mock_redis_client.get.call_args[0][0] == cache_key


def test_fov_cache_key_consistency(mocker, test_location, test_time):
    """Test that the same parameters generate the same cache key."""
    # Use a set to collect and compare cache keys
    cache_keys = set()

    mock_redis_client = mocker.patch("api.services.fov_service.redis_client")
    mock_redis_client.get.return_value = None

    tle_repo = FakeTLERepository([])

    # Make multiple identical calls and collect cache keys
    for _ in range(3):
        get_satellite_passes_in_fov(
            tle_repo,
            test_location,
            None,
            test_time,
            3600,
            100.0,
            -20.0,
            10.0,
            "time",
            "test",
            "v1",
        )
        cache_keys.add(mock_redis_client.get.call_args[0][0])
        mock_redis_client.reset_mock()

    # If all keys are identical, the set will have only one element
    assert len(cache_keys) == 1


def test_fov_different_cache_keys(mocker, test_location, test_time):
    """Test that different parameters generate different cache keys."""
    mock_redis_client = mocker.patch("api.services.fov_service.redis_client")
    mock_redis_client.get.return_value = None

    tle_repo = FakeTLERepository([])

    # Parameter variations to test
    param_variations = [
        {"duration": 1800},  # Different duration
        {"ra": 101.0},  # Different RA
        {"dec": -21.0},  # Different DEC
        {"fov_radius": 5.0},  # Different FOV radius
        {"group_by": "satellite"},  # Different grouping
    ]

    # Collect all generated cache keys
    cache_keys = set()

    # First call with base parameters
    get_satellite_passes_in_fov(
        tle_repo,
        test_location,
        None,
        test_time,
        3600,
        100.0,
        -20.0,
        10.0,
        "time",
        "test",
        "v1",
    )
    cache_keys.add(mock_redis_client.get.call_args[0][0])
    mock_redis_client.reset_mock()

    # Try each variation
    for variation in param_variations:
        # Start with base parameters
        params = {
            "tle_repo": tle_repo,
            "location": test_location,
            "start_time_jd": None,
            "mid_obs_time_jd": test_time,
            "duration": 3600,
            "ra": 100.0,
            "dec": -20.0,
            "fov_radius": 10.0,
            "group_by": "time",
            "api_source": "test",
            "api_version": "v1",
        }

        # Apply the variation
        params.update(variation)

        # Make the call
        get_satellite_passes_in_fov(**params)
        cache_keys.add(mock_redis_client.get.call_args[0][0])
        mock_redis_client.reset_mock()

    # Every variation should generate a unique key
    assert len(cache_keys) == len(param_variations) + 1
