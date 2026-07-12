# ruff: noqa: S101
import pytest
from tests.conftest import FakeEphemerisRepository

from api.utils.propagation_strategies import KroghPropagationStrategy

# Observer at the sub-satellite point of STARLINK-31570 at index 30 of the
# fixture ephemeris (2025-10-10 19:37:42 UTC). Placing the observer directly
# below guarantees the satellite is overhead regardless of FOV orientation.
# Derived by running find_fov_params.py against the full MEME file.
TEST_JD = 2460959.317847  # 2025-10-10 19:37:42 UTC
OBSERVER_LAT = -0.808  # degrees
OBSERVER_LON = -1.084  # degrees
OBSERVER_ELEV = 0.0  # metres


@pytest.fixture(scope="module")
def loaded_krogh_strategy(starlink_ephemeris):
    """KroghPropagationStrategy with STARLINK-31570 ephemeris already loaded.

    Module-scoped to avoid repeating the expensive sigma-point and spline
    generation (O(n_points)) for every test.
    """
    strategy = KroghPropagationStrategy()
    repo = FakeEphemerisRepository([starlink_ephemeris])
    strategy.load_ephemeris(starlink_ephemeris, repo)
    return strategy


def test_sigma_points_generated(loaded_krogh_strategy, starlink_ephemeris):
    """Sigma points are created for every ephemeris time step."""
    assert loaded_krogh_strategy.sigma_points_dict is not None
    assert len(loaded_krogh_strategy.sigma_points_dict) == len(
        starlink_ephemeris.points
    )


def test_interpolated_splines_created(loaded_krogh_strategy):
    """Krogh splines are built for position and velocity components."""
    splines = loaded_krogh_strategy.interpolated_splines
    assert splines is not None
    assert "positions" in splines
    assert "velocities" in splines
    assert "time_range" in splines


def test_spline_time_range_covers_ephemeris(loaded_krogh_strategy, starlink_ephemeris):
    """Spline time range spans the full ephemeris window."""
    import julian

    time_range = loaded_krogh_strategy.interpolated_splines["time_range"]
    start_jd = julian.to_jd(starlink_ephemeris.ephemeris_start)
    stop_jd = julian.to_jd(starlink_ephemeris.ephemeris_stop)
    assert time_range[0] <= start_jd
    assert time_range[1] >= stop_jd


def test_propagate_returns_one_result_per_jd(loaded_krogh_strategy):
    """propagate() returns exactly one result for a single JD inside the ephemeris."""
    results = loaded_krogh_strategy.propagate(
        TEST_JD,
        None,
        latitude=OBSERVER_LAT,
        longitude=OBSERVER_LON,
        elevation=OBSERVER_ELEV,
    )
    assert len(results) == 1


def test_propagated_position_has_valid_ra_dec(loaded_krogh_strategy):
    """Each propagated position carries a valid RA and Dec."""
    results = loaded_krogh_strategy.propagate(
        TEST_JD,
        None,
        latitude=OBSERVER_LAT,
        longitude=OBSERVER_LON,
        elevation=OBSERVER_ELEV,
    )
    pos = results[0]
    assert pos.ra == pytest.approx(312.6525015, rel=1e-7)
    assert pos.dec == pytest.approx(-0.9114941, rel=1e-7)


def test_satellite_overhead_at_sub_satellite_point(loaded_krogh_strategy):
    """Observer placed at the sub-satellite point sees the satellite near zenith."""
    results = loaded_krogh_strategy.propagate(
        TEST_JD,
        None,
        latitude=OBSERVER_LAT,
        longitude=OBSERVER_LON,
        elevation=OBSERVER_ELEV,
    )
    assert results[0].altitude is not None
    assert results[0].altitude > 60.0


def test_propagate_multiple_jds(loaded_krogh_strategy):
    """propagate() handles a list of Julian dates."""
    jds = [TEST_JD - 0.005, TEST_JD, TEST_JD + 0.005]  # ~7 min apart
    results = loaded_krogh_strategy.propagate(
        jds,
        None,
        latitude=OBSERVER_LAT,
        longitude=OBSERVER_LON,
        elevation=OBSERVER_ELEV,
    )
    assert len(results) == 3
    for pos in results:
        assert pos.ra is not None
        assert pos.dec is not None


def test_covariance_is_returned(loaded_krogh_strategy):
    """Propagated positions include a 6×6 covariance matrix."""
    results = loaded_krogh_strategy.propagate(
        TEST_JD,
        None,
        latitude=OBSERVER_LAT,
        longitude=OBSERVER_LON,
        elevation=OBSERVER_ELEV,
    )
    cov = results[0].covariance
    assert cov is not None
    assert cov.shape == (6, 6)
    # assert actual values are close to the expected values
    assert cov[0, 0] == pytest.approx(1.7559586242244689e-06, rel=1e-8)
    assert cov[0, 1] == pytest.approx(-3.859641286516257e-06, rel=1e-8)
    assert cov[0, 2] == pytest.approx(0.0, abs=1e-8)
    assert cov[0, 3] == pytest.approx(0.0, abs=1e-8)
    assert cov[0, 4] == pytest.approx(0.0, abs=1e-8)
    assert cov[0, 5] == pytest.approx(0.0, abs=1e-8)
    assert cov[1, 0] == pytest.approx(-3.859641286516257e-06, rel=1e-8)
    assert cov[1, 1] == pytest.approx(1.6439354304807393e-05, rel=1e-8)


def test_raises_without_loaded_ephemeris():
    """propagate() raises ValueError if load_ephemeris was never called."""
    strategy = KroghPropagationStrategy()
    with pytest.raises(ValueError, match="No ephemeris data loaded"):
        strategy.propagate(
            TEST_JD,
            None,
            latitude=OBSERVER_LAT,
            longitude=OBSERVER_LON,
            elevation=OBSERVER_ELEV,
        )
