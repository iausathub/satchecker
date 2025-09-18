# ruff: noqa: E501, S101, F841
import pytest
from tests.factories.satellite_factory import (
    SatelliteDesignationFactory,
    SatelliteFactory,
)
from tests.factories.tle_factory import TLEFactory

from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository


def test_get_satellite_passes_in_fov(client, session, services_available):
    satellite = SatelliteFactory(
        designations=[SatelliteDesignationFactory(sat_name="ISS")]
    )
    tle = TLEFactory(satellite=satellite)
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    response = client.get(
        "/fov/satellite-passes/?latitude=0&longitude=0&elevation=0&mid_obs_time_jd=2459000.5&duration=30&ra=224.048903&dec=78.778084&fov_radius=2&group_by=satellite"
    )
    if response.status_code != 200:
        print(f"Error response: {response.get_data(as_text=True)}")
    assert response.status_code == 200


def test_get_satellite_passes_in_fov_missing_parameters(client, services_available):
    # Missing 'latitude' parameter
    response = client.get(
        "/fov/satellite-passes/?longitude=0&elevation=0&mid_obs_time_jd=2459000.5&duration=30&ra=224.048903&dec=78.778084&fov_radius=2&group_by=satellite"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Missing parameter" in response.text


@pytest.mark.parametrize(
    "min_altitude,constellation,expected_code",
    [
        (0, None, 200),
        (30, None, 200),
        (None, None, 200),
        (0, "starlink", 200),
        (30, "oneweb", 200),
    ],
)
def test_get_satellites_above_horizon(
    client, session, services_available, min_altitude, constellation, expected_code
):
    """Test get_satellites_above_horizon with different minimum altitudes and constellations."""
    # Create a satellite and TLE for testing
    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(sat_name="TEST-SAT", sat_number="12345")
        ],
        decay_date=None,
        constellation=constellation if constellation else "test",
    )
    tle = TLEFactory(satellite=satellite)
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    # Base URL with required parameters
    url = "/fov/satellites-above-horizon/?latitude=0&longitude=0&elevation=0&julian_date=2459000.5"

    # Add min_altitude if provided
    if min_altitude is not None:
        url += f"&min_altitude={min_altitude}"

    # Add constellation if provided
    if constellation is not None:
        url += f"&constellation={constellation}"

    response = client.get(url)
    assert response.status_code == expected_code

    if response.status_code == 200:
        assert "data" in response.json
        assert "total_position_results" in response.json
        assert "source" in response.json
        assert "version" in response.json
        assert "performance" in response.json


def test_get_satellites_above_horizon_missing_parameters(client, services_available):
    """Test get_satellites_above_horizon with missing required parameters."""
    # Test missing elevation parameter
    response = client.get(
        "/fov/satellites-above-horizon/?latitude=0&longitude=0&julian_date=2459000.5"
    )
    assert response.status_code == 400
    assert "Missing parameter" in response.text
