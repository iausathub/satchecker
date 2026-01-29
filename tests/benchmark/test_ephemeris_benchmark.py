# ruff: noqa: S101, E501
import logging

import pytest
import requests
from astropy.coordinates import EarthLocation

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

EPHEMERIS_TEST_CASES = [
    {
        "name": "2025_60min_5min",
        "startjd": 2460428.5,
        "stopjd": 2460428.541667,
        "stepjd": 0.0034722222,
        "catalog": 44748,
    },
    {
        "name": "2025_60min_15min",
        "startjd": 2460428.5,
        "stopjd": 2460428.541667,
        "stepjd": 0.0104166667,
        "catalog": 44748,
    },
    {
        "name": "2025_60min_30min",
        "startjd": 2460428.5,
        "stopjd": 2460428.541667,
        "stepjd": 0.0208333333,
        "catalog": 44748,
    },
    {
        "name": "2025_1day_5min",
        "startjd": 2460428.5,
        "stopjd": 2460429.5,
        "stepjd": 0.0034722222,
        "catalog": 44748,
    },
    {
        "name": "2025_1day_15min",
        "startjd": 2460428.5,
        "stopjd": 2460429.5,
        "stepjd": 0.0104166667,
        "catalog": 44748,
    },
    {
        "name": "2025_1day_30min",
        "startjd": 2460428.5,
        "stopjd": 2460429.5,
        "stepjd": 0.0208333333,
        "catalog": 44748,
    },
    {
        "name": "2024_60min_5min",
        "startjd": 2460063.5,
        "stopjd": 2460063.541667,
        "stepjd": 0.0034722222,
        "catalog": 44748,
    },
    {
        "name": "2024_60min_15min",
        "startjd": 2460063.5,
        "stopjd": 2460063.541667,
        "stepjd": 0.0104166667,
        "catalog": 44748,
    },
    {
        "name": "2024_60min_30min",
        "startjd": 2460063.5,
        "stopjd": 2460063.541667,
        "stepjd": 0.0208333333,
        "catalog": 44748,
    },
    {
        "name": "2024_1day_5min",
        "startjd": 2460063.5,
        "stopjd": 2460064.5,
        "stepjd": 0.0034722222,
        "catalog": 44748,
    },
    {
        "name": "2024_1day_15min",
        "startjd": 2460063.5,
        "stopjd": 2460064.5,
        "stepjd": 0.0104166667,
        "catalog": 44748,
    },
    {
        "name": "2024_1day_30min",
        "startjd": 2460063.5,
        "stopjd": 2460064.5,
        "stepjd": 0.0208333333,
        "catalog": 44748,
        "latitude": 33,
        "longitude": -117,
        "elevation": 100,
    },
    {
        "name": "2020_60min_5min",
        "startjd": 2458963.5,
        "stopjd": 2458963.541667,
        "stepjd": 0.0034722222,
        "catalog": 44748,
    },
    {
        "name": "2020_60min_15min",
        "startjd": 2458963.5,
        "stopjd": 2458963.541667,
        "stepjd": 0.0104166667,
        "catalog": 44748,
    },
    {
        "name": "2020_60min_30min",
        "startjd": 2458963.5,
        "stopjd": 2458963.541667,
        "stepjd": 0.0208333333,
        "catalog": 44748,
        "latitude": 33,
        "longitude": -117,
        "elevation": 100,
    },
    {
        "name": "2020_1day_5min",
        "startjd": 2458963.5,
        "stopjd": 2458964.5,
        "stepjd": 0.0034722222,
        "catalog": 44748,
    },
    {
        "name": "2020_1day_15min",
        "startjd": 2458963.5,
        "stopjd": 2458964.5,
        "stepjd": 0.0104166667,
        "catalog": 44748,
    },
    {
        "name": "2020_1day_30min",
        "startjd": 2458963.5,
        "stopjd": 2458964.5,
        "stepjd": 0.0208333333,
        "catalog": 44748,
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
    "ephemeris_case", EPHEMERIS_TEST_CASES, ids=lambda case: f"EPHEMERIS_{case['name']}"
)
def test_benchmark_ephemeris_endpoint_response_time(
    benchmark, test_location, ephemeris_case
):
    """Benchmark the response time of the EPHEMERIS endpoint with different parameters."""

    def make_request():
        logger.debug(f"Making request for EPHEMERIS case: {ephemeris_case['name']}")
        url = "https://dev.satchecker.cps.iau.noirlab.edu/ephemeris/catalog-number-jdstep/"
        params = {
            "latitude": test_location.lat.value,
            "longitude": test_location.lon.value,
            "elevation": test_location.height.value,
            "catalog": ephemeris_case["catalog"],
            "startjd": ephemeris_case["startjd"],
            "stopjd": ephemeris_case["stopjd"],
            "stepjd": ephemeris_case["stepjd"],
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

        return result

    result = benchmark(make_request)
    assert isinstance(result, dict)
