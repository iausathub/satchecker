# ruff: noqa: S101
import logging

from astropy.coordinates import EarthLocation
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


def test_satellite_in_fov():
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
        location=EarthLocation(lat=43.192909, lon=-81.325655, height=300),
        mid_obs_time_jd=Time("2024-10-01 18:19:13"),
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
        location=EarthLocation(lat=43.192909, lon=-81.325655, height=300),
        mid_obs_time_jd=Time("2024-10-01 18:19:13"),
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


def test_satellite_outside_fov():
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
        location=EarthLocation(lat=43, lon=-81, height=300),
        mid_obs_time_jd=Time("2024-10-01 18:19:13"),
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


def test_empty_tle_list():
    """Test behavior with no TLEs available"""
    tle_repo = FakeTLERepository([])

    result = get_satellite_passes_in_fov(
        tle_repo,
        location=EarthLocation(lat=43, lon=-81, height=300),
        mid_obs_time_jd=Time("2024-10-01 18:19:13"),
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


def test_satellites_above_horizon():
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
        location=EarthLocation(lat=43, lon=-81, height=300),
        julian_dates=[Time("2024-10-01 18:19:13")],
    )

    assert len(result["data"]) == 1
    assert result["data"][0]["altitude"] > 0

    # Test for satellite above horizon but below minimum altitude
    result = get_satellites_above_horizon(
        tle_repo,
        location=EarthLocation(lat=43, lon=-81, height=300),
        julian_dates=[Time("2024-10-01 18:19:13")],
        min_altitude=30,
    )

    assert len(result["data"]) == 0

    # Test for satellite below horizon
    result = get_satellites_above_horizon(
        tle_repo,
        location=EarthLocation(lat=43, lon=-81, height=300),
        julian_dates=[Time("2024-10-01 15:19:13")],
        min_altitude=0,
    )

    assert len(result["data"]) == 0
