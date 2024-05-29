# ruff: noqa: S101

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

    # name missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400

    # julian_date missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400

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

    # catalog number missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&longitude=-110&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&julian_date=2460193.104167",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400

    # julian_date missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 400

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

    # name missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

    # startjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

    # stopjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

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

    # catalog id missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?elevation=150&latitude=32&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

    # latitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&longitude=-110&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&startjd=2460193.104167&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

    # startjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&stopjd=2460194.104167&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with correct error
    assert response.status_code == 400

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

    # tle missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 500

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

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&elevation=222&julian_date=2460000.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400

    # julian_date missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400

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

    # tle missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 500

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

    # longitude missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400

    # startjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&stopjd=2460000.3&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400

    # stopjd missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stepjd=0.1",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400

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
        "https://cps.iau.org/tools/satchecker/api/tools/norad-ids-from-name/?name=STARLINK-1130",
        timeout=10,
    )
    # Check that the response was returned without error
    assert response.status_code == 200

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
    assert response.status_code == 400


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
    # with end date
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=ISS%20(ZARYA)&id_type=name&end_date=2460427",
        timeout=10,
    )

    # with start and end date
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427",
        timeout=10,
    )
    assert response.status_code == 200
    assert response.json() != []

    # id missing
    response = requests.get(
        "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id_type=name",
        timeout=10,
    )
    # Check that the response was returned with the correct error
    assert response.status_code == 400
