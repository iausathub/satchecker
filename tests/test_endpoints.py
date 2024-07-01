# ruff: noqa: S101
import datetime
from collections import namedtuple

import pytest
import redis
from core.versions.v1 import routes

assert_precision = 0.000001


def cannot_connect_to_redis():
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.ping()
        return False
    except redis.ConnectionError:
        return True


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
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


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
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


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
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


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
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


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
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


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
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


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
def test_min_max_alt_name(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110\
            &julian_date=2460193.104167"
    )

    # Check that the response was correct
    data = response.json
    assert (
        "info" in data
        and data["info"] == "No position information found with this criteria"
    )

    response = client.get(
        "/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110\
            &julian_date=2460193.104167&min_altitude=-90"
    )
    # Check that the response was correct
    data = response.json
    assert_single_jd(data)


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
def test_min_max_alt_name_jdstep(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32\
            &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1"
    )

    # Check that the response was correct
    data = response.json
    assert (
        "info" in data
        and data["info"] == "No position information found with this criteria"
    )

    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32\
            &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&min_altitude=-90"
    )
    # Check that the response was correct
    data = response.json
    assert_jd_step(data)


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
def test_min_max_alt_catalog(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110\
            &julian_date=2460193.104167"
    )

    # Check that the response was correct
    data = response.json
    assert (
        "info" in data
        and data["info"] == "No position information found with this criteria"
    )

    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110\
            &julian_date=2460193.104167&min_altitude=-90"
    )
    # Check that the response was correct
    data = response.json
    assert_single_jd(data)


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
def test_min_max_alt_catalog_jdstep(client, mocker):
    mocker.patch.object(routes, "get_tle", return_value=get_mock_tle())
    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32\
        &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1"
    )

    # Check that the response was correct
    data = response.json
    assert (
        "info" in data
        and data["info"] == "No position information found with this criteria"
    )

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32\
        &longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&min_altitude=-90"
    )
    # Check that the response was correct
    data = response.json
    assert_jd_step(data)


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
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
    assert (
        "info" in data
        and data["info"] == "No position information found with this criteria"
    )

    response = client.get(
        "/ephemeris/tle/?elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167\
            &min_altitude=-90&tle="
        + tle
    )
    # Check that the response was correct
    data = response.json
    assert_single_jd(data)


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
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
    assert (
        "info" in data
        and data["info"] == "No position information found with this criteria"
    )

    response = client.get(
        "/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&stopjd=2460193.2&stepjd=0.1&min_altitude=-90&tle="
        + tle
    )
    # Check that the response was correct
    data = response.json
    assert_jd_step(data)


@pytest.mark.skipif(cannot_connect_to_redis(), reason="Can't connect to Redis")
def get_mock_tle():
    tle_line1 = "1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997"
    tle_line2 = "2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    date_collected = datetime.datetime(2023, 9, 5, 16, 21, 29)
    sat_name = "ISS (ZARYA)"
    data_source = "celestrak"

    satellite_tuple = namedtuple("satellite", ["sat_name", "sat_number"])
    tle_tuple = namedtuple(
        "tle",
        ["tle_line1", "tle_line2", "date_collected", "data_source", "tle_satellite"],
    )

    satellite = satellite_tuple(sat_name, 25544)
    tle = tle_tuple(tle_line1, tle_line2, date_collected, data_source, satellite)

    return tle


def assert_single_jd(json_data):
    fields_ordered = [
        "name",
        "catalog_id",
        "julian_date",
        "satellite_gcrs_km",
        "right_ascension_deg",
        "declination_deg",
        "tle_date",
        "dra_cosdec_deg_per_sec",
        "ddec_deg_per_sec",
        "altitude_deg",
        "azimuth_deg",
        "range_km",
        "range_rate_km_per_sec",
        "phase_angle_deg",
        "illuminated",
        "data_source",
        "observer_gcrs_km",
    ]

    data = json_data["data"]
    data = [dict(zip(fields_ordered, data_point)) for data_point in data]

    assert data[0]["altitude_deg"] == pytest.approx(-8.16137402215, assert_precision)
    assert data[0]["azimuth_deg"] == pytest.approx(306.59130150861, assert_precision)
    assert data[0]["ddec_deg_per_sec"] == pytest.approx(0.00471072904, assert_precision)
    assert data[0]["declination_deg"] == pytest.approx(25.04591441092, assert_precision)
    assert data[0]["dra_cosdec_deg_per_sec"] == pytest.approx(
        0.05809617341, assert_precision
    )
    assert data[0]["illuminated"] is True
    assert data[0]["julian_date"] == 2460193.104167
    assert data[0]["name"] == "ISS (ZARYA)"
    assert data[0]["phase_angle_deg"] == pytest.approx(33.59995261255, assert_precision)
    assert data[0]["range_km"] == pytest.approx(3426.649224172898, assert_precision)
    assert data[0]["range_rate_km_per_sec"] == pytest.approx(
        -6.597948905187, assert_precision
    )
    assert data[0]["right_ascension_deg"] == pytest.approx(
        333.08094588626, assert_precision
    )
    assert data[0]["observer_gcrs_km"] == pytest.approx(
        [-147.12272716510805, 5412.091101268944, 3360.663968123699], assert_precision
    )
    assert data[0]["satellite_gcrs_km"] == pytest.approx(
        [2620.939611834229, 4006.6152611592215, 4811.316736985398], assert_precision
    )


def assert_jd_step(json_data):
    fields_ordered = [
        "name",
        "catalog_id",
        "julian_date",
        "satellite_gcrs_km",
        "right_ascension_deg",
        "declination_deg",
        "tle_date",
        "dra_cosdec_deg_per_sec",
        "ddec_deg_per_sec",
        "altitude_deg",
        "azimuth_deg",
        "range_km",
        "range_rate_km_per_sec",
        "phase_angle_deg",
        "illuminated",
        "data_source",
        "observer_gcrs_km",
    ]
    data = json_data["data"]
    data = [dict(zip(fields_ordered, data_point)) for data_point in data]

    assert data[0]["altitude_deg"] == pytest.approx(-22.16343307904, assert_precision)
    assert data[0]["azimuth_deg"] == pytest.approx(313.30708204802, assert_precision)
    assert data[0]["ddec_deg_per_sec"] == pytest.approx(0.02061734218, assert_precision)
    assert data[0]["declination_deg"] == pytest.approx(19.71059982444, assert_precision)
    assert data[0]["dra_cosdec_deg_per_sec"] == pytest.approx(
        0.03480327715, assert_precision
    )
    assert data[0]["illuminated"] is True
    assert data[0]["julian_date"] == 2460193.1
    assert data[0]["name"] == "ISS (ZARYA)"
    assert data[0]["phase_angle_deg"] == pytest.approx(38.23308559305, assert_precision)
    assert data[0]["range_km"] == pytest.approx(5773.187963839149, assert_precision)
    assert data[0]["range_rate_km_per_sec"] == pytest.approx(
        -6.337586503698, assert_precision
    )
    assert data[0]["right_ascension_deg"] == pytest.approx(
        315.91572204924, assert_precision
    )
    assert data[0]["observer_gcrs_km"] == pytest.approx(
        [-5.00171963899434, 5414.289884914357, 3360.3388991056636], assert_precision
    )
    assert data[0]["satellite_gcrs_km"] == pytest.approx(
        [3898.999479564518, 1633.1262527576182, 5307.458692361852], assert_precision
    )

    assert data[1]["altitude_deg"] == pytest.approx(-59.87503033798, assert_precision)
    assert data[1]["azimuth_deg"] == pytest.approx(129.21859963133, assert_precision)
    assert data[1]["ddec_deg_per_sec"] == pytest.approx(0.02919672877, assert_precision)
    assert data[1]["declination_deg"] == pytest.approx(
        -46.67552227562, assert_precision
    )
    assert data[1]["dra_cosdec_deg_per_sec"] == pytest.approx(
        0.02033564678, assert_precision
    )
    assert data[1]["illuminated"] is True
    assert data[1]["julian_date"] == 2460193.2
    assert data[1]["name"] == "ISS (ZARYA)"
    assert data[1]["phase_angle_deg"] == pytest.approx(72.93173570671, assert_precision)
    assert data[1]["range_km"] == pytest.approx(11500.17459762438, assert_precision)
    assert data[1]["range_rate_km_per_sec"] == pytest.approx(
        2.699116660657, assert_precision
    )
    assert data[1]["right_ascension_deg"] == pytest.approx(
        271.57445320308, assert_precision
    )
    assert data[1]["observer_gcrs_km"] == pytest.approx(
        [-3192.457318351085, 4367.320274866453, 3367.664974307105], assert_precision
    )
    assert data[1]["satellite_gcrs_km"] == pytest.approx(
        [-2975.655556845774, -3520.3064260060255, -4998.4785697481575], assert_precision
    )
