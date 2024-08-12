# ruff: noqa: S101
import math
from datetime import datetime

import numpy as np
import pytest
from api.common.exceptions import ValidationError
from api.utils import coordinate_systems, time_utils
from api.utils.output_utils import position_data_to_json
from api.utils.propagation_strategies import (
    PropagationInfo,
    SkyfieldPropagationStrategy,
)
from astropy.time import Time
from skyfield.api import wgs84


def test_icrf2radec_degrees_unit():
    pos = np.array([1, 0, 0])
    expected_ra_deg = 0
    expected_dec_deg = 0
    ra_deg, dec_deg = coordinate_systems.icrf2radec(pos, unit_vector=True, deg=True)
    assert np.isclose(ra_deg, expected_ra_deg)
    assert np.isclose(dec_deg, expected_dec_deg)


def test_icrf2radec_radians_unit():
    pos = np.array([1, 0, 0])
    expected_ra_rad = 0
    expected_dec_rad = 0
    ra_rad, dec_rad = coordinate_systems.icrf2radec(pos, unit_vector=True, deg=False)
    assert np.isclose(ra_rad, expected_ra_rad)
    assert np.isclose(dec_rad, expected_dec_rad)


def test_icrf2radec():
    pos = np.array([101, 2000, -20])
    expected_ra_deg = 87.10901904
    expected_dec_deg = -0.57220957
    ra_deg, dec_deg = coordinate_systems.icrf2radec(pos, unit_vector=False, deg=True)
    assert np.isclose(ra_deg, expected_ra_deg)
    assert np.isclose(dec_deg, expected_dec_deg)

    pos = np.array([-1023, -302, 402])
    expected_ra_deg = 196.44713619
    expected_dec_deg = 20.65054402
    ra_deg, dec_deg = coordinate_systems.icrf2radec(pos, unit_vector=False, deg=True)
    assert np.isclose(ra_deg, expected_ra_deg)
    assert np.isclose(dec_deg, expected_dec_deg)


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


def test_calc_correct_position():
    lat = 34.0522
    long = -118.2437
    height = 100
    expected_position = wgs84.latlon(lat, long, height)

    result = coordinate_systems.calculate_current_position(lat, long, height)
    assert result.latitude.degrees == lat
    assert result.longitude.degrees == long
    assert result.elevation.m == expected_position.elevation.m

    lat = "a"
    long = "b"
    height = "c"

    # any numeric input works since values are converted to correct ranges
    # in skyfield
    with pytest.raises(TypeError):
        result = coordinate_systems.calculate_current_position(lat, long, height)


def test_tle_to_icrf_state_with_epoch():
    tle_line_1 = "1 25544U 98067A   20333.54791667  .00016717  00000-0  10270-3 0  9000"
    tle_line_2 = "2 25544  51.6442  21.4611 0001363  85.7861  74.4771 15.49180547  1000"
    jd = 0  # Use epoch from TLE

    result = coordinate_systems.tle_to_icrf_state(tle_line_1, tle_line_2, jd)
    assert result[0] == pytest.approx(6439.4733751377125, rel=1e-9)
    assert result[5] == pytest.approx(5.726261362770601, rel=1e-9)
    assert result.shape == (6,)
    assert isinstance(result, np.ndarray)


def test_tle_to_icrf_state_with_jd():
    tle_line_1 = "1 25544U 98067A   20333.54791667  .00016717  00000-0  10270-3 0  9000"
    tle_line_2 = "2 25544  51.6442  21.4611 0001363  85.7861  74.4771 15.49180547  1000"
    jd = Time(2459000.5, format="jd")

    result = coordinate_systems.tle_to_icrf_state(tle_line_1, tle_line_2, jd)
    assert result[0] == pytest.approx(-6300.1587196871105, rel=1e-9)
    assert result[5] == pytest.approx(5.253949584720267, rel=1e-9)
    assert result.shape == (6,)
    assert isinstance(result, np.ndarray)


def test_tle_to_icrf_state_invalid_tle():
    tle_line_1 = "1"
    tle_line_2 = "2"
    jd = 0  # Use epoch from TLE

    with pytest.raises(ValidationError):
        coordinate_systems.tle_to_icrf_state(tle_line_1, tle_line_2, jd)


def test_skyfield_propagation_strategy():
    julian_date = 2459000.5
    tle_line_1 = "1 25544U 98067A   20333.54791667  .00016717  00000-0  10270-3 0  9000"
    tle_line_2 = "2 25544  51.6442  21.4611 0001363  85.7861  74.4771 15.49180547  1000"
    latitude = 34.0522
    longitude = -118.2437
    elevation = 100

    propagation_info = PropagationInfo(
        SkyfieldPropagationStrategy(),
        tle_line_1,
        tle_line_2,
        julian_date,
        latitude,
        longitude,
        elevation,
    )
    result = propagation_info.propagate()

    assert result.ra == pytest.approx(234.01865005681205, rel=1e-9)
    assert result.dec == pytest.approx(-51.424189307650366, rel=1e-9)


def test_skyfield_propagation_strategy_error():
    julian_date = 2459000.5
    tle_line_1 = ""
    tle_line_2 = ""
    latitude = 0
    longitude = 0
    elevation = 0

    propagation_info = PropagationInfo(
        SkyfieldPropagationStrategy(),
        tle_line_1,
        tle_line_2,
        julian_date,
        latitude,
        longitude,
        elevation,
    )
    result = propagation_info.propagate()
    # Weird lat/long./elevation values will not cause errors -
    # they will be normalized to a valid range; invalid TLE data
    # will cause a NaN result, but not throw an exception
    assert math.isnan(result.ra)
    assert math.isnan(result.dec)


def test_position_data_to_json():
    name = "ISS (ZARYA)"
    catalog_id = 25544
    date_collected = datetime.now()
    data_source = "spacetrack"

    results = [
        (
            306.063400059889,
            -33.66579178108618,
            -0.06540086862265515,
            0.11862347867553424,
            -85.3068799143513,
            98.86517357440482,
            5942.835544462139,
            25.903436713068203,
            51.95659698598527,
            True,
            [-643.0446467211723, -0.01912640597469738, 166.51906642428338],
            [-3554.7354993588046, 3998.2681386590784, 3460.9157688886103],
            2459000.5,
        )
    ]

    api_source = "test"
    api_version = "v1"
    data_set = position_data_to_json(
        name, catalog_id, date_collected, data_source, results, api_source, api_version
    )

    assert data_set["data"][0][0] == name
    assert data_set["data"][0][4] == pytest.approx(306.063400059889)
    assert data_set["source"] == api_source
    assert data_set["version"] == api_version


def test_position_data_to_json_errors():
    pass
