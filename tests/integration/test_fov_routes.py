# ruff: noqa: E501, S101, F841
import pytest
from tests.conftest import cannot_connect_to_services
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason=cannot_connect_to_services() or "Services not available",
)
def test_get_satellite_passes_in_fov(client, session):
    satellite = SatelliteFactory(sat_name="ISS")
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


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason=cannot_connect_to_services() or "Services not available",
)
def test_get_satellite_passes_in_fov_missing_parameters(client):
    # Missing 'latitude' parameter
    response = client.get(
        "/fov/satellite-passes/?longitude=0&elevation=0&mid_obs_time_jd=2459000.5&duration=30&ra=224.048903&dec=78.778084&fov_radius=2&group_by=satellite"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Incorrect parameters" in response.text


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason=cannot_connect_to_services() or "Services not available",
)
def test_get_satellites_above_horizon(client):
    response = client.get(
        "/fov/satellites-above-horizon/?latitude=0&longitude=0&elevation=0&julian_date=2459000.5&min_altitude=0"
    )
    assert response.status_code == 200

    response = client.get(
        "/fov/satellites-above-horizon/?latitude=0&longitude=0&elevation=0&julian_date=2459000.5&min_altitude=30"
    )
    assert response.status_code == 200

    response = client.get(
        "/fov/satellites-above-horizon/?latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 200


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason=cannot_connect_to_services() or "Services not available",
)
def test_get_satellites_above_horizon_missing_parameters(client):
    response = client.get(
        "/fov/satellites-above-horizon/?latitude=0&longitude=0&julian_date=2459000.5"
    )
    assert response.status_code == 400
    assert "Incorrect parameters" in response.text
