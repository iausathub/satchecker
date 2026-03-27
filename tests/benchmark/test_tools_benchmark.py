# ruff: noqa: S101, E501
import logging

import requests

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_benchmark_tools_get_active_satellites_response_time(benchmark):
    """Benchmark the response time of the get-active-satellites endpoint."""

    def make_request():
        logger.debug("Making request for get-active-satellites")
        url = "https://satchecker.cps.iau.org/tools/get-active-satellites/"
        logger.debug(f"Request URL: {url}")
        response = requests.get(url)  # noqa: S113
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        if response.status_code != 200:
            logger.error(f"Response body: {response.text}")
        assert response.status_code == 200
        result = response.json()

        return result

    result = benchmark(make_request)
    assert isinstance(result, dict)


def test_benchmark_tools_get_tle_data_response_time(benchmark):
    """Benchmark the response time of the get-tle-data endpoint."""

    def make_request():
        logger.debug("Making request for get-tle-data")
        url = "https://satchecker.cps.iau.org/tools/get-tle-data/"
        params = {
            "id": "25544",
            "id_type": "catalog",
            "start_date_jd": "2460425",
            "end_date_jd": "2460500",
        }
        logger.debug(f"Request URL: {url}")
        response = requests.get(url, params=params)  # noqa: S113
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        if response.status_code != 200:
            logger.error(f"Response body: {response.text}")
        assert response.status_code == 200
        result = response.json()

        return result

    result = benchmark(make_request)
    assert isinstance(result, list)


def test_benchmark_tools_tles_at_epoch_response_time(benchmark):
    """Benchmark the response time of the tles-at-epoch endpoint."""

    def make_request():
        logger.debug("Making request for tles-at-epoch")
        url = "https://satchecker.cps.iau.org/tools/tles-at-epoch/"
        params = {
            "epoch": "2459448.5",
            "page": 1,
            "per_page": 200,
        }
        logger.debug(f"Request URL: {url}")
        response = requests.get(url, params=params)  # noqa: S113
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        if response.status_code != 200:
            logger.error(f"Response body: {response.text}")
        assert response.status_code == 200
        result = response.json()

        return result

    result = benchmark(make_request)
    assert isinstance(result, list)
