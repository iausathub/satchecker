# ruff: noqa: S101
import datetime
from collections import namedtuple

import pytest

from api.core import routes

assert_precision = 0.000001


def test_get_ephemeris_by_name(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110\
            &julian_date=2460193.104167&min_altitude=-90"
    )

    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert_single_jd(data)


def test_get_ephemeris_by_name_jdstep(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32\
            &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&min_altitude=-90"
    )

    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert_jd_step(data)


def test_get_ephemeris_by_catalog_number(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90"
    )

    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert_single_jd(data)


def test_get_ephemeris_by_catalog_number_jdstep(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32\
        &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&min_altitude=-90"
    )

    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert_jd_step(data)


def test_get_ephemeris_by_tle(client, mocker):
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        "/ephemeris/tle/?elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167\
            &min_altitude=-90&tle="
        + tle
    )

    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert_single_jd(data)


def test_get_ephemeris_by_tle_jdstep(client):
    tle = "ISS (ZARYA) \\n\
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        "/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&min_altitude=-90&tle="
        + tle
    )

    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert_jd_step(data)


def test_min_max_alt_name(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110\
            &julian_date=2460193.104167"
    )

    # Check that the response was correct
    data = response.json
    assert data == {"info": "No position information found with this criteria"}

    response = client.get(
        "/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110\
            &julian_date=2460193.104167&min_altitude=-90"
    )
    # Check that the response was correct
    data = response.json
    assert_single_jd(data)


def test_min_max_alt_name_jdstep(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32\
            &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1"
    )

    # Check that the response was correct
    data = response.json
    assert data == {"info": "No position information found with this criteria"}

    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32\
            &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&min_altitude=-90"
    )
    # Check that the response was correct
    data = response.json
    assert_jd_step(data)


def test_min_max_alt_catalog(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110\
            &julian_date=2460193.104167"
    )

    # Check that the response was correct
    data = response.json
    assert data == {"info": "No position information found with this criteria"}

    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110\
            &julian_date=2460193.104167&min_altitude=-90"
    )
    # Check that the response was correct
    data = response.json
    assert_single_jd(data)


def test_min_max_alt_catalog_jdstep(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32\
        &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1"
    )

    # Check that the response was correct
    data = response.json
    assert data == {"info": "No position information found with this criteria"}

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32\
        &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&min_altitude=-90"
    )
    # Check that the response was correct
    data = response.json
    assert_jd_step(data)


def test_min_max_alt_tle(client, mocker):
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        "/ephemeris/tle/?elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&tle="
        + tle
    )

    # Check that the response was correct
    data = response.json
    assert data == {"info": "No position information found with this criteria"}

    response = client.get(
        "/ephemeris/tle/?elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167\
            &min_altitude=-90&tle="
        + tle
    )
    # Check that the response was correct
    data = response.json
    assert_single_jd(data)


def test_min_max_alt_tle_jdstep(client, mocker):
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        "/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&tle="
        + tle
    )

    # Check that the response was correct
    data = response.json
    assert data == {"info": "No position information found with this criteria"}

    response = client.get(
        "/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&min_altitude=-90&tle="
        + tle
    )
    # Check that the response was correct
    data = response.json
    assert_jd_step(data)


def get_mock_tle():
    tle_line1 = "1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997"
    tle_line2 = "2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    date_collected = datetime.datetime(2023, 9, 5, 16, 21, 29)
    sat_name = "ISS (ZARYA)"

    tle_tuple = namedtuple("tle", ["tle_line1", "tle_line2", "date_collected"])
    satellite_tuple = namedtuple("satellite", ["sat_name", "sat_number"])

    tle = tle_tuple(tle_line1, tle_line2, date_collected)
    satellite = satellite_tuple(sat_name, 25544)

    return tle, satellite


def assert_single_jd(data):
    assert data[0]["ALTITUDE-DEG"] == pytest.approx(-8.16137402215, assert_precision)
    assert data[0]["AZIMUTH-DEG"] == pytest.approx(306.59130150861, assert_precision)
    assert data[0]["DDEC-DEG_PER_SEC"] == pytest.approx(0.00471072904, assert_precision)
    assert data[0]["DECLINATION-DEG"] == pytest.approx(25.04591441092, assert_precision)
    assert data[0]["DRA_COSDEC-DEG_PER_SEC"] == pytest.approx(
        0.05809617341, assert_precision
    )
    assert data[0]["ILLUMINATED"] is True
    assert data[0]["JULIAN_DATE"] == 2460193.104167
    assert data[0]["NAME"] == "ISS (ZARYA)"
    assert data[0]["PHASE_ANGLE-DEG"] == pytest.approx(33.59995261255, assert_precision)
    assert data[0]["RANGE-KM"] == pytest.approx(3426.649224172898, assert_precision)
    assert data[0]["RANGE_RATE-KM_PER_SEC"] == pytest.approx(
        -6.597948905187, assert_precision
    )
    assert data[0]["RIGHT_ASCENSION-DEG"] == pytest.approx(
        333.08094588626, assert_precision
    )
    assert data[0]["OBSERVER_GCRS-KM"] == pytest.approx(
        [-147.12272716510805, 5412.091101268944, 3360.663968123699], assert_precision
    )
    assert data[0]["SATELLITE_GCRS-KM"] == pytest.approx(
        [2620.939611834229, 4006.6152611592215, 4811.316736985398], assert_precision
    )


def assert_jd_step(data):
    assert data[0]["ALTITUDE-DEG"] == pytest.approx(-22.16343307904, assert_precision)
    assert data[0]["AZIMUTH-DEG"] == pytest.approx(313.30708204802, assert_precision)
    assert data[0]["DDEC-DEG_PER_SEC"] == pytest.approx(0.02061734218, assert_precision)
    assert data[0]["DECLINATION-DEG"] == pytest.approx(19.71059982444, assert_precision)
    assert data[0]["DRA_COSDEC-DEG_PER_SEC"] == pytest.approx(
        0.03480327715, assert_precision
    )
    assert data[0]["ILLUMINATED"] is True
    assert data[0]["JULIAN_DATE"] == 2460193.1
    assert data[0]["NAME"] == "ISS (ZARYA)"
    assert data[0]["PHASE_ANGLE-DEG"] == pytest.approx(38.23308559305, assert_precision)
    assert data[0]["RANGE-KM"] == pytest.approx(5773.187963839149, assert_precision)
    assert data[0]["RANGE_RATE-KM_PER_SEC"] == pytest.approx(
        -6.337586503698, assert_precision
    )
    assert data[0]["RIGHT_ASCENSION-DEG"] == pytest.approx(
        315.91572204924, assert_precision
    )
    assert data[0]["OBSERVER_GCRS-KM"] == pytest.approx(
        [-5.00171963899434, 5414.289884914357, 3360.3388991056636], assert_precision
    )
    assert data[0]["SATELLITE_GCRS-KM"] == pytest.approx(
        [3898.999479564518, 1633.1262527576182, 5307.458692361852], assert_precision
    )

    assert data[1]["ALTITUDE-DEG"] == pytest.approx(-59.87503033798, assert_precision)
    assert data[1]["AZIMUTH-DEG"] == pytest.approx(129.21859963133, assert_precision)
    assert data[1]["DDEC-DEG_PER_SEC"] == pytest.approx(0.02919672877, assert_precision)
    assert data[1]["DECLINATION-DEG"] == pytest.approx(
        -46.67552227562, assert_precision
    )
    assert data[1]["DRA_COSDEC-DEG_PER_SEC"] == pytest.approx(
        0.02033564678, assert_precision
    )
    assert data[1]["ILLUMINATED"] is True
    assert data[1]["JULIAN_DATE"] == 2460193.2
    assert data[1]["NAME"] == "ISS (ZARYA)"
    assert data[1]["PHASE_ANGLE-DEG"] == pytest.approx(72.93173570671, assert_precision)
    assert data[1]["RANGE-KM"] == pytest.approx(11500.17459762438, assert_precision)
    assert data[1]["RANGE_RATE-KM_PER_SEC"] == pytest.approx(
        2.699116660657, assert_precision
    )
    assert data[1]["RIGHT_ASCENSION-DEG"] == pytest.approx(
        271.57445320308, assert_precision
    )
    assert data[1]["OBSERVER_GCRS-KM"] == pytest.approx(
        [-3192.457318351085, 4367.320274866453, 3367.664974307105], assert_precision
    )
    assert data[1]["SATELLITE_GCRS-KM"] == pytest.approx(
        [-2975.655556845774, -3520.3064260060255, -4998.4785697481575], assert_precision
    )
