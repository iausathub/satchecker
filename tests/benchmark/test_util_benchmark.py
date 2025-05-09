# ruff: noqa: S101, E501
import numpy as np
import pytest
from astropy.time import Time
from skyfield.api import load, wgs84

from api.utils import coordinate_systems
from api.utils.propagation_strategies import (
    PropagationInfo,
    SkyfieldPropagationStrategy,
    satellite_position,
)
from api.utils.time_utils import calculate_lst, jd_to_gst


@pytest.fixture
def sample_tle():
    """Provide a sample TLE for testing."""
    tle_line_1 = "1 25544U 98067A   20333.54791667  .00016717  00000-0  10270-3 0  9000"
    tle_line_2 = "2 25544  51.6442  21.4611 0001363  85.7861  74.4771 15.49180547  1000"
    return tle_line_1, tle_line_2


@pytest.fixture
def sample_position():
    """Provide a sample position vector for testing."""
    return np.array([6439.4733751377125, 170.5387440379329, 146.3086642536418])


@pytest.fixture
def sample_julian_date():
    """Provide a sample Julian date for testing."""
    return 2459000.5


@pytest.fixture
def sample_location():
    """Provide a sample location for testing."""
    latitude = 34.0522
    longitude = -118.2437
    elevation = 100
    return latitude, longitude, elevation


def test_benchmark_icrf2radec(benchmark, sample_position):
    """Benchmark the icrf2radec function with degrees."""
    result = benchmark(
        coordinate_systems.icrf2radec, sample_position, unit_vector=False, deg=True
    )
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_benchmark_icrf2radec_unit_vector(benchmark, sample_position):
    """Benchmark the icrf2radec function with unit vectors."""
    normalized_pos = sample_position / np.linalg.norm(sample_position)
    result = benchmark(
        coordinate_systems.icrf2radec, normalized_pos, unit_vector=True, deg=True
    )
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_benchmark_jd_to_gst(benchmark, sample_julian_date):
    """Benchmark the jd_to_gst function."""
    nutation = 17.20  # Example nutation in degrees
    result = benchmark(jd_to_gst, sample_julian_date, nutation)
    assert isinstance(result, float)


def test_benchmark_calculate_lst(benchmark, sample_location, sample_julian_date):
    """Benchmark the calculate_lst function."""
    _, longitude, _ = sample_location
    result = benchmark(calculate_lst, longitude, sample_julian_date)
    assert isinstance(result, float)


def test_benchmark_tle_to_icrf_state(benchmark, sample_tle, sample_julian_date):
    """Benchmark the tle_to_icrf_state function."""
    tle_line_1, tle_line_2 = sample_tle

    # Convert float to Time object since coordinate_systems.tle_to_icrf_state expects a Time object
    jd_time = Time(sample_julian_date, format="jd")

    result = benchmark(
        coordinate_systems.tle_to_icrf_state, tle_line_1, tle_line_2, jd_time
    )
    assert result.shape == (6,)


def test_benchmark_skyfield_propagation(
    benchmark, sample_tle, sample_location, sample_julian_date
):
    """Benchmark the Skyfield propagation strategy."""
    tle_line_1, tle_line_2 = sample_tle
    latitude, longitude, elevation = sample_location

    def setup_and_propagate():
        propagation_info = PropagationInfo(
            SkyfieldPropagationStrategy(),
            tle_line_1,
            tle_line_2,
            [sample_julian_date],
            latitude,
            longitude,
            elevation,
        )
        return propagation_info.propagate()

    result = benchmark(setup_and_propagate)
    assert len(result) == 1
    assert hasattr(result[0], "ra")
    assert hasattr(result[0], "dec")


def test_benchmark_is_illuminated(benchmark, sample_julian_date):
    """Benchmark the is_illuminated function."""
    # Create a sample GCRS position
    sat_gcrs = np.array([6439.4733751377125, 170.5387440379329, 146.3086642536418])

    result = benchmark(coordinate_systems.is_illuminated, sat_gcrs, sample_julian_date)
    assert isinstance(result, bool)


def test_benchmark_get_phase_angle(benchmark, sample_julian_date):
    """Benchmark the get_phase_angle function."""
    # Create sample vectors
    topocentricn = np.array([0.6, 0.7, 0.8]) / np.sqrt(0.6**2 + 0.7**2 + 0.8**2)
    sat_gcrs = np.array([6439.4733751377125, 170.5387440379329, 146.3086642536418])

    result = benchmark(
        coordinate_systems.get_phase_angle, topocentricn, sat_gcrs, sample_julian_date
    )
    assert isinstance(result, float)


def test_benchmark_get_earth_sun_positions(benchmark, sample_julian_date):
    """Benchmark the get_earth_sun_positions function."""
    result = benchmark(coordinate_systems.get_earth_sun_positions, sample_julian_date)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], np.ndarray)
    assert isinstance(result[1], np.ndarray)


def test_benchmark_full_satellite_position_calculation(
    benchmark, sample_tle, sample_location, sample_julian_date
):
    """Benchmark the full satellite position calculation pipeline."""
    tle_line_1, tle_line_2 = sample_tle
    latitude, longitude, elevation = sample_location

    ts = load.timescale()
    t = ts.ut1_jd(sample_julian_date)

    def calculate_full_position():
        from skyfield.api import EarthSatellite

        satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)
        curr_pos = wgs84.latlon(latitude, longitude, elevation)

        difference = satellite - curr_pos
        topocentric = difference.at(t)

        ra, dec, distance = topocentric.radec()
        alt, az, _ = topocentric.altaz()

        sat_gcrs = satellite.at(t).position.km
        obs_gcrs = curr_pos.at(t).position.km

        topocentricn = topocentric.position.km / np.linalg.norm(topocentric.position.km)
        phase_angle = coordinate_systems.get_phase_angle(
            topocentricn, sat_gcrs, sample_julian_date
        )
        illuminated = coordinate_systems.is_illuminated(sat_gcrs, sample_julian_date)

        return satellite_position(
            ra._degrees,
            dec.degrees,
            0.0,  # dracosdec - dummy value for benchmark
            0.0,  # ddec - dummy value for benchmark
            alt._degrees,
            az._degrees,
            distance.km,
            0.0,  # ddistance - dummy value for benchmark
            phase_angle,
            illuminated,
            sat_gcrs.tolist(),
            obs_gcrs.tolist(),
            sample_julian_date,
        )

    result = benchmark(calculate_full_position)
    assert isinstance(result, satellite_position)
