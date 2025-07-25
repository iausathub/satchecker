# ruff: noqa: S101, E501
import logging
from datetime import datetime, timedelta
from functools import wraps
from time import sleep
from unittest.mock import Mock, patch

import numpy as np
import pytest
import requests
from astropy.coordinates import EarthLocation
from astropy.time import Time

from api import create_app
from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.entrypoints.v1.routes.fov_routes import (
    get_all_satellites_above_horizon,
    get_all_satellites_above_horizon_range,
    get_satellite_passes,
)
from api.services.fov_service import (
    get_satellites_above_horizon,
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MockTLERepository(AbstractTLERepository):
    """Mock TLE repository for testing."""

    def __init__(self, mock_tles=None):
        self.mock_tles = mock_tles or []

    def get_all_active_tles(
        self, active_epoch=None, source="test", return_as_list=False
    ):
        return self.mock_tles

    def get_latest_active_tle_by_sat_id(self, sat_id, active_epoch=None, source="test"):
        for tle in self.mock_tles:
            if tle.satellite.sat_id == sat_id:
                return tle
        return None

    def get_latest_tles_by_sat_ids(self, sat_ids, active_epoch=None, source="test"):
        return [tle for tle in self.mock_tles if tle.satellite.sat_id in sat_ids]

    def _add(self, tle):
        self.mock_tles.append(tle)

    def _get_all_for_date_range_by_satellite_name(
        self, satellite_name, start_date, end_date
    ):
        return [
            tle
            for tle in self.mock_tles
            if (
                tle.satellite.sat_name == satellite_name
                and (start_date is None or start_date <= getattr(tle, "epoch", 0))
                and (end_date is None or getattr(tle, "epoch", 0) <= end_date)
            )
        ]

    def _get_all_for_date_range_by_satellite_number(
        self, satellite_number, start_date, end_date
    ):
        return [
            tle
            for tle in self.mock_tles
            if (
                tle.satellite.sat_number == satellite_number
                and (start_date is None or start_date <= getattr(tle, "epoch", 0))
                and (end_date is None or getattr(tle, "epoch", 0) <= end_date)
            )
        ]

    def _get_closest_by_satellite_name(self, satellite_name, epoch):
        matching_tles = [
            tle for tle in self.mock_tles if tle.satellite.sat_name == satellite_name
        ]
        if not matching_tles:
            return None
        return matching_tles[0]  # Just return the first one for simplicity in testing

    def _get_closest_by_satellite_number(self, satellite_number, epoch):
        matching_tles = [
            tle
            for tle in self.mock_tles
            if tle.satellite.sat_number == satellite_number
        ]
        if not matching_tles:
            return None
        return matching_tles[0]  # Just return the first one for simplicity in testing

    def _get_all_tles_at_epoch(
        self, epoch_date, page, per_page, format, constellation, data_source
    ):
        return self.mock_tles, len(self.mock_tles), "database"

    def _get_adjacent_tles(self, id, id_type, epoch):
        matching_tles = [tle for tle in self.mock_tles if tle.satellite.sat_id == id]
        return matching_tles[:2]  # Return up to 2 adjacent TLEs

    def _get_tles_around_epoch(self, id, id_type, epoch, count_before, count_after):
        matching_tles = [tle for tle in self.mock_tles if tle.satellite.sat_id == id]
        return matching_tles[: (count_before + count_after)]

    def _get_nearest_tle(self, id, id_type, epoch):
        matching_tles = [tle for tle in self.mock_tles if tle.satellite.sat_id == id]
        if not matching_tles:
            return None
        return matching_tles[0]  # Just return the first one for simplicity in testing


@pytest.fixture
def sample_tles():
    """Create multiple sample TLE objects for testing."""
    return _create_sample_tles(5)


@pytest.fixture
def single_sample_tle():
    """Create a single sample TLE object."""
    return _create_sample_tles(1)[0]


# Helper function to create sample TLEs without being a fixture
def _create_sample_tles(num_tles=5):
    """Helper function to create sample TLEs without being a fixture."""
    tles = []

    # Create a fixed set of sample TLEs
    satellites = [
        # ISS
        {
            "sat_id": 25544,
            "sat_name": "ISS (ZARYA)",
            "norad_id": 25544,
            "sat_number": 25544,
            "tle1": "1 25544U 98067A   24023.88563310  .00014265  00000+0  26320-3 0  9990",
            "tle2": "2 25544  51.6422 150.2384 0004789  89.9089  25.8579 15.49640796432702",
        },
        # Starlink-1855
        {
            "sat_id": 47438,
            "sat_name": "STARLINK-1855",
            "norad_id": 47438,
            "sat_number": 47438,
            "tle1": "1 47438U 20101AY  24024.27811800  .00011519  00000+0  11191-2 0  9992",
            "tle2": "2 47438  53.0544 176.8276 0001319  77.9264 282.1858 15.06338255176863",
        },
        # NOAA-18
        {
            "sat_id": 28654,
            "sat_name": "NOAA-18",
            "norad_id": 28654,
            "sat_number": 28654,
            "tle1": "1 28654U 05018A   24024.28778438  .00000195  00000+0  19259-3 0  9992",
            "tle2": "2 28654  99.0134  69.3066 0014148  26.5883 333.6185 14.12925272955782",
        },
        # TERRA
        {
            "sat_id": 25994,
            "sat_name": "TERRA",
            "norad_id": 25994,
            "sat_number": 25994,
            "tle1": "1 25994U 99068A   24024.33767259  .00000121  00000+0  34743-4 0  9992",
            "tle2": "2 25994  98.1714  69.9151 0001293  89.1304 271.0026 14.57157682281275",
        },
        # AQUA
        {
            "sat_id": 27424,
            "sat_name": "AQUA",
            "norad_id": 27424,
            "sat_number": 27424,
            "tle1": "1 27424U 02022A   24024.32708743  .00000147  00000+0  41598-4 0  9996",
            "tle2": "2 27424  98.2021  70.2456 0002481  74.5196 285.6275 14.57116600228939",
        },
    ]

    # Create enough TLEs to match num_tles parameter
    for i in range(min(num_tles, len(satellites))):
        satellite = Mock()
        satellite.sat_id = satellites[i]["sat_id"]
        satellite.sat_name = satellites[i]["sat_name"]
        satellite.norad_id = satellites[i]["norad_id"]
        satellite.sat_number = satellites[i]["sat_number"]

        tle = Mock()
        tle.satellite = satellite
        tle.tle1 = tle.tle_line1 = satellites[i]["tle1"]
        tle.tle2 = tle.tle_line2 = satellites[i]["tle2"]
        tle.source = tle.data_source = "test"
        tle.epoch = Time(datetime.now(), scale="utc").jd

        tles.append(tle)

    return tles


@pytest.fixture
def mock_tle_repository(sample_tles):
    """Create a mock TLE repository with sample TLEs."""
    return MockTLERepository(sample_tles)


@pytest.fixture
def location():
    """Create a sample EarthLocation for testing."""
    return EarthLocation.from_geodetic(lon=-110.9478, lat=32.2333, height=728.0)


@pytest.fixture
def observation_times():
    """Create sample observation times."""
    mid_obs_time = Time(datetime.now(), scale="utc")
    start_time = Time(datetime.now() - timedelta(minutes=30), scale="utc")

    return mid_obs_time, start_time, 60.0  # mid time, start time, duration in minutes


@pytest.fixture
def fov_params():
    """Sample field of view parameters."""
    return {
        "ra": 150.0,  # Right ascension in degrees
        "dec": 20.0,  # Declination in degrees
        "fov_radius": 2.0,  # Field of view radius in degrees
    }


# Benchmark complete functions
@patch("api.services.fov_service.output_utils.fov_data_to_json")
def test_benchmark_get_satellites_above_horizon_complete(
    mock_fov_data_to_json, benchmark, mock_tle_repository, location, observation_times
):
    """Benchmark the complete get_satellites_above_horizon function."""
    mid_obs_time, _, _ = observation_times

    # Mock the fov_data_to_json function to return a simple dictionary
    mock_fov_data_to_json.return_value = {"results": [], "visible_satellites": 0}

    def run_full_function():
        return get_satellites_above_horizon(
            tle_repo=mock_tle_repository,
            location=location,
            julian_dates=[mid_obs_time],
            min_altitude=10.0,
            min_range=0.0,
            max_range=10000.0,
            illuminated_only=False,
            api_source="test",
            api_version="v1",
            constellation=None,
        )

    result = benchmark(run_full_function)
    assert isinstance(result, dict)


# Benchmark component parts


@patch("api.services.fov_service.output_utils.fov_data_to_json")
def test_benchmark_get_satellite_passes_in_fov_setup(
    mock_fov_data_to_json,
    benchmark,
    mock_tle_repository,
    location,
    observation_times,
    fov_params,
):
    """Benchmark the setup part of get_satellite_passes_in_fov."""
    mid_obs_time, start_time, duration = observation_times

    # Mock the fov_data_to_json function to return a simple dictionary
    mock_fov_data_to_json.return_value = {"results": [], "points_in_fov": 0}

    # Define a function that only does the setup part of the function
    def setup_only():
        # This replicates what happens in the beginning of get_satellite_passes_in_fov
        all_tles = mock_tle_repository.get_all_active_tles()
        count = len(all_tles)
        all_results = []
        duration_jd = duration / 1440.0  # Convert minutes to days
        time_step = 1 / 720.0  # 2-minute steps in days

        # Generate observation times
        if mid_obs_time is not None:
            jd_times = np.arange(
                mid_obs_time.jd - duration_jd / 2,
                mid_obs_time.jd + duration_jd / 2,
                time_step,
            )
        else:
            jd_times = np.arange(
                start_time.jd,
                start_time.jd + duration_jd,
                time_step,
            )

        return count, all_results, jd_times

    result = benchmark(setup_only)
    assert len(result) == 3
    assert result[0] > 0  # At least one TLE in the repository
    assert len(result[2]) > 0  # Some Julian dates were created


@patch("api.services.fov_service.output_utils.fov_data_to_json")
def test_benchmark_get_satellites_above_horizon_setup(
    mock_fov_data_to_json, benchmark, mock_tle_repository, location, observation_times
):
    """Benchmark the setup part of get_satellites_above_horizon."""
    mid_obs_time, _, _ = observation_times

    # Mock the fov_data_to_json function to return a simple dictionary
    mock_fov_data_to_json.return_value = {"results": [], "visible_satellites": 0}

    def setup_only():
        # This replicates what happens at the beginning of get_satellites_above_horizon
        time_jd = mid_obs_time
        tles, count, _ = mock_tle_repository._get_all_tles_at_epoch(
            time_jd.to_datetime(), 1, 10000, "zip", None, None
        )
        all_results = []

        return count, all_results

    result = benchmark(setup_only)
    assert len(result) == 2
    assert result[0] > 0  # At least one TLE in the repository


# Add URL response time benchmarks
def noop_decorator(*args, **kwargs):
    """A decorator that does nothing."""

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapped

    return decorator


@pytest.fixture(autouse=True)
def disable_rate_limiting():
    """Disable rate limiting for all tests."""
    # Patch the actual route functions to bypass rate limiting
    with (
        patch(
            "api.entrypoints.v1.routes.fov_routes.get_satellite_passes",
            side_effect=lambda: noop_decorator(get_satellite_passes),
        ),
        patch(
            "api.entrypoints.v1.routes.fov_routes.get_all_satellites_above_horizon",
            side_effect=lambda: noop_decorator(get_all_satellites_above_horizon),
        ),
        patch(
            "api.entrypoints.v1.routes.fov_routes.get_all_satellites_above_horizon_range",
            side_effect=lambda: noop_decorator(get_all_satellites_above_horizon_range),
        ),
    ):
        yield


@pytest.fixture
def test_client():
    """Create a Flask test client."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


# Test case parameters
FOV_TEST_CASES = [
    # By year
    {
        "name": "2025",
        "mid_obs_time_jd": 2460796.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "2024",
        "mid_obs_time_jd": 2460431.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "2023",
        "mid_obs_time_jd": 2460065.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "2022",
        "mid_obs_time_jd": 2459700.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "2021",
        "mid_obs_time_jd": 2459335.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "2020",
        "mid_obs_time_jd": 2458970.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "2019",
        "mid_obs_time_jd": 2458604.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "2015",
        "mid_obs_time_jd": 2457143.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "2010",
        "mid_obs_time_jd": 2455317.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "2000",
        "mid_obs_time_jd": 2451665.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "1980",
        "mid_obs_time_jd": 2444360.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "1960",
        "mid_obs_time_jd": 2437055.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    # By duration
    {
        "name": "duration_30",
        "mid_obs_time_jd": 2460796.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "duration_60",
        "mid_obs_time_jd": 2460796.5,
        "duration": 60,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "duration_180",
        "mid_obs_time_jd": 2460796.5,
        "duration": 180,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "duration_240",
        "mid_obs_time_jd": 2460796.5,
        "duration": 240,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "duration_300",
        "mid_obs_time_jd": 2460796.5,
        "duration": 300,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "duration_600",
        "mid_obs_time_jd": 2460796.5,
        "duration": 600,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    # By radius
    {
        "name": "radius_1",
        "mid_obs_time_jd": 2460796.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 1,
    },
    {
        "name": "radius_2",
        "mid_obs_time_jd": 2460796.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 2,
    },
    {
        "name": "radius_5",
        "mid_obs_time_jd": 2460796.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 5,
    },
    {
        "name": "radius_10",
        "mid_obs_time_jd": 2460796.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 10,
    },
    {
        "name": "radius_20",
        "mid_obs_time_jd": 2460796.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 20,
    },
    {
        "name": "radius_45",
        "mid_obs_time_jd": 2460796.5,
        "duration": 30,
        "ra": 224.048903,
        "dec": 78.778084,
        "fov_radius": 45,
    },
]

HORIZON_TEST_CASES = [
    {
        "name": "2025",
        "julian_date": 2460796.5,
    },
    {
        "name": "2024",
        "julian_date": 2460431.5,
    },
    {
        "name": "2023",
        "julian_date": 2460065.5,
    },
    {
        "name": "2022",
        "julian_date": 2459700.5,
    },
    {
        "name": "2021",
        "julian_date": 2459335.5,
    },
    {
        "name": "2020",
        "julian_date": 2458970.5,
    },
    {
        "name": "2019",
        "julian_date": 2458604.5,
    },
    {
        "name": "2015",
        "julian_date": 2457143.5,
    },
    {
        "name": "2010",
        "julian_date": 2455317.5,
    },
    {
        "name": "2000",
        "julian_date": 2451665.5,
    },
    {
        "name": "1980",
        "julian_date": 2444360.5,
    },
    {
        "name": "1960",
        "julian_date": 2437055.5,
    },
]

# Test location
TEST_LOCATION = {
    "name": "test_location",
    "lat": 33.0,
    "lon": -117.0,
    "height": 100.0,
}


@pytest.fixture
def test_location():
    """Create test location."""
    return EarthLocation.from_geodetic(
        lon=TEST_LOCATION["lon"],
        lat=TEST_LOCATION["lat"],
        height=TEST_LOCATION["height"],
    )


@pytest.mark.parametrize(
    "fov_case",
    FOV_TEST_CASES,
    ids=lambda case: f"FOV_{case['name']}_radius{case['fov_radius']}_duration{case['duration']}",
)
def test_benchmark_fov_endpoint_response_time(
    benchmark, test_client, test_location, fov_case
):
    """Benchmark the response time of the FOV endpoint with different parameters."""

    def make_request():
        logger.debug(f"Making request for FOV case: {fov_case['name']}")
        url = "https://dev.satchecker.cps.iau.noirlab.edu/fov/satellite-passes/"
        params = {
            "latitude": test_location.lat.value,
            "longitude": test_location.lon.value,
            "elevation": test_location.height.value,
            "mid_obs_time_jd": fov_case["mid_obs_time_jd"],
            "duration": fov_case["duration"],
            "ra": fov_case["ra"],
            "dec": fov_case["dec"],
            "fov_radius": fov_case["fov_radius"],
            "skip_cache": "true",
        }
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request parameters: {params}")
        response = requests.get(url, params=params)  # noqa: S113
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        if response.status_code != 200:
            logger.error(f"Response body: {response.text}")
        assert response.status_code == 200
        result = response.json()

        # Log performance metrics
        print(f"\nFOV Test Case: {fov_case['name']}")
        print(
            f"Satellites processed: {result.get('performance_metrics', {}).get('satellites_processed', 0)}"
        )
        print(
            f"Propagation time: {result.get('performance_metrics', {}).get('propagation_time', 0)}s"
        )
        print(f"TLE time: {result.get('performance_metrics', {}).get('tle_time', 0)}s")
        print(
            f"Total time: {result.get('performance_metrics', {}).get('total_time', 0)}s"
        )
        print(
            f"Points in FOV: {result.get('performance_metrics', {}).get('points_in_fov', 0)}"
        )

        return result

    result = benchmark(make_request)
    assert isinstance(result, dict)


@pytest.mark.parametrize(
    "horizon_case", HORIZON_TEST_CASES, ids=lambda case: f"Horizon_{case['name']}"
)
def test_benchmark_horizon_endpoint_response_time(
    benchmark, test_client, test_location, horizon_case
):
    """Benchmark the response time of the horizon endpoint with different parameters."""

    def make_request():
        url = "https://dev.satchecker.cps.iau.noirlab.edu/fov/satellites-above-horizon/"
        params = {
            "latitude": test_location.lat.value,
            "longitude": test_location.lon.value,
            "elevation": test_location.height.value,
            "julian_date": horizon_case["julian_date"],
        }
        response = requests.get(url, params=params)  # noqa: S113
        assert response.status_code == 200
        result = response.json()

        # Log performance metrics
        print(f"\nHorizon Test Case: {horizon_case['name']}")
        print(
            f"Satellites processed: {result.get('performance_metrics', {}).get('satellites_processed', 0)}"
        )
        print(
            f"Total time: {result.get('performance_metrics', {}).get('total_time', 0)}s"
        )
        print(
            f"Visible satellites: {result.get('performance_metrics', {}).get('visible_satellites', 0)}"
        )

        return result

    result = benchmark(make_request)
    sleep(10)
    assert isinstance(result, dict)
