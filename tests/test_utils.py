# ruff: noqa: S101
import os

import numpy as np
import pytest
from core import utils

from api.utils import time_utils

assert_precision = 0.000001


def test_get_db_login():
    os.environ["LOCAL_DB"] = "1"

    db_login = utils.get_db_login()
    assert db_login == ["postgres", "postgres", "localhost", "5432", "satchecker_test"]


def test_icrf2radec_degrees_unit():
    pos = np.array([1, 0, 0])
    expected_ra_deg = 0
    expected_dec_deg = 0
    ra_deg, dec_deg = utils.icrf2radec(pos, unit_vector=True, deg=True)
    assert np.isclose(ra_deg, expected_ra_deg)
    assert np.isclose(dec_deg, expected_dec_deg)


def test_icrf2radec_radians_unit():
    pos = np.array([1, 0, 0])
    expected_ra_rad = 0
    expected_dec_rad = 0
    ra_rad, dec_rad = utils.icrf2radec(pos, unit_vector=True, deg=False)
    assert np.isclose(ra_rad, expected_ra_rad)
    assert np.isclose(dec_rad, expected_dec_rad)


def test_icrf2radec():
    pos = np.array([101, 2000, -20])
    expected_ra_deg = 87.10901904
    expected_dec_deg = -0.57220957
    ra_deg, dec_deg = utils.icrf2radec(pos, unit_vector=False, deg=True)
    assert np.isclose(ra_deg, expected_ra_deg)
    assert np.isclose(dec_deg, expected_dec_deg)

    pos = np.array([-1023, -302, 402])
    expected_ra_deg = 196.44713619
    expected_dec_deg = 20.65054402
    ra_deg, dec_deg = utils.icrf2radec(pos, unit_vector=False, deg=True)
    assert np.isclose(ra_deg, expected_ra_deg)
    assert np.isclose(dec_deg, expected_dec_deg)


def test_jd_arange():
    start_jd = 2451545.0
    end_jd = 2451545.5
    dr = 0.1
    decimals = 2
    expected_dates = [2451545.0, 2451545.1, 2451545.2, 2451545.3, 2451545.4, 2451545.5]
    result = utils.jd_arange(start_jd, end_jd, dr, decimals)
    assert np.allclose([t.jd for t in result], expected_dates)

    # Test decimal place handling
    start_jd = 2451545.123456
    end_jd = 2451545.223456
    dr = 0.05
    decimals = 4
    result = utils.jd_arange(start_jd, end_jd, dr, decimals)
    assert all(len(str(t.jd).split(".")[1]) <= decimals for t in result)

    # Test handling of end date `b` exactly on a step increment
    start_jd = 2451545.0
    end_jd = 2451545.2
    dr = 0.1
    result = utils.jd_arange(start_jd, end_jd, dr)
    assert np.isclose(result[-1].jd, end_jd)

    # Test error handling
    with pytest.raises(Exception) as exc_info:
        utils.jd_arange("invalid", "invalid", 0.1)
    assert "Invalid Julian Date" in str(exc_info.value)


def test_jd_to_gst():
    jd = 2451545.0  # A known Julian Day
    nutation = 17.20  # Example nutation in degrees
    expected_gast = np.deg2rad(
        (
            280.46061837
            + 360.98564736629 * (jd - 2451545.0)
            + 0.000387933 * ((jd + 32.184 / (24 * 60 * 60) - 2451545.0) / 36525.0) ** 2
            - ((jd + 32.184 / (24 * 60 * 60) - 2451545.0) / 36525.0) ** 3 / 38710000.0
            + nutation
        )
        % 360
    )

    result = time_utils.jd_to_gst(jd, nutation)
    assert np.isclose(result, expected_gast), f"Expected {expected_gast}, got {result}"

    jd = 2451545.5
    nutation = 12.34

    expected_gast = np.deg2rad(
        (
            280.46061837
            + 360.98564736629 * (jd - 2451545.0)
            + 0.000387933 * ((jd + 32.184 / (24 * 60 * 60) - 2451545.0) / 36525.0) ** 2
            - ((jd + 32.184 / (24 * 60 * 60) - 2451545.0) / 36525.0) ** 3 / 38710000.0
            + nutation
        )
        % 360
    )

    result = time_utils.jd_to_gst(jd, nutation)
    assert np.isclose(result, expected_gast), f"Expected {expected_gast}, got {result}"


def test_calculate_lst():
    longitude = 32.0
    jd = 2451545.0
    expected_lst = 5.453466
    result = time_utils.calculate_lst(longitude, jd)
    assert np.isclose(result, expected_lst), f"Expected {expected_lst}, got {result}"

    longitude = -110.0
    jd = 2451545.5
    expected_lst = 6.125293
    result = time_utils.calculate_lst(longitude, jd)
    assert np.isclose(result, expected_lst), f"Expected {expected_lst}, got {result}"
