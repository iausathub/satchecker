import pytest
import api.core

def test_index_redirect(client):
    response = client.get("/index")
    # Check that there was one redirect response.
    assert response.status_code == 302
    # Check that the redirect was to the correct location.
    assert response.location == "https://satchecker.readthedocs.io/en/latest/"


def test_missing_parameter(client):
    response = client.get("/ephemeris/name/?name=test_sat&elevation=150&latitude=32&longitude=-110")
    # Check that the correct error code was returned.
    assert response.status_code == 400
    assert response.text.find("Incorrect parameters") != -1

def test_missing_data(client, mocker):
    mocker.patch.object(api.core.routes,"get_TLE_by_name", return_value=(None, None))
    response = client.get("/ephemeris/name/?name=test_sat123&elevation=150&latitude=32&longitude=-110&julian_date=2459000.5")
    # Check that the correct error code was returned.
    assert response.status_code == 500
    assert response.text.find("No TLE found") != -1

def test_incorrect_TLE(client):
    tle = "ISS (ZARYA) \\n 1 25544U 98067A   23248.54842295  .00012769  00000+0  \\n2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get("/ephemeris/tle/?elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&tle=" + tle)
    # Check that the correct error code was returned.
    assert response.status_code == 500
    assert response.text.find("Incorrect TLE format") != -1


