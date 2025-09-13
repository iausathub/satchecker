#!/usr/bin/env python3
"""
This is meant to be run manually to validate the actual results of the
satellite passes and satellites above horizon endpoints between dev and production.

Use this when changes are made to the
"""

import sys
import time
from urllib.parse import urlencode

import requests

DEV_URL = "https://dev.satchecker.cps.iau.noirlab.edu"
PROD_URL = "https://satchecker.cps.iau.org"
TIMEOUT = 180


def make_request(endpoint, params):
    """Make requests to both servers and return data."""
    dev_url = f"{DEV_URL}{endpoint}?{urlencode(params)}"
    prod_url = f"{PROD_URL}{endpoint}?{urlencode(params)}"

    print(f"  Dev: {dev_url}")
    print(f"  Prod: {prod_url}")

    try:
        dev_resp = requests.get(dev_url, timeout=TIMEOUT)
        prod_resp = requests.get(prod_url, timeout=TIMEOUT)

        if dev_resp.status_code != 200:
            return None, f"Dev error: {dev_resp.status_code}"
        if prod_resp.status_code != 200:
            return None, f"Prod error: {prod_resp.status_code}"

        return dev_resp.json(), prod_resp.json()
    except Exception as e:
        return None, f"Request error: {e}"


def compare_responses(dev_data, prod_data, test_name):
    """Compare two JSON responses and report meaningful differences."""
    errors = []

    # Check basic counts first
    for key in ["total_satellites", "total_position_results", "count"]:
        if key in dev_data and key in prod_data:
            if dev_data[key] != prod_data[key]:
                errors.append(f"{key}: dev={dev_data[key]}, prod={prod_data[key]}")

    # Check metadata
    for key in ["source", "version"]:
        if key in dev_data and key in prod_data:
            if dev_data[key] != prod_data[key]:
                errors.append(f"{key}: dev={dev_data[key]}, prod={prod_data[key]}")

    # Check data structure - handle both dict and list formats
    if "data" in dev_data and "data" in prod_data:
        dev_data_content = dev_data["data"]
        prod_data_content = prod_data["data"]

        # If data is a dictionary (satellite-passes format)
        if isinstance(dev_data_content, dict) and isinstance(prod_data_content, dict):
            dev_satellites = dev_data_content.get("satellites", {})
            prod_satellites = prod_data_content.get("satellites", {})

            if len(dev_satellites) != len(prod_satellites):
                errors.append(
                    f"Satellite count: dev={len(dev_satellites)}, "
                    f"prod={len(prod_satellites)}"
                )

            # Check satellite names match
            dev_names = set(dev_satellites.keys())
            prod_names = set(prod_satellites.keys())
            if dev_names != prod_names:
                missing_prod = dev_names - prod_names
                missing_dev = prod_names - dev_names
                if missing_prod:
                    errors.append(
                        f"Missing in prod: {list(missing_prod)[:5]}..."
                    )  # Show first 5
                if missing_dev:
                    errors.append(f"Missing in dev: {list(missing_dev)[:5]}...")

        # If data is a list (satellites-above-horizon format)
        elif isinstance(dev_data_content, list) and isinstance(prod_data_content, list):
            if len(dev_data_content) != len(prod_data_content):
                errors.append(
                    f"Data array length: dev={len(dev_data_content)}, "
                    f"prod={len(prod_data_content)}"
                )

    if errors:
        print(f"{test_name} FAILED:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print(f"{test_name} PASSED")
        return True


def run_test(endpoint, params, test_name):
    """Run a single test."""
    print(f"\n{'=================================================='}")
    print(f"Testing: {test_name}")
    print(f"{'=================================================='}")

    dev_data, prod_data = make_request(endpoint, params)
    if dev_data is None:
        print(f"{test_name} FAILED: {prod_data}")
        return False

    return compare_responses(dev_data, prod_data, test_name)


def main():
    """Run all validation tests."""
    print("Dev vs Production FOV Validation")

    # All test cases from original script
    tests = [
        # Satellite passes tests
        (
            "/fov/satellite-passes/",
            {
                "site": "rubin",
                "duration": 60.0,
                "ra": 15.0,
                "dec": 30.0,
                "fov_radius": 0.5,
                "mid_obs_time_jd": 2460931.191285,
                "group_by": "satellite",
            },
            "Basic satellite passes - Rubin Observatory, group by satellite",
        ),
        (
            "/fov/satellite-passes/",
            {
                "latitude": 32.0,
                "longitude": -110.0,
                "elevation": 150.0,
                "duration": 30.0,
                "ra": 224.048903,
                "dec": 78.778084,
                "fov_radius": 10.0,
                "mid_obs_time_jd": 2460931.191285,
                "group_by": "time",
            },
            "Satellite passes with coordinates - Large FOV, group by time",
        ),
        (
            "/fov/satellite-passes/",
            {
                "site": "rubin",
                "duration": 10.0,
                "ra": 0.0,
                "dec": 0.0,
                "fov_radius": 1.0,
                "mid_obs_time_jd": 2460931.191285,
                "constellation": "starlink",
                "illuminated_only": True,
            },
            "Satellite passes - Starlink constellation only, illuminated",
        ),
        (
            "/fov/satellite-passes/",
            {
                "latitude": 48.8566,
                "longitude": 2.3522,
                "elevation": 35.0,
                "duration": 30.0,
                "ra": 180.0,
                "dec": 45.0,
                "fov_radius": 0.1,
                "mid_obs_time_jd": 2460931.191285,
                "include_tles": True,
                "skip_cache": True,
            },
            "Satellite passes - Small FOV, include TLEs",
        ),
        (
            "/fov/satellite-passes/",
            {
                "site": "rubin",
                "duration": 90.0,
                "ra": 270.0,
                "dec": -30.0,
                "fov_radius": 0.8,
                "mid_obs_time_jd": 2460931.191285,
                "data_source": "celestrak",
            },
            "Satellite passes - Celestrak data source",
        ),
        # Satellites above horizon tests
        (
            "/fov/satellites-above-horizon/",
            {"site": "rubin", "julian_date": 2460931.191285},
            "Basic satellites above horizon - Rubin Observatory",
        ),
        (
            "/fov/satellites-above-horizon/",
            {
                "latitude": 32.0,
                "longitude": -110.0,
                "elevation": 150.0,
                "julian_date": 2460931.191285,
                "min_altitude": 15.0,
            },
            "Satellites above horizon with coordinates, min altitude",
        ),
        (
            "/fov/satellites-above-horizon/",
            {
                "site": "rubin",
                "julian_date": 2460931.191285,
                "constellation": "starlink",
                "illuminated_only": True,
                "min_range": 300.0,
                "max_range": 500.0,
            },
            "Satellites above horizon - Starlink only, illuminated",
        ),
        (
            "/fov/satellites-above-horizon/",
            {
                "latitude": 48.8566,
                "longitude": 2.3522,
                "elevation": 35.0,
                "julian_date": 2460931.191285,
                "min_altitude": 30.0,
            },
            "Satellites above horizon - Altitude filter",
        ),
        # Additional satellite passes test cases
        (
            "/fov/satellite-passes/",
            {
                "site": "rubin",
                "duration": 5.0,
                "ra": 0.0,
                "dec": 90.0,
                "fov_radius": 0.05,
                "mid_obs_time_jd": 2460931.191285,
                "min_altitude": 45.0,
            },
            "Satellite passes - Very small FOV, high altitude",
        ),
        (
            "/fov/satellite-passes/",
            {
                "site": "rubin",
                "duration": 30.0,
                "ra": 270.0,
                "dec": 0.0,
                "fov_radius": 1.5,
                "mid_obs_time_jd": 2460931.191285,
                "max_altitude": 20.0,
                "illuminated_only": False,
            },
            "Satellite passes - Low altitude filter, all satellites",
        ),
        (
            "/fov/satellite-passes/",
            {
                "latitude": 19.8206,
                "longitude": -155.4681,
                "elevation": 4205.0,
                "duration": 240.0,
                "ra": 45.0,
                "dec": 60.0,
                "fov_radius": 3.0,
                "mid_obs_time_jd": 2460931.191285,
                "constellation": "oneweb",
                "include_tles": True,
            },
            "Satellite passes - OneWeb constellation with TLEs",
        ),
        (
            "/fov/satellite-passes/",
            {
                "site": "rubin",
                "duration": 15.0,
                "ra": 120.0,
                "dec": -45.0,
                "fov_radius": 0.2,
                "mid_obs_time_jd": 2460931.191285,
                "min_range": 400.0,
                "max_range": 600.0,
            },
            "Satellite passes - Range filter",
        ),
        (
            "/fov/satellites-above-horizon/",
            {
                "site": "rubin",
                "julian_date": 2460931.191285,
                "constellation": "starlink",
                "illuminated_only": False,
            },
            "Satellites above horizon - Starlink, all satellites",
        ),
        (
            "/fov/satellites-above-horizon/",
            {
                "latitude": 19.8206,
                "longitude": -155.4681,
                "elevation": 4205.0,
                "julian_date": 2460931.191285,
                "min_altitude": 5.0,
                "max_altitude": 85.0,
            },
            "Satellites above horizon - Altitude range filter",
        ),
        (
            "/fov/satellites-above-horizon/",
            {
                "site": "rubin",
                "julian_date": 2460931.191285,
                "min_range": 200.0,
                "max_range": 1000.0,
                "illuminated_only": True,
            },
            "Satellites above horizon - Range and illumination filter",
        ),
        (
            "/fov/satellites-above-horizon/",
            {
                "latitude": 48.8566,
                "longitude": 2.3522,
                "elevation": 35.0,
                "julian_date": 2460931.191285,
                "constellation": "starlink",
                "min_altitude": 0.0,
                "max_altitude": 90.0,
            },
            "Satellites above horizon - Full altitude range (manual), Starlink",
        ),
        # Ephemeris endpoint test cases
        (
            "/ephemeris/name/",
            {
                "name": "ISS (ZARYA)",
                "latitude": 32.0,
                "longitude": -110.0,
                "elevation": 150.0,
                "julian_date": 2460931.191285,
                "min_altitude": -90.0,
            },
            "Ephemeris by name - ISS from coordinates with altitude filter",
        ),
        (
            "/ephemeris/catalog-number/",
            {
                "catalog": "25544",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "elevation": 35.0,
                "julian_date": 2460931.191285,
            },
            "Ephemeris by catalog number",
        ),
        (
            "/ephemeris/catalog-number/",
            {
                "catalog": "25544",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "elevation": 35.0,
                "julian_date": 2460931.191285,
                "data_source": "celestrak",
            },
            "Ephemeris by catalog - ISS with Celestrak data",
        ),
        (
            "/ephemeris/name-jdstep/",
            {
                "name": "ISS (ZARYA)",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "elevation": 35.0,
                "startjd": 2460931.191285,
                "stopjd": 2460932.191285,
                "stepjd": 0.01,
            },
            "Ephemeris by name with JD step",
        ),
        # Tool endpoint test cases
        (
            "/tools/norad-ids-from-name/",
            {"name": "ISS (ZARYA)"},
            "Tools - NORAD IDs from name (ISS)",
        ),
        (
            "/tools/names-from-norad-id/",
            {"id": "25544"},
            "Tools - Names from NORAD ID (25544)",
        ),
        (
            "/tools/get-tle-data/",
            {"id": "25544", "id_type": "catalog"},
            "Tools - Get TLE data for ISS",
        ),
        (
            "/tools/get-tle-data/",
            {
                "id": "ISS (ZARYA)",
                "id_type": "name",
                "start_date_jd": 2460900.0,
                "end_date_jd": 2461000.0,
            },
            "Tools - Get TLE data for ISS with date range",
        ),
        (
            "/tools/get-nearest-tle/",
            {"id": "25544", "id_type": "catalog", "epoch": 2460901.191285},
            "Tools - Get nearest TLE for ISS",
        ),
        (
            "/tools/get-starlink-generations/",
            {},
            "Tools - Get Starlink generations list",
        ),
    ]

    passed = 0
    failed = 0

    for endpoint, params, name in tests:
        if run_test(endpoint, params, name):
            passed += 1
        else:
            failed += 1
        time.sleep(0.5)

    print(f"\n{'=================================================='}")
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print(f"{'=================================================='}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
