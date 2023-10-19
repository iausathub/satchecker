Ephemeris API
=============

Retrieve satellite ephemeris by name with JD time step
-----------------------------------------------------------

.. http:get:: /name-jdstep/
   :noindex:

    Retrieve ephemeris over a JD range at a specified time step
	
   :query name: (*required*) -- Name of satellite as displayed in CelesTrak TLE files
   :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
   :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg) 
   :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
   :query startjd: (*required*) -- UT1 Julian Start Date
   :query stopjd: (*required*) -- UT1 Julian End Date (not included)
   :query stepjd: (*required*) -- UT1 time step in Julian Days for ephemeris generation


**Example Request**
    .. tabs::

        .. code-tab:: python
                    
            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/'
            params = {'name': 'STARLINK-1600',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'startjd': 2460000.1,
                            'stopjd': 2460000.3,
                            'stepjd': 0.1}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1" -H "accept: application/json"


**Example Response**

.. sourcecode:: json

    [
        {
            "ALTITUDE-DEG": -83.92701127488,
            "AZIMUTH-DEG": 74.23644169397,
            "DDEC-DEG_PER_SEC": -0.02013597761,
            "DECLINATION-DEG": -38.21698520948,
            "DRA_COSDEC-DEG_PER_SEC": 0.0273538424,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.1,
            "NAME": "STARLINK-1600",
            "PHASE_ANGLE-DEG": 75.47849642996,
            "RANGE-KM": 13236.231719560885,
            "RANGE_RATE-KM_PER_SEC": 0.656362193304,
            "RIGHT_ASCENSION-DEG": 94.32142232641,
            "TLE-DATE": "2023-09-05 16:20:37"
        },
        {
            "ALTITUDE-DEG": -11.8036627367,
            "AZIMUTH-DEG": 282.38507272541,
            "DDEC-DEG_PER_SEC": 0.05433004435,
            "DECLINATION-DEG": 1.75807790636,
            "DRA_COSDEC-DEG_PER_SEC": 0.00760649602,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.2,
            "NAME": "STARLINK-1600",
            "PHASE_ANGLE-DEG": 53.73895247174,
            "RANGE-KM": 4328.449597815868,
            "RANGE_RATE-KM_PER_SEC": -6.016772535669,
            "RIGHT_ASCENSION-DEG": 210.80053185868,
            "TLE-DATE": "2023-09-05 16:20:37"
        }
    ]


Retrieve satellite ephemeris by name
-----------------------------------------------------------

.. http:get:: /name/
    :noindex:

    Retrieve ephemeris for specified satellite
	
    :query name: (*required*) -- Name of satellite as displayed in CelesTrak TLE files
    :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
    :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg) 
    :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
    :query julian_date: (*required*) -- UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.

**Example Request**
    .. tabs::

        .. code-tab:: python
                    
            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/name/'
            params = {'name': 'STARLINK-1600',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'julian_date': 2460000.1}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1" -H "accept: application/json"


**Example Response**

.. sourcecode:: json

    [
        {
            "ALTITUDE-DEG": -83.92701127488,
            "AZIMUTH-DEG": 74.23644169397,
            "DDEC-DEG_PER_SEC": -0.02013597761,
            "DECLINATION-DEG": -38.21698520948,
            "DRA_COSDEC-DEG_PER_SEC": 0.0273538424,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.1,
            "NAME": "STARLINK-1600",
            "PHASE_ANGLE-DEG": 75.47849642996,
            "RANGE-KM": 13236.231719560885,
            "RANGE_RATE-KM_PER_SEC": 0.656362193304,
            "RIGHT_ASCENSION-DEG": 94.32142232641,
            "TLE-DATE": "2023-09-05 16:20:37"
        }
    ]


Retrieve satellite ephemeris by catalog number with JD time step
-----------------------------------------------------------------

.. http:get:: /catalog-number-jdstep/
    :noindex:
 
    Retrieve ephemeris for specified satellite
	
    :query catalog: (*required*) -- Satellite catalog number (NORAD ID)
    :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
    :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg) 
    :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
    :query startjd: (*required*) -- UT1 Julian Start Date
    :query stopjd: (*required*) -- UT1 Julian End Date (not included)
    :query stepjd: (*required*) -- UT1 time step in Julian Days for ephemeris generation

**Example Request**
    .. tabs::

        .. code-tab:: python
                    
            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/'
            params = {'catalog': '25544',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'startjd': 2460000.1,
                            'stopjd': 2460000.3,
                            'stepjd': 0.1}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1" -H "accept: application/json"


**Example Response**

.. sourcecode:: json

    [
        {
            "ALTITUDE-DEG": -59.42992120557,
            "AZIMUTH-DEG": 288.04620638774,
            "DDEC-DEG_PER_SEC": 0.02460147584,
            "DECLINATION-DEG": -25.64785198072,
            "DRA_COSDEC-DEG_PER_SEC": 0.02499960249,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.1,
            "NAME": "ISS (ZARYA)",
            "PHASE_ANGLE-DEG": 41.69217956408,
            "RANGE-KM": 11477.324789805665,
            "RANGE_RATE-KM_PER_SEC": -3.431545486776,
            "RIGHT_ASCENSION-DEG": 134.21602941437,
            "TLE-DATE": "2023-09-05 16:21:29"
        },
        {
            "ALTITUDE-DEG": -22.86735389391,
            "AZIMUTH-DEG": 142.33553116822,
            "DDEC-DEG_PER_SEC": -0.01420767889,
            "DECLINATION-DEG": -54.03105192755,
            "DRA_COSDEC-DEG_PER_SEC": 0.03650863588,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.2,
            "NAME": "ISS (ZARYA)",
            "PHASE_ANGLE-DEG": 118.54352293428,
            "RANGE-KM": 5908.636912798003,
            "RANGE_RATE-KM_PER_SEC": 6.290602878885,
            "RIGHT_ASCENSION-DEG": 30.83552022903,
            "TLE-DATE": "2023-09-05 16:21:29"
        }
    ]


Retrieve satellite ephemeris by catalog number
-----------------------------------------------------------

.. http:get:: /catalog-number/
    :noindex:
 
    Retrieve ephemeris for specified satellite
	
    :query catalog: (*required*) -- Satellite catalog number (NORAD ID)
    :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
    :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg) 
    :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
    :query julian_date: (*required*) -- UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.

**Example Request**
    .. tabs::

        .. code-tab:: python
                    
            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/'
            params = {'catalog': '25544',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'julian_date': 2460000.1}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1" -H "accept: application/json"


**Example Response**

.. sourcecode:: json

    [
        {
            "ALTITUDE-DEG": -59.42992120557,
            "AZIMUTH-DEG": 288.04620638774,
            "DDEC-DEG_PER_SEC": 0.02460147584,
            "DECLINATION-DEG": -25.64785198072,
            "DRA_COSDEC-DEG_PER_SEC": 0.02499960249,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.1,
            "NAME": "ISS (ZARYA)",
            "PHASE_ANGLE-DEG": 41.69217956408,
            "RANGE-KM": 11477.324789805665,
            "RANGE_RATE-KM_PER_SEC": -3.431545486776,
            "RIGHT_ASCENSION-DEG": 134.21602941437,
            "TLE-DATE": "2023-09-05 16:21:29"
        }
    ]


Retrieve satellite ephemeris given a TLE with JD time step
-----------------------------------------------------------

.. http:get:: /tle-jdstep/
   :noindex:

    Retrieve ephemeris over a JD range at a specified time step
	
   :query tle: (*required*) -- Two line element set 
   :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
   :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg) 
   :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
   :query startjd: (*required*) -- UT1 Julian Start Date
   :query stopjd: (*required*) -- UT1 Julian End Date (not included)
   :query stepjd: (*required*) -- UT1 time step in Julian Days for ephemeris generation


**Example Request**
    .. tabs::

        .. code-tab:: python
                    
            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/'
            params = {'tle': 'ISS (ZARYA) \n 1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\n2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'startjd': 2460000.1,
                            'stopjd': 2460000.3,
                            'stepjd': 0.1}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1" -H "accept: application/json"


**Example Response**

.. sourcecode:: json

    [
        {
            "ALTITUDE-DEG": -59.42992120557,
            "AZIMUTH-DEG": 288.04620638774,
            "DDEC-DEG_PER_SEC": 0.02460147584,
            "DECLINATION-DEG": -25.64785198072,
            "DRA_COSDEC-DEG_PER_SEC": 0.02499960249,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.1,
            "NAME": "ISS (ZARYA)",
            "PHASE_ANGLE-DEG": 41.69217956408,
            "RANGE-KM": 11477.324789805663,
            "RANGE_RATE-KM_PER_SEC": -3.431545486777,
            "RIGHT_ASCENSION-DEG": 134.21602941437,
            "TLE-DATE": null
        },
        {
            "ALTITUDE-DEG": -22.86735389391,
            "AZIMUTH-DEG": 142.33553116822,
            "DDEC-DEG_PER_SEC": -0.01420767889,
            "DECLINATION-DEG": -54.03105192755,
            "DRA_COSDEC-DEG_PER_SEC": 0.03650863588,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.2,
            "NAME": "ISS (ZARYA)",
            "PHASE_ANGLE-DEG": 118.54352293428,
            "RANGE-KM": 5908.636912798006,
            "RANGE_RATE-KM_PER_SEC": 6.290602878885,
            "RIGHT_ASCENSION-DEG": 30.83552022903,
            "TLE-DATE": null
        }
    ]


Retrieve satellite ephemeris with a given TLE
-----------------------------------------------------------

.. http:get:: /tle/
    :noindex:

    Retrieve ephemeris for specified satellite
	
    :query tle: (*required*) -- Two line element set
    :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
    :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg) 
    :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
    :query julian_date: (*required*) -- UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.

**Example Request**
    .. tabs::

        .. code-tab:: python
                    
            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/tle/'
            params = {'tle': 'ISS (ZARYA) \n 1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\n2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'julian_date': 2460000.1}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1" -H "accept: application/json"


**Example Response**

.. sourcecode:: json

    [
        {
            "ALTITUDE-DEG": -59.42992120557,
            "AZIMUTH-DEG": 288.04620638774,
            "DDEC-DEG_PER_SEC": 0.02460147584,
            "DECLINATION-DEG": -25.64785198072,
            "DRA_COSDEC-DEG_PER_SEC": 0.02499960249,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.1,
            "NAME": "ISS (ZARYA)",
            "PHASE_ANGLE-DEG": 41.69217956408,
            "RANGE-KM": 11477.324789805663,
            "RANGE_RATE-KM_PER_SEC": -3.431545486777,
            "RIGHT_ASCENSION-DEG": 134.21602941437,
            "TLE-DATE": null
        }
    ]