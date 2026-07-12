# ruff: noqa: S101
import logging
from datetime import datetime, timedelta, timezone

import pytest
from astropy.coordinates import EarthLocation
from astropy.time import Time
from skyfield.api import EarthSatellite, load
from tests.conftest import (
    FakeEphemerisRepository,
    FakeOrbitalElementsRepository,
    FakeTdmPredictionRepository,
    FakeTLERepository,
)
from tests.factories.orbital_elements_factory import OrbitalElementsFactory
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tdm_prediction_factory import (
    TdmPredictionFactory,
    TdmPredictionPointFactory,
)
from tests.factories.tle_factory import TLEFactory

from api.services import fov_service
from api.services.fov_service import (
    get_satellite_passes_in_fov,
    get_satellite_passes_in_fov_async,
    get_satellite_passes_in_fov_tdm,
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
        epoch=test_time.to_datetime(timezone.utc),
    )

    tle_repo = FakeTLERepository([tle])
    orbital_elements_repo = FakeOrbitalElementsRepository([])
    ephemeris_repo = FakeEphemerisRepository([])

    # Test with group_by=satellite
    result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=24.797270,
        dec=75.774139,
        fov_radius=1.66,
        group_by="satellite",
        include_tles=False,
        skip_cache=False,
        constellation=None,
        data_source="any",
        illuminated_only=False,
        tle_only=False,
        use_generated_tles=False,
        api_source="test",
        api_version="1.0",
    )

    assert len(result["data"]["satellites"]) == 1
    assert result["data"]["total_position_results"] == 18

    # Test with group_by=time
    result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=24.797270,
        dec=75.774139,
        fov_radius=1.66,
        group_by="time",
        include_tles=False,
        skip_cache=False,
        constellation=None,
        data_source=None,
        illuminated_only=False,
        tle_only=False,
        use_generated_tles=False,
        api_source="test",
        api_version="1.0",
    )

    assert result["total_position_results"] == 18
    assert result["data"][0]["norad_id"] == 31746
    assert result["data"][0]["range_km"] > 0
    assert result["data"][0]["altitude"] is not None
    assert result["data"][0]["azimuth"] is not None
    assert result["data"][0]["angle"] >= 0
    assert result["data"][0]["julian_date"] is not None
    assert result["data"][0]["name"] == "FENGYUN 1C DEB"
    assert result["data"][0]["orbital_data_epoch"] is not None
    assert result["data"][0]["ra"] == pytest.approx(21.23511431, rel=1e-9)
    assert result["data"][0]["dec"] is not None
    with pytest.raises(KeyError):
        assert result["data"][0]["tle_data"]

    # Test with group_by=time and include_tles=True
    result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=24.797270,
        dec=75.774139,
        fov_radius=2.0,
        group_by="time",
        include_tles=True,
        skip_cache=False,
        constellation=None,
        data_source=None,
        illuminated_only=False,
        tle_only=False,
        use_generated_tles=False,
        api_source="test",
        api_version="1.0",
    )

    assert result["data"][0]["tle_data"]["tle_line1"] == tle.tle_line1
    assert result["data"][0]["tle_data"]["tle_line2"] == tle.tle_line2

    # Test with group_by=satellite and include_tles=True
    result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=24.797270,
        dec=75.774139,
        fov_radius=2.5,
        group_by="satellite",
        include_tles=True,
        skip_cache=False,
        constellation=None,
        data_source="any",
        illuminated_only=False,
        tle_only=False,
        use_generated_tles=False,
        api_source="test",
        api_version="1.0",
    )
    # Get the first satellite key
    satellite_key = list(result["data"]["satellites"].keys())[0]
    assert (
        result["data"]["satellites"][satellite_key]["tle_data"]["tle_line1"]
        == tle.tle_line1
    )
    assert (
        result["data"]["satellites"][satellite_key]["tle_data"]["tle_line2"]
        == tle.tle_line2
    )


def _fengyun_orbital_elements(satellite, epoch):
    """OrbitalElements with the same mean elements as the FENGYUN 1C DEB TLE
    used elsewhere in this file, so both propagation paths describe the same
    physical orbit."""
    return OrbitalElementsFactory(
        satellite=satellite,
        epoch=epoch,
        date_collected=epoch,
        data_source="celestrak",
        classification_type="U",
        mean_motion=14.52723026,
        eccentricity=0.0030132,
        inclination=98.5847,
        ra_of_ascending_node=13.2387,
        arg_of_pericenter=143.9377,
        mean_anomaly=216.3858,
        bstar=0.86550e-2,
        mean_motion_dot=0.00035853,
        mean_motion_ddot=0.0,
        rev_at_epoch=90668,
        ephemeris_type=0,
        element_set_no=999,
    )


def test_satellite_in_fov_orbital_elements_after_cutoff(test_location):
    """
    Regression test for the OMM/orbital-elements sync FOV path
    (time_param >= ORBITAL_ELEMENTS_CUTOFF).
    """
    omm_time = Time("2026-08-01T18:19:13", format="isot", scale="utc")

    satellite = SatelliteFactory(
        sat_name="FENGYUN 1C DEB",
        sat_number=31746,
        decay_date=None,
        has_current_sat_number=True,
    )
    orbital_elements = _fengyun_orbital_elements(
        satellite, omm_time.to_datetime(timezone.utc)
    )

    tle_repo = FakeTLERepository([])
    orbital_elements_repo = FakeOrbitalElementsRepository([orbital_elements])
    ephemeris_repo = FakeEphemerisRepository([])

    result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        location=test_location,
        mid_obs_time_jd=omm_time,
        start_time_jd=None,
        duration=30,
        ra=353.68,
        dec=-22.18,
        fov_radius=1.0,
        group_by="satellite",
        include_tles=False,
        skip_cache=True,
        constellation=None,
        data_source="any",
        illuminated_only=False,
        tle_only=False,
        use_generated_tles=False,
        api_source="test",
        api_version="1.0",
    )

    assert len(result["data"]["satellites"]) == 1
    satellite_key = list(result["data"]["satellites"].keys())[0]
    assert result["data"]["satellites"][satellite_key]["norad_id"] == 31746
    assert len(result["data"]["satellites"][satellite_key]["positions"]) == 30
    # Same mean elements as the TLE in test_satellite_in_fov (different epoch/
    # FOV geometry), so this is a different value -- it's here to confirm the
    # orbital-elements path produces a real, stable propagated position.
    first_position = result["data"]["satellites"][satellite_key]["positions"][0]
    assert first_position["ra"] == pytest.approx(353.73939585, rel=1e-9)


def test_tle_and_orbital_elements_propagation_match(test_location, test_time):
    """
    Cross-check that the TLE path and the orbital-elements path produce the
    same sky position for the same underlying orbit.

    ORBITAL_ELEMENTS_CUTOFF is patched so both calls
    use the identical mid_obs_time_jd -- otherwise the two paths would also
    differ in Earth's rotation state at observation time, confounding the
    comparison.
    """
    tle_line1 = "1 31746U 99025CEV 24275.73908890  .00035853  00000-0  86550-2 0  9990"  # noqa: E501
    tle_line2 = "2 31746  98.5847  13.2387 0030132 143.9377 216.3858 14.52723026906685"  # noqa: E501
    ts = load.timescale()
    tle_epoch = EarthSatellite(tle_line1, tle_line2, ts=ts).epoch.utc_datetime()

    satellite = SatelliteFactory(
        sat_name="FENGYUN 1C DEB",
        sat_number=31746,
        decay_date=None,
        has_current_sat_number=True,
    )
    tle = TLEFactory(
        satellite=satellite,
        tle_line1=tle_line1,
        tle_line2=tle_line2,
        epoch=tle_epoch,
    )
    orbital_elements = _fengyun_orbital_elements(satellite, tle_epoch)

    common_args = dict(
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=24.797270,
        dec=75.774139,
        fov_radius=1.66,
        group_by="time",
        include_tles=False,
        skip_cache=True,
        constellation=None,
        data_source="any",
        illuminated_only=False,
        tle_only=False,
        use_generated_tles=False,
        api_source="test",
        api_version="1.0",
    )

    result_tle = get_satellite_passes_in_fov(
        FakeTLERepository([tle]),
        FakeOrbitalElementsRepository([]),
        FakeEphemerisRepository([]),
        **common_args,
    )

    original_cutoff = fov_service.ORBITAL_ELEMENTS_CUTOFF
    fov_service.ORBITAL_ELEMENTS_CUTOFF = datetime(2020, 1, 1, tzinfo=timezone.utc)
    try:
        result_omm = get_satellite_passes_in_fov(
            FakeTLERepository([]),
            FakeOrbitalElementsRepository([orbital_elements]),
            FakeEphemerisRepository([]),
            **common_args,
        )
    finally:
        fov_service.ORBITAL_ELEMENTS_CUTOFF = original_cutoff

    assert result_tle["total_position_results"] == 18
    assert result_omm["total_position_results"] == result_tle["total_position_results"]

    for tle_point, omm_point in zip(
        result_tle["data"], result_omm["data"], strict=True
    ):
        assert omm_point["ra"] == pytest.approx(tle_point["ra"], abs=1e-4)
        assert omm_point["dec"] == pytest.approx(tle_point["dec"], abs=1e-4)


def test_get_satellite_passes_in_fov_async_orbital_elements_after_cutoff(test_location):
    """
    Regression test for the OMM/orbital-elements async FOV path.
    """
    from api.celery_app import celery
    from api.services.tasks.fov_tasks import (
        aggregate_fov_results_task,
        get_fov_task_status,
        process_satellite_batch_task,
        refine_with_ephemeris_task,
    )

    omm_time = Time("2026-08-01T18:19:13", format="isot", scale="utc")

    satellite = SatelliteFactory(
        sat_name="FENGYUN 1C DEB",
        sat_number=31746,
        decay_date=None,
        has_current_sat_number=True,
    )
    orbital_elements = _fengyun_orbital_elements(
        satellite, omm_time.to_datetime(timezone.utc)
    )

    tle_repo = FakeTLERepository([])
    orbital_elements_repo = FakeOrbitalElementsRepository([orbital_elements])

    eager_tasks = (
        process_satellite_batch_task,
        aggregate_fov_results_task,
        refine_with_ephemeris_task,
    )

    original_always_eager = celery.conf.task_always_eager
    original_eager_propagates = celery.conf.task_eager_propagates
    original_store_eager_result = celery.conf.task_store_eager_result
    original_task_store_eager_results = [t.store_eager_result for t in eager_tasks]
    celery.conf.task_always_eager = True
    celery.conf.task_eager_propagates = True
    celery.conf.task_store_eager_result = True
    for task in eager_tasks:
        task.store_eager_result = True
    try:
        dispatch_result = get_satellite_passes_in_fov_async(
            tle_repo,
            orbital_elements_repo,
            location=test_location,
            mid_obs_time_jd=omm_time,
            start_time_jd=None,
            duration=30,
            ra=353.68,
            dec=-22.18,
            fov_radius=1.0,
            group_by="satellite",
            include_tles=False,
            skip_cache=True,
            constellation=None,
            data_source="any",
            illuminated_only=False,
            tle_only=True,
            use_generated_tles=False,
            api_source="test",
            api_version="1.0",
        )
        assert dispatch_result["status"] == "PENDING"
        assert dispatch_result["task_id"] is not None

        status = get_fov_task_status(dispatch_result["task_id"])
    finally:
        celery.conf.task_always_eager = original_always_eager
        celery.conf.task_eager_propagates = original_eager_propagates
        celery.conf.task_store_eager_result = original_store_eager_result
        for task, original in zip(
            eager_tasks, original_task_store_eager_results, strict=True
        ):
            task.store_eager_result = original

    assert status["status"] == "SUCCESS"
    satellites = status["data"]["satellites"]
    assert len(satellites) == 1
    satellite_key = list(satellites.keys())[0]
    assert satellites[satellite_key]["norad_id"] == 31746

    positions = satellites[satellite_key]["positions"]
    assert len(positions) == 30
    assert positions[0]["ra"] == pytest.approx(353.73939585, rel=1e-9)
    assert all(p["orbital_data_source"] == "omm" for p in positions)


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
        epoch=test_time.to_datetime(timezone.utc),
    )

    tle_repo = FakeTLERepository([tle])
    orbital_elements_repo = FakeOrbitalElementsRepository([])
    ephemeris_repo = FakeEphemerisRepository([])

    result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=48.797270,
        dec=75.774139,
        fov_radius=2.0,
        group_by="satellite",
        include_tles=False,
        skip_cache=False,
        constellation=None,
        data_source="any",
        illuminated_only=False,
        tle_only=False,
        use_generated_tles=False,
        api_source="test",
        api_version="1.0",
    )

    assert len(result["data"]["satellites"]) == 0
    assert result["data"]["total_position_results"] == 0


def test_fov_service_uses_ephemeris(starlink_ephemeris):
    """Service call uses ephemeris refinement when both TLE and ephemeris exist."""
    satellite = SatelliteFactory(
        sat_name="STARLINK-31570",
        sat_number=59324,
        decay_date=None,
        has_current_sat_number=True,
    )
    # TLE from production matching STARLINK-31570 at 2025-10-10 19:07:42 UTC
    # to match the ephemeris fixture data
    tle = TLEFactory(
        satellite=satellite,
        tle_line1="1 59324C 24057E   25283.79701389  .00003769  00000+0  13645-3 0  2837",  # noqa: E501
        tle_line2="2 59324  43.0040 313.9787 0001364 274.5572 329.6279 15.27588869    18",  # noqa: E501
        epoch=datetime(2025, 10, 10, 19, 7, 42, tzinfo=timezone.utc),
    )

    tle_repo = FakeTLERepository([tle])
    orbital_elements_repo = FakeOrbitalElementsRepository([])
    ephemeris_repo = FakeEphemerisRepository([starlink_ephemeris])
    location = EarthLocation(lat=-0.808, lon=-1.084, height=0)
    obs_time = Time(2460959.317847, format="jd", scale="utc")

    result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        location=location,
        mid_obs_time_jd=obs_time,
        start_time_jd=None,
        duration=30,
        ra=312.6525015,
        dec=-0.9114941,
        fov_radius=180.0,
        group_by="time",
        include_tles=False,
        skip_cache=True,
        constellation=None,
        data_source=None,
        illuminated_only=False,
        tle_only=False,
        use_generated_tles=False,
        api_source="test",
        api_version="1.0",
    )

    assert result["total_position_results"] > 0
    starlink_results = [row for row in result["data"] if row["norad_id"] == 59324]
    assert len(starlink_results) > 0
    assert all(row["orbital_data_source"] == "ephemeris" for row in starlink_results)

    tle_only_result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        location=location,
        mid_obs_time_jd=obs_time,
        start_time_jd=None,
        duration=30,
        ra=312.6525015,
        dec=-0.9114941,
        fov_radius=180.0,
        group_by="time",
        include_tles=False,
        skip_cache=True,
        constellation=None,
        data_source=None,
        illuminated_only=False,
        tle_only=True,
        use_generated_tles=False,
        api_source="test",
        api_version="1.0",
    )

    assert tle_only_result["total_position_results"] > 0
    tle_starlink_results = [
        row for row in tle_only_result["data"] if row["norad_id"] == 59324
    ]
    assert len(tle_starlink_results) > 0
    assert all(row.get("orbital_data_source") == "tle" for row in tle_starlink_results)


def test_satellite_in_fov_tdm(test_location, test_time):
    """Test when satellite never enters FOV"""
    # Set up with FOV pointing away from orbit - RA changed to 48.797270

    satellite = SatelliteFactory(
        sat_name="FENGYUN 1C DEB",
        sat_number=31746,
        decay_date=None,
        has_current_sat_number=True,
        constellation="starlink",
    )

    tdm_prediction = TdmPredictionFactory(
        satellite=satellite,
        creation_date=test_time,
        time_range_start=test_time - timedelta(minutes=2),
        time_range_end=test_time + timedelta(minutes=2),
    )

    point = TdmPredictionPointFactory(
        tdm_prediction_id=tdm_prediction.id,
        timestamp=test_time + timedelta(seconds=15),
        right_ascension=48.797270,
        declination=75.774139,
        apparent_magnitude=10.0,
        satellite_number=31746,
        satellite_name="FENGYUN 1C DEB",
    )
    tdm_repo = FakeTdmPredictionRepository(
        tdm_prediction_points=[point], tdm_predictions=[tdm_prediction]
    )

    result = get_satellite_passes_in_fov_tdm(
        tdm_repo,
        site="LSST",
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=48.797270,
        dec=75.774139,
        fov_radius=2.0,
        group_by="satellite",
        constellation="starlink",
        api_source="test",
        api_version="1.0",
    )

    assert len(result["data"]["satellites"]) == 0
    assert result["data"]["total_position_results"] == 0


def test_satellite_outside_fov_tdm(test_location, test_time):
    """Test when satellite never enters FOV"""
    # Set up with FOV pointing away from orbit - RA changed to 48.797270

    satellite = SatelliteFactory(
        sat_name="FENGYUN 1C DEB",
        sat_number=31746,
        decay_date=None,
        has_current_sat_number=True,
    )

    tdm_prediction = TdmPredictionFactory(
        satellite=satellite,
        creation_date=test_time,
    )

    point = TdmPredictionPointFactory(
        tdm_prediction_id=tdm_prediction.id,
        timestamp=test_time + timedelta(minutes=1),
        right_ascension=40.797270,
        declination=72.774139,
        apparent_magnitude=10.0,
        satellite_number=31746,
        satellite_name="FENGYUN 1C DEB",
    )
    tdm_repo = FakeTdmPredictionRepository(
        tdm_prediction_points=[point], tdm_predictions=[tdm_prediction]
    )

    result = get_satellite_passes_in_fov_tdm(
        tdm_repo,
        site="test",
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=48.797270,
        dec=75.774139,
        fov_radius=2.0,
        group_by="satellite",
        constellation="starlink",
        api_source="test",
        api_version="1.0",
    )

    assert len(result["data"]["satellites"]) == 0
    assert result["data"]["total_position_results"] == 0


def test_empty_tle_list(test_location, test_time):
    """Test behavior with no TLEs available"""
    tle_repo = FakeTLERepository([])
    orbital_elements_repo = FakeOrbitalElementsRepository([])
    ephemeris_repo = FakeEphemerisRepository([])

    result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        location=test_location,
        mid_obs_time_jd=test_time,
        start_time_jd=None,
        duration=30,
        ra=48.797270,
        dec=75.774139,
        fov_radius=2.0,
        group_by="satellite",
        include_tles=False,
        skip_cache=False,
        constellation=None,
        data_source=None,
        illuminated_only=False,
        tle_only=False,
        use_generated_tles=False,
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
        constellation="starlink",
    )

    tle = TLEFactory(
        satellite=satellite,
        tle_line1="1 31746U 99025CEV 24275.73908890  .00035853  00000-0  86550-2 0  9990",  # noqa: E501
        tle_line2="2 31746  98.5847  13.2387 0030132 143.9377 216.3858 14.52723026906685",  # noqa: E501
        epoch=test_time.to_datetime(timezone.utc),
    )

    tle_repo = FakeTLERepository([tle])
    orbital_elements_repo = FakeOrbitalElementsRepository([])

    result = get_satellites_above_horizon(
        tle_repo,
        orbital_elements_repo,
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
        orbital_elements_repo,
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
        orbital_elements_repo,
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
        orbital_elements_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=0,
        max_range=1000,
    )

    assert len(result["data"]) == 0

    result = get_satellites_above_horizon(
        tle_repo,
        orbital_elements_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=1000,
        max_range=1500000,
    )

    assert len(result["data"]) == 1

    result = get_satellites_above_horizon(
        tle_repo,
        orbital_elements_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=1500,
        max_range=1500000,
    )

    assert len(result["data"]) == 0

    result = get_satellites_above_horizon(
        tle_repo,
        orbital_elements_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=1000,
        max_range=1500000,
        constellation="starlink",
    )

    assert len(result["data"]) == 1

    result = get_satellites_above_horizon(
        tle_repo,
        orbital_elements_repo,
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=1000,
        max_range=1500000,
        constellation="oneweb",
    )

    assert len(result["data"]) == 0


def test_tle_and_orbital_elements_above_horizon_match(test_location, test_time):
    """
    Cross-check that the TLE path and the orbital-elements path produce the
    same sky position for get_satellites_above_horizon, for the same
    underlying orbit.

    ORBITAL_ELEMENTS_CUTOFF is patched so both calls use the identical
    julian_dates -- otherwise the two paths would also differ in Earth's
    rotation state at observation time.
    """
    tle_line1 = "1 31746U 99025CEV 24275.73908890  .00035853  00000-0  86550-2 0  9990"  # noqa: E501
    tle_line2 = "2 31746  98.5847  13.2387 0030132 143.9377 216.3858 14.52723026906685"  # noqa: E501
    ts = load.timescale()
    tle_epoch = EarthSatellite(tle_line1, tle_line2, ts=ts).epoch.utc_datetime()

    satellite = SatelliteFactory(
        sat_name="FENGYUN 1C DEB",
        sat_number=31746,
        decay_date=None,
        has_current_sat_number=True,
        constellation="starlink",
    )
    tle = TLEFactory(
        satellite=satellite,
        tle_line1=tle_line1,
        tle_line2=tle_line2,
        epoch=tle_epoch,
    )
    orbital_elements = _fengyun_orbital_elements(satellite, tle_epoch)

    common_args = dict(
        location=test_location,
        julian_dates=[test_time],
        min_altitude=0,
        min_range=0,
        max_range=1500000,
    )

    result_tle = get_satellites_above_horizon(
        FakeTLERepository([tle]),
        FakeOrbitalElementsRepository([]),
        **common_args,
    )

    original_cutoff = fov_service.ORBITAL_ELEMENTS_CUTOFF
    fov_service.ORBITAL_ELEMENTS_CUTOFF = datetime(2020, 1, 1, tzinfo=timezone.utc)
    try:
        result_omm = get_satellites_above_horizon(
            FakeTLERepository([]),
            FakeOrbitalElementsRepository([orbital_elements]),
            **common_args,
        )
    finally:
        fov_service.ORBITAL_ELEMENTS_CUTOFF = original_cutoff

    assert len(result_tle["data"]) == 1
    assert len(result_omm["data"]) == len(result_tle["data"])

    tle_point = result_tle["data"][0]
    omm_point = result_omm["data"][0]

    assert tle_point["orbital_data_source"] == "tle"
    assert omm_point["orbital_data_source"] == "omm"
    assert omm_point["ra"] == pytest.approx(tle_point["ra"], abs=1e-4)
    assert omm_point["dec"] == pytest.approx(tle_point["dec"], abs=1e-4)
    assert omm_point["altitude"] == pytest.approx(tle_point["altitude"], abs=1e-4)
    assert omm_point["azimuth"] == pytest.approx(tle_point["azimuth"], abs=1e-4)
    assert omm_point["range_km"] == pytest.approx(tle_point["range_km"], abs=1e-2)


@pytest.mark.skip(reason="Caching is temporarily disabled")
def test_fov_caching_cycle(mocker, test_location, test_time):
    """Test the complete caching cycle: miss, compute, store, then hit."""
    # Create a simple dictionary to act as our cache storage
    fake_cache = {}

    def mock_get(key):
        return fake_cache.get(key)

    def mock_setex(key, expiry, value):
        fake_cache[key] = value
        return True

    # Mock redis_client in cache_service instead of fov_service
    mock_redis_client = mocker.patch("api.services.cache_service.redis_client")
    mock_redis_client.get.side_effect = mock_get
    mock_redis_client.setex.side_effect = mock_setex

    tle_repo = FakeTLERepository([])
    orbital_elements_repo = FakeOrbitalElementsRepository([])
    ephemeris_repo = FakeEphemerisRepository([])
    # First call - should compute and cache (cache miss)
    first_result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        test_location,
        None,
        test_time,
        3600,
        100.0,
        -20.0,
        10.0,
        "time",
        False,
        False,
        None,
        None,
        "test",
        "v1",
    )

    # Verify result was computed and cached
    assert len(fake_cache) == 1  # Something was stored in cache
    # TODO: 1 for cache miss + 1 for verification - revert later
    assert mock_redis_client.get.call_count == 2
    assert mock_redis_client.setex.call_count == 1
    assert "from_cache" not in first_result["performance"]

    # Get the cache key for later verification
    cache_key = mock_redis_client.get.call_args[0][0]  # noqa: F841

    # Second call with same parameters - should use cache (cache hit)
    mock_redis_client.reset_mock()  # Reset call counts

    second_result = get_satellite_passes_in_fov(  # noqa: F841
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        test_location,
        None,
        test_time,
        3600,
        100.0,
        -20.0,
        10.0,
        "time",
        False,
        False,
        None,
        None,
        "test",
        "v1",
    )

    # TODO: resolve caching issue
    """
    # Verify cache was used
    assert mock_redis_client.get.call_count == 1
    assert mock_redis_client.setex.call_count == 0  # No new caching
    assert second_result["performance"]["from_cache"] is True

    # Results should match
    assert second_result["data"] == first_result["data"]

    # Same cache key should be used
    assert mock_redis_client.get.call_args[0][0] == cache_key
    """

    # Third call with skip_cache=True - should compute and cache (cache miss)
    mock_redis_client.reset_mock()  # Reset call counts

    third_result = get_satellite_passes_in_fov(
        tle_repo,
        orbital_elements_repo,
        ephemeris_repo,
        test_location,
        None,
        test_time,
        3600,
        100.0,
        -20.0,
        10.0,
        "time",
        False,
        True,  # skip_cache=True
        None,
        None,
        "test",
        "v1",
    )

    assert "from_cache" not in third_result["performance"]

    # Results should match
    assert third_result["data"] == first_result["data"]


@pytest.mark.skip(reason="TODO: Re-enable once caching is properly implemented")
def test_fov_cache_key_consistency(mocker, test_location, test_time):
    """Test that the same parameters generate the same cache key."""
    # Use a set to collect and compare cache keys
    cache_keys = set()

    mock_redis_client = mocker.patch("api.services.cache_service.redis_client")
    mock_redis_client.get.return_value = None

    tle_repo = FakeTLERepository([])
    orbital_elements_repo = FakeOrbitalElementsRepository([])
    ephemeris_repo = FakeEphemerisRepository([])
    # Make multiple identical calls and collect cache keys
    for _ in range(3):
        get_satellite_passes_in_fov(
            tle_repo,
            orbital_elements_repo,
            ephemeris_repo,
            test_location,
            None,
            test_time,
            3600,
            100.0,
            -20.0,
            10.0,
            "time",
            False,
            False,
            None,
            None,
            "test",
            "v1",
        )
        cache_keys.add(mock_redis_client.get.call_args[0][0])
        mock_redis_client.reset_mock()

    # If all keys are identical, the set will have only one element
    assert len(cache_keys) == 1


@pytest.mark.skip(reason="TODO: Re-enable once caching is properly implemented")
def test_fov_different_cache_keys(mocker, test_location, test_time):
    """Test that different parameters generate different cache keys."""
    mock_redis_client = mocker.patch("api.services.cache_service.redis_client")
    mock_redis_client.get.return_value = None

    tle_repo = FakeTLERepository([])
    orbital_elements_repo = FakeOrbitalElementsRepository([])
    ephemeris_repo = FakeEphemerisRepository([])
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
        orbital_elements_repo,
        ephemeris_repo,
        test_location,
        None,
        test_time,
        3600,
        100.0,
        -20.0,
        10.0,
        "time",
        False,
        False,
        None,
        None,
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
            "orbital_elements_repo": orbital_elements_repo,
            "ephemeris_repo": ephemeris_repo,
            "location": test_location,
            "start_time_jd": None,
            "mid_obs_time_jd": test_time,
            "duration": 3600,
            "ra": 100.0,
            "dec": -20.0,
            "fov_radius": 10.0,
            "group_by": "time",
            "include_tles": False,
            "skip_cache": False,
            "constellation": None,
            "data_source": None,
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
