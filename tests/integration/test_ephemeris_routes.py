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
def test_get_ephemeris_by_name(client, session):
    satellite = SatelliteFactory(sat_name="ISS")
    tle = TLEFactory(satellite=satellite)
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    response = client.get(
        "/ephemeris/name/?name=ISS&latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 200


@pytest.mark.skipif(cannot_connect_to_services(), reason="Services not available")
def test_get_ephemeris_by_name_jd_step(client, session):
    satellite = SatelliteFactory(sat_name="ISS")
    tle = TLEFactory(satellite=satellite)
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()  # Commit to ensure data is saved

    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS&latitude=0&longitude=0&elevation=0"
        "&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 200


@pytest.mark.skipif(cannot_connect_to_services(), reason="Services not available")
def test_get_ephemeris_by_catalog_number(client, session):
    satellite = SatelliteFactory(sat_number="25544")
    tle = TLEFactory(satellite=satellite)
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 200


@pytest.mark.skipif(cannot_connect_to_services(), reason="Services not available")
def test_get_ephemeris_by_catalog_number_jdstep(client, session):
    satellite = SatelliteFactory(sat_number="25544")
    tle = TLEFactory(satellite=satellite)
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 200


@pytest.mark.skipif(cannot_connect_to_services(), reason="Services not available")
def test_get_ephemeris_no_tle(client):
    response = client.get(
        "/ephemeris/name/?name=ISS&latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 500
    assert "No TLE found" in response.text

    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 500
    assert "No TLE found" in response.text

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 500
    assert "No TLE found" in response.text

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 500
    assert "No TLE found" in response.text


@pytest.mark.skipif(cannot_connect_to_services(), reason="Services not available")
def test_get_ephemeris_data_from_tle(client):
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        f"/ephemeris/tle/?elevation=150&latitude=32&longitude=-110\
            &julian_date=2459000.5&tle={tle}"
    )
    assert response.status_code == 200


@pytest.mark.skipif(cannot_connect_to_services(), reason="Services not available")
def test_get_ephemeris_data_from_tle_jdstep(client):
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        f"/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&startjd=2459000.5&stopjd=2459001.5&stepjd=.5&tle={tle}"
    )
    assert response.status_code == 200


def test_get_ephemeris_missing_parameter(client):
    # Missing 'latitude' parameter
    response = client.get(
        "/ephemeris/name/?name=ISS&longitude=0&elevation=0&julian_date=2459000.5"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Incorrect parameters" in response.text

    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Incorrect parameters" in response.text

    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&longitude=0&elevation=0&julian_date=2459000.5"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Incorrect parameters" in response.text

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Incorrect parameters" in response.text

    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        f"/ephemeris/tle/?elevation=150&longitude=-110&julian_date=2459000.5&tle={tle}"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Incorrect parameters" in response.text

    response = client.get(
        f"/ephemeris/tle-jdstep/?elevation=150&longitude=-110\
            &startjd=2460193.1&startjd=2459000.5&stopjd=2459001.5&stepjd=.5&tle={tle}"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Incorrect parameters" in response.text


def test_get_ephemeris_by_tle_incorrect_format(client):
    tle = "tle"
    response = client.get(
        f"/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&startjd=2459000.5&stopjd=2459001.5&stepjd=.5&tle={tle}"
    )
    assert response.status_code == 500
    assert "Invalid TLE format" in response.text
