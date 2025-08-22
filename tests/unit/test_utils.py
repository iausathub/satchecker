# ruff: noqa: S101
import math
from datetime import datetime, timezone

import numpy as np
import pytest
from astropy.time import Time
from skyfield.api import wgs84
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.common.exceptions import ValidationError
from api.utils import coordinate_systems, time_utils
from api.utils.output_utils import position_data_to_json
from api.utils.propagation_strategies import (
    SkyfieldPropagationStrategy,
    process_satellite_batch,
)


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


def test_icrf2radec_pos_ndim():
    pos = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    expected_ra_deg = [0, 90, 0]
    expected_dec_deg = [0, 0, 90]
    ra_deg, dec_deg = coordinate_systems.icrf2radec(pos, unit_vector=True, deg=True)
    assert np.allclose(ra_deg, expected_ra_deg)
    assert np.allclose(dec_deg, expected_dec_deg)

    ra_deg, dec_deg = coordinate_systems.icrf2radec(pos, unit_vector=False, deg=True)
    assert np.allclose(ra_deg, expected_ra_deg)
    assert np.allclose(dec_deg, expected_dec_deg)


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


def test_process_satellite_batch():
    # Use the same TLE values from the passing FOV tests (FENGYUN 1C DEB)
    # Create proper satellite and TLE objects like in the FOV tests
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

    tle_batch = [tle]
    julian_dates = [Time("2024-10-01T18:19:13", format="isot", scale="utc").jd]
    latitude = 43.1929
    longitude = -81.3256
    elevation = 300
    fov_center = (24.797270, 75.774139)
    fov_radius = 2.0
    include_tles = True
    illuminated_only = False

    args = (
        tle_batch,
        julian_dates,
        latitude,
        longitude,
        elevation,
        fov_center,
        fov_radius,
        include_tles,
        illuminated_only,
    )
    result = process_satellite_batch(args)

    assert result[0][0]["ra"] == pytest.approx(23.95167273, rel=1e-9)
    assert result[0][0]["dec"] == pytest.approx(75.60577991, rel=1e-9)


def test_skyfield_propagation_strategy():
    julian_date = 2459000.5
    tle_line_1 = "1 25544U 98067A   20333.54791667  .00016717  00000-0  10270-3 0  9000"
    tle_line_2 = "2 25544  51.6442  21.4611 0001363  85.7861  74.4771 15.49180547  1000"
    latitude = 34.0522
    longitude = -118.2437
    elevation = 100

    strategy = SkyfieldPropagationStrategy()
    result = strategy.propagate(
        julian_dates=[julian_date],
        tle_line_1=tle_line_1,
        tle_line_2=tle_line_2,
        latitude=latitude,
        longitude=longitude,
        elevation=elevation,
    )

    assert result[0].ra == pytest.approx(234.01865005681205, rel=1e-9)
    assert result[0].dec == pytest.approx(-51.424189307650366, rel=1e-9)


def test_skyfield_propagation_strategy_error():
    julian_date = 2459000.5
    tle_line_1 = ""
    tle_line_2 = ""
    latitude = 0
    longitude = 0
    elevation = 0

    strategy = SkyfieldPropagationStrategy()
    result = strategy.propagate(
        julian_dates=[julian_date],
        tle_line_1=tle_line_1,
        tle_line_2=tle_line_2,
        latitude=latitude,
        longitude=longitude,
        elevation=elevation,
    )
    # Weird lat/long./elevation values will not cause errors -
    # they will be normalized to a valid range; invalid TLE data
    # will cause a NaN result, but not throw an exception
    assert math.isnan(result[0].ra)
    assert math.isnan(result[0].dec)


def test_position_data_to_json():
    name = "ISS (ZARYA)"
    catalog_id = 25544
    date_collected = datetime.now()
    tle_epoch = datetime.now()
    data_source = "spacetrack"
    intl_designator = "1998-067A"

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
        name,
        intl_designator,
        catalog_id,
        date_collected,
        tle_epoch,
        data_source,
        results,
        api_source,
        api_version,
    )

    assert data_set["data"][0][0] == name
    assert data_set["data"][0][4] == pytest.approx(306.063400059889)
    assert data_set["source"] == api_source
    assert data_set["version"] == api_version


def test_position_data_to_json_errors():
    pass


# This test only verifies the current implementation, and will need
# to be updated when teme_to_ecef is reviewed/corrected
def test_teme_to_ecef():
    r_teme = [1.0, 0.0, 0.0]
    theta_gst = 0.0
    expected_result = np.array([1.0, 0.0, 0.0])
    result = coordinate_systems.teme_to_ecef(r_teme, theta_gst)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    r_teme = [1.0, 0.0, 0.0]
    theta_gst = np.pi / 2
    expected_result = np.array([0.0, -1.0, 0.0])
    result = coordinate_systems.teme_to_ecef(r_teme, theta_gst)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    r_teme = [1.0, 0.0, 0.0]
    theta_gst = np.pi
    expected_result = np.array([-1.0, 0.0, 0.0])
    result = coordinate_systems.teme_to_ecef(r_teme, theta_gst)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    r_teme = [1.0, 0.0, 0.0]
    theta_gst = 3 * np.pi / 2
    expected_result = np.array([0.0, 1.0, 0.0])
    result = coordinate_systems.teme_to_ecef(r_teme, theta_gst)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    r_teme = [1.0, 0.0, 1.0]
    theta_gst = np.pi / 2
    expected_result = np.array([0.0, -1.0, 1.0])
    result = coordinate_systems.teme_to_ecef(r_teme, theta_gst)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)


# This test only verifies the current implementation, and will need
# to be updated when ecef_to_enu is reviewed/corrected
def test_ecef_to_enu():
    r_ecef = [1.0, 0.0, 0.0]
    lat = 0.0
    lon = 0.0
    expected_result = np.array([0.0, 0.0, 1.0])
    result = coordinate_systems.ecef_to_enu(r_ecef, lat, lon)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # 90 degrees latitude
    r_ecef = [0.0, 0.0, 1.0]
    lat = 90.0
    lon = 0.0
    expected_result = np.array([0.0, 0.0, 1.0])
    result = coordinate_systems.ecef_to_enu(r_ecef, lat, lon)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # 90 degrees longitude
    r_ecef = [0.0, 1.0, 0.0]
    lat = 0.0
    lon = 90.0
    expected_result = np.array([0.0, 0.0, 1.0])
    result = coordinate_systems.ecef_to_enu(r_ecef, lat, lon)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # 45 degrees latitude and longitude
    r_ecef = [1.0, 1.0, 1.0]
    lat = 45.0
    lon = 45.0
    expected_result = np.array([0, -0.2928932, 1.707107])
    result = coordinate_systems.ecef_to_enu(r_ecef, lat, lon)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # -90 degrees latitude
    r_ecef = [0.0, 0.0, -1.0]
    lat = -90.0
    lon = 0.0
    expected_result = np.array([0.0, 0.0, 1.0])
    result = coordinate_systems.ecef_to_enu(r_ecef, lat, lon)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # with error
    r_ecef = [1.0, 0.0]
    lat = 0.0
    lon = 0.0
    with pytest.raises(ValueError):
        result = coordinate_systems.ecef_to_enu(r_ecef, lat, lon)


# This test only verifies the current implementation, and will need
# to be updated when ecef_to_itrs is reviewed/corrected
def test_ecef_to_itrs():
    # with zero coordinates
    r_ecef = np.array([0.0, 0.0, 0.0])
    expected_result = np.array([0.0, 0.0, 0.0])
    result = coordinate_systems.ecef_to_itrs(r_ecef)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # with one non-zero coordinate
    r_ecef = np.array([6378137.0, 0.0, 0.0])  # Earth's semi-major axis in meters
    expected_result = np.array([6378137.0 / (1 + 1 / 298.257223563), 0.0, 0.0])
    result = coordinate_systems.ecef_to_itrs(r_ecef)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # with arbitrary coordinates
    r_ecef = np.array([1000.0, 2000.0, 3000.0])
    expected_result = np.array([1000.0 / (1 + 1 / 298.257223563), 2000.0, 3000.0])
    result = coordinate_systems.ecef_to_itrs(r_ecef)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # with error
    r_ecef = np.array([1000.0, 2000.0])
    with pytest.raises(IndexError):
        result = coordinate_systems.ecef_to_itrs(r_ecef)


# This test only verifies the current implementation, and will need
# to be updated when itrs_to_gcrs is reviewed/corrected
def test_itrs_to_gcrs():
    # with zero coordinates
    r_itrs = np.array([0.0, 0.0, 0.0])
    julian_date = 2451545.0  # Example Julian date
    expected_result = np.array([0.0, 0.0, 0.0])
    result = coordinate_systems.itrs_to_gcrs(r_itrs, julian_date)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # with one non-zero coordinate
    r_itrs = np.array([1.0, 0.0, 0.0])
    expected_result = np.array([0.181493, -0.983392, 0.0])
    result = coordinate_systems.itrs_to_gcrs(r_itrs, julian_date)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # with arbitrary coordinates
    r_itrs = np.array([1.0, 1.0, 1.0])
    expected_result = np.array([1.164885, -0.801899, 1.0])
    result = coordinate_systems.itrs_to_gcrs(r_itrs, julian_date)
    np.testing.assert_almost_equal(result, expected_result, decimal=6)

    # with error
    r_itrs = np.array([1.0, 1.0])
    with pytest.raises(IndexError):
        result = coordinate_systems.itrs_to_gcrs(r_itrs, julian_date)

    r_itrs = np.array([1.0, 1.0, 1.0])
    julian_date = "date"
    with pytest.raises(TypeError):
        result = coordinate_systems.itrs_to_gcrs(r_itrs, julian_date)


# This test only verifies the current implementation, and will need
# to be updated when enu_to_az_el is reviewed/corrected
def test_enu_to_az_el():
    # ENU coordinates with zero elevation
    r_enu = np.array([1.0, 0.0, 0.0])
    expected_az = 90.0  # Azimuth in degrees
    expected_el = 0.0  # Elevation in degrees
    az, el = coordinate_systems.enu_to_az_el(r_enu)
    assert np.isclose(az, expected_az, atol=1e-6)
    assert np.isclose(el, expected_el, atol=1e-6)

    # ENU coordinates with 45 degrees elevation
    r_enu = np.array([1.0, 1.0, 1.0])
    expected_az = 45.0  # Azimuth in degrees
    expected_el = 35.264389682754654  # Elevation in degrees (arctan2(1, sqrt(2)))
    az, el = coordinate_systems.enu_to_az_el(r_enu)
    assert np.isclose(az, expected_az, atol=1e-6)
    assert np.isclose(el, expected_el, atol=1e-6)

    # ENU coordinates with negative azimuth
    r_enu = np.array([-1.0, 0.0, 0.0])
    expected_az = 270.0
    expected_el = 0.0
    az, el = coordinate_systems.enu_to_az_el(r_enu)
    assert np.isclose(az, expected_az, atol=1e-6)
    assert np.isclose(el, expected_el, atol=1e-6)

    # ENU coordinates with zero azimuth and elevation
    r_enu = np.array([0.0, 0.0, 0.0])
    expected_az = 0.0
    expected_el = 0.0
    az, el = coordinate_systems.enu_to_az_el(r_enu)
    assert np.isclose(az, expected_az, atol=1e-6)
    assert np.isclose(el, expected_el, atol=1e-6)

    # with error
    r_enu = np.array([1.0, 1.0])
    with pytest.raises(IndexError):
        az, el = coordinate_systems.enu_to_az_el(r_enu)


# This test only verifies the current implementation, and will need
# to be updated when ecef_to_eci is reviewed/corrected
def test_ecef_to_eci():
    r_ecef = [1.0, 0.0, 0.0]

    # theta_gst = 0 degrees
    theta_gst = 0.0
    expected_eci = np.array([1.0, 0.0, 0.0])
    result = coordinate_systems.ecef_to_eci(r_ecef, theta_gst)
    np.testing.assert_almost_equal(result, expected_eci, decimal=6)

    # theta_gst = 90 degrees
    theta_gst = 90.0
    expected_eci = np.array([0.0, -1.0, 0.0])
    result = coordinate_systems.ecef_to_eci(r_ecef, theta_gst)
    np.testing.assert_almost_equal(result, expected_eci, decimal=6)

    # theta_gst = 180 degrees
    theta_gst = 180.0
    expected_eci = np.array([-1.0, 0.0, 0.0])
    result = coordinate_systems.ecef_to_eci(r_ecef, theta_gst)
    np.testing.assert_almost_equal(result, expected_eci, decimal=6)

    # theta_gst = 270 degrees
    theta_gst = 270.0
    expected_eci = np.array([0.0, 1.0, 0.0])
    result = coordinate_systems.ecef_to_eci(r_ecef, theta_gst)
    np.testing.assert_almost_equal(result, expected_eci, decimal=6)

    # theta_gst = 41 degrees
    r_ecef = [1.235, 0.3712, 22.0]
    theta_gst = 41.0
    expected_eci = np.array([1.175595, -0.530085, 22.0])
    result = coordinate_systems.ecef_to_eci(r_ecef, theta_gst)
    np.testing.assert_almost_equal(result, expected_eci, decimal=6)

    # with error
    r_ecef = [1.0, 0.0]
    with pytest.raises(ValueError):
        result = coordinate_systems.ecef_to_eci(r_ecef, theta_gst)


# This test only verifies the current implementation, and will need
# to be updated when az_el_to_ra_dec is reviewed/corrected
def test_az_el_to_ra_dec():
    az = 45.0
    el = 30.0
    lat = 40.0
    lon = -75.0
    jd = 2451545.0
    expected_ra = 114.46864445153196
    expected_dec = 52.23210340306717

    ra, dec = coordinate_systems.az_el_to_ra_dec(az, el, lat, lon, jd)
    assert np.isclose(ra, expected_ra, atol=1e-6)
    assert np.isclose(dec, expected_dec, atol=1e-6)

    az = 0.0
    el = 0.0
    lat = 0.0
    lon = 0.0
    expected_ra = 190.46061837000005
    expected_dec = 90.0

    ra, dec = coordinate_systems.az_el_to_ra_dec(az, el, lat, lon, jd)
    assert np.isclose(ra, expected_ra, atol=1e-6)
    assert np.isclose(dec, expected_dec, atol=1e-6)

    az = None
    with pytest.raises(TypeError):
        ra, dec = coordinate_systems.az_el_to_ra_dec(az, el, lat, lon, jd)


def test_is_illuminated():
    # Examples from SatChecker and checked with Privateer's GlintEvader
    # https://satchecker.cps.iau.org/ephemeris/name/?name=STARLINK-2617&elevation=100
    # &latitude=33&longitude=-110&julian_date=2460546.599502
    # STARLINK-1477, STARLINK-3154, STARLINK-2617, STARLINK-1986
    # STARLINK-2291, STARLINK-30263, STARLINK-31166

    # should be illuminated
    sat_gcrs = np.array([-1807.4145165806299, -5481.865083864486, 3817.782079208943])
    julian_date = 2460546.599502
    is_illuminated = coordinate_systems.is_illuminated(sat_gcrs, julian_date)
    assert is_illuminated

    sat_gcrs = np.array([-1726.6525239983253, -5556.764988629915, 3732.6312069408664])
    is_illuminated = coordinate_systems.is_illuminated(sat_gcrs, julian_date)
    assert is_illuminated

    sat_gcrs = np.array([-2788.9344500353254, -6082.063324305135, 1780.452113395069])
    is_illuminated = coordinate_systems.is_illuminated(sat_gcrs, julian_date)
    assert is_illuminated

    sat_gcrs = np.array([-6285.693766146678, -2883.510160329265, 372.90511732453666])
    is_illuminated = coordinate_systems.is_illuminated(sat_gcrs, julian_date)
    assert is_illuminated

    # should not be illuminated
    sat_gcrs = np.array([2148.476260974862, -5720.341032518884, 3250.5047622565057])
    is_illuminated = coordinate_systems.is_illuminated(sat_gcrs, julian_date)
    assert not is_illuminated

    sat_gcrs = np.array([1239.1815032279183, -6748.906100431373, 1012.4062279591224])
    is_illuminated = coordinate_systems.is_illuminated(sat_gcrs, julian_date)
    assert not is_illuminated

    sat_gcrs = np.array([-145.69690994172956, -6807.470474898967, 877.3659084400132])
    is_illuminated = coordinate_systems.is_illuminated(sat_gcrs, julian_date)
    assert not is_illuminated

    # with error
    sat_gcrs = np.array([1.0, 0.0])
    with pytest.raises(ValueError):
        is_illuminated = coordinate_systems.is_illuminated(sat_gcrs, julian_date)


def test_is_illuminated_vectorized():
    # should be illuminated
    sat_gcrs = np.array([-1807.4145165806299, -5481.865083864486, 3817.782079208943])
    julian_date = 2460546.599502
    is_illuminated = coordinate_systems.is_illuminated_vectorized(
        [sat_gcrs], [julian_date]
    )
    assert is_illuminated[0]

    sat_gcrs = np.array([-1726.6525239983253, -5556.764988629915, 3732.6312069408664])
    is_illuminated = coordinate_systems.is_illuminated_vectorized(
        [sat_gcrs], [julian_date]
    )
    assert is_illuminated[0]

    sat_gcrs = np.array([-2788.9344500353254, -6082.063324305135, 1780.452113395069])
    is_illuminated = coordinate_systems.is_illuminated_vectorized(
        [sat_gcrs], [julian_date]
    )
    assert is_illuminated[0]

    sat_gcrs = np.array([-6285.693766146678, -2883.510160329265, 372.90511732453666])
    is_illuminated = coordinate_systems.is_illuminated_vectorized(
        [sat_gcrs], [julian_date]
    )
    assert is_illuminated[0]

    # should not be illuminated
    sat_gcrs = np.array([2148.476260974862, -5720.341032518884, 3250.5047622565057])
    is_illuminated = coordinate_systems.is_illuminated_vectorized(
        [sat_gcrs], [julian_date]
    )
    assert not is_illuminated[0]

    sat_gcrs = np.array([1239.1815032279183, -6748.906100431373, 1012.4062279591224])
    is_illuminated = coordinate_systems.is_illuminated_vectorized(
        [sat_gcrs], [julian_date]
    )
    assert not is_illuminated[0]

    sat_gcrs = np.array([-145.69690994172956, -6807.470474898967, 877.3659084400132])
    is_illuminated = coordinate_systems.is_illuminated_vectorized(
        [sat_gcrs], [julian_date]
    )
    assert not is_illuminated[0]

    # with error
    sat_gcrs = np.array([1.0, 0.0])
    with pytest.raises(ValueError):
        is_illuminated = coordinate_systems.is_illuminated_vectorized(
            [sat_gcrs], [julian_date]
        )


def test_ensure_datetime():
    # Test date string in YYYY-MM-DD format
    date_str = "2025-01-01"
    result = time_utils.ensure_datetime(date_str)
    assert result == datetime(2025, 1, 1, tzinfo=timezone.utc)

    # Test date string in YYYY-MM-DD HH:MM:SS format
    date_str = "2025-01-01 12:00:00"
    result = time_utils.ensure_datetime(date_str)
    assert result == datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    # Test timezone-aware datetime
    dt = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    result = time_utils.ensure_datetime(dt)
    assert result == dt

    # Test naive datetime
    dt = datetime(2025, 1, 1, 12, 0, 0)
    result = time_utils.ensure_datetime(dt)
    assert result == datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    # Test invalid input types
    with pytest.raises(TypeError):
        time_utils.ensure_datetime(123)

    with pytest.raises(ValueError):
        time_utils.ensure_datetime("invalid-date")
