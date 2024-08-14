# ruff: noqa: S101

import pytest
import requests

assert_precision = 0.0000000001


def test_get_ephemeris_by_name(client):
    # correct request
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # elevation missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&latitude=32&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response has the correct status code
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # name missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400

    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # julian_date missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # with min_altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with min and max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with data_source (both)
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90&data_source=celestrak",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90&data_source=spacetrack",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # verify response data
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90&max_altitude=80",
        timeout=10,
    )
    data = response.json()["data"]

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
    data = [dict(zip(fields_ordered, data_point)) for data_point in data]
    for field in fields_ordered:
        print(f"{field}: {data[0][field]}")
    assert data[0]["altitude_deg"] == pytest.approx(-8.16564726, assert_precision)
    assert data[0]["azimuth_deg"] == pytest.approx(306.5940723, assert_precision)
    assert data[0]["ddec_deg_per_sec"] == pytest.approx(0.0047194, assert_precision)
    assert data[0]["declination_deg"] == pytest.approx(25.04516817, assert_precision)
    assert data[0]["dra_cosdec_deg_per_sec"] == pytest.approx(
        0.05808628, assert_precision
    )
    assert data[0]["illuminated"] is True
    assert data[0]["julian_date"] == 2460193.104167
    assert data[0]["name"] == "ISS (ZARYA)"
    assert data[0]["phase_angle_deg"] == pytest.approx(33.60092979, assert_precision)
    assert data[0]["range_km"] == pytest.approx(3426.841441, assert_precision)
    assert data[0]["range_rate_km_per_sec"] == pytest.approx(
        -6.598351868609, assert_precision
    )
    assert data[0]["right_ascension_deg"] == pytest.approx(
        333.07540204, assert_precision
    )
    assert data[0]["observer_gcrs_km"] == pytest.approx(
        [-147.12272716510805, 5412.091101268944, 3360.663968123699], assert_precision
    )
    assert data[0]["satellite_gcrs_km"] == pytest.approx(
        [2620.975719684184, 4006.2600242071826, 4811.357675217916], assert_precision
    )
    assert data[0]["tle_date"] == "2023-09-07 19:16:45 UTC"
    assert data[0]["data_source"] == "celestrak"


def test_get_ephemeris_by_catalog_number(client):
    # correct request
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # elevation missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&latitude=32&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response has the correct status code
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # catalog number missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # julian_date missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # with min_altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with min and max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with data_source (both)
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90&data_source=celestrak",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167&min_altitude=-90&data_source=spacetrack",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200


def test_get_ephemeris_by_name_jdstep(client):
    # correct request
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # elevation missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response has the correct status code
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # name missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # startjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # stopjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # with min_altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with min and max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&min_altitude=-90&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with data_source (both)
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&min_altitude=-90&data_source=celestrak",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&min_altitude=-90&data_source=spacetrack",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200


def test_get_ephemeris_by_catalog_jdstep(client):
    # correct request
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # elevation missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response has the correct status code
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # catalog id missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # startjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # stopjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

    # with min_altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with min and max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&min_altitude=-90&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with data_source (both)
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&min_altitude=-90&data_source=celestrak",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1&min_altitude=-90&data_source=spacetrack",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200


def test_get_ephemeris_by_tle(client):
    # correct request
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # elevation missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&julian_date=2460000.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response has the correct status code
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # tle missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    assert "Missing parameter" in response.text, "Incorrect error message returned"

    # tle not formatted correctly
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%209812769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 500

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&elevation=222&julian_date=2460000.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # julian_date missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # with min_altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with min and max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with data_source (both)
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90&data_source=celestrak",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90&data_source=spacetrack",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200


def test_get_ephemeris_by_tle_jdstep(client):
    # correct request
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # elevation missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1",
        timeout=10,
    )
    # Check that the response has the correct status code
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # tle missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    assert "Missing parameter" in response.text, "Incorrect error message returned"

    # tle not correctly formatted
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%202554420%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 500

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # startjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&stopjd=2460000.3&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # stopjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"

    # with min_altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with min and max altitude
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90&max_altitude=80",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with data_source (both)
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90&data_source=celestrak",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90&data_source=spacetrack",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200


def test_get_names_from_norad_id(client):
    # one name found
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/names-from-norad-id/?id=25544",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # multiple names found
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/names-from-norad-id/?id=59582",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200
    data = response.json()
    assert data[1] != []

    # no names found
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/names-from-norad-id/?id=1",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200
    assert response.json() == []

    # norad id missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/names-from-norad-id/",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"


def test_get_norad_ids_from_name(client):
    # one norad id found
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/norad-ids-from-name/?name=ISS%20(ZARYA)",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # multiple norad ids found
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/norad-ids-from-name/?name=STARLINK-31000",
        timeout=10,
    )
    # Check that the response was returned without error and has multiple ids
    assert response.status_code == 200
    data = response.json()
    assert data[1] != []

    # no norad ids found
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/norad-ids-from-name/?name=STARLINK-11300",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # name missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/norad-ids-from-name/",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 500


def test_get_tle_data(client):
    # norad id as id
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=25544&id_type=catalog",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # no TLE data found
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=1&id_type=catalog",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200
    assert response.json() == []

    # name as id
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=ISS%20(ZARYA)&id_type=name",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with start date
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=ISS%20(ZARYA)&id_type=name&start_date=2460425",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with end date
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=ISS%20(ZARYA)&id_type=name&end_date=2460427",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

    # with start and end date
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427",
        timeout=10,
    )
    assert response.status_code == 200

    data = response.json()
    assert data[0]["satellite_name"] == "ISS (ZARYA)"
    assert data[0]["date_collected"] == "2024-04-26 01:31:05 UTC"
    assert data[0]["epoch"] == "2024-04-25 18:22:37 UTC"
    assert data[0]["satellite_id"] == 25544
    assert (
        data[0]["tle_line1"]
        == "1 25544U 98067A   24116.76570894  .00062894  00000+0  10654-2 0  9996"
    )
    assert (
        data[0]["tle_line2"]
        == "2 25544  51.6396 215.3361 0004566  95.7745   7.6568 15.50926567450413"
    )

    # id missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id_type=name",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
    # Check that the response contains the expected error message.
    assert "Incorrect parameters" in response.text, "Incorrect error message returned"
