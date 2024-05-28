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
   :query stepjd: (*optional*) -- UT1 time step in Julian Days for ephemeris generation. Default is .05 (1.2 hours).
   :query min_altitude: (*optional*) -- Minimum altitude to return satellite positions (degrees). Default is 0.
   :query max_altitude: (*optional*) -- Maximum altitude to return satellite positions (degrees). Default is 90.
   :query data_source: (*optional*) -- Data source for the TLE data - either 'celestrak' or 'spacetrack'. Default is 'spacetrack'.


**Example Request**
    .. tabs::

        .. tab:: Browser

            https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90

        .. code-tab:: Python

            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/'
            params = {'name': 'STARLINK-1600',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'startjd': 2460000.1,
                            'stopjd': 2460000.3,
                            'stepjd': 0.1,
                            'min_altitude': -90}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    [
        {
            "ALTITUDE-DEG": -9.80971257652,
            "AZIMUTH-DEG": 55.15478730961,
            "CATALOG_ID": 46161,
            "DATA_SOURCE": "spacetrack",
            "DDEC-DEG_PER_SEC": -0.05070574412,
            "DECLINATION-DEG": 18.61796683006,
            "DRA_COSDEC-DEG_PER_SEC": 0.01019243518,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.1,
            "NAME": "STARLINK-1600",
            "OBSERVER_GCRS_KM": [
            1000.044906440929,
            -4783.283201527772,
            4085.459180326725
            ],
            "PHASE_ANGLE-DEG": 109.24612785799,
            "RANGE-KM": 4095.040926172063,
            "RANGE_RATE-KM_PER_SEC": 6.284422469172,
            "RIGHT_ASCENSION-DEG": 43.04367601256,
            "SATELLITE_GCRS_KM": [
            2836.175695292651,
            2648.8215197690492,
            1307.3684135941762
            ],
            "TLE-DATE": "2024-02-05 16:12:42"
        },
        {
            "ALTITUDE-DEG": -83.13771686839,
            "AZIMUTH-DEG": 208.61161584252,
            "CATALOG_ID": 46161,
            "DATA_SOURCE": "spacetrack",
            "DDEC-DEG_PER_SEC": 0.00663582343,
            "DECLINATION-DEG": -45.94348488944,
            "DRA_COSDEC-DEG_PER_SEC": 0.03354248225,
            "ILLUMINATED": true,
            "JULIAN_DATE": 2460000.2,
            "NAME": "STARLINK-1600",
            "OBSERVER_GCRS_KM": [
            3628.0577317280786,
            -3281.0604185873253,
            4079.547075333211
            ],
            "PHASE_ANGLE-DEG": 56.98343683301,
            "RANGE-KM": 13245.443279043235,
            "RANGE_RATE-KM_PER_SEC": -0.265606961091,
            "RIGHT_ASCENSION-DEG": 142.61268227652,
            "SATELLITE_GCRS_KM": [
            -7318.155592415026,
            5592.586129513591,
            -9518.894198777909
            ],
            "TLE-DATE": "2024-02-05 16:12:42"
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
    :query min_altitude: (*optional*) -- Minimum altitude to return satellite positions (degrees). Default is 0.
    :query max_altitude: (*optional*) -- Maximum altitude to return satellite positions (degrees). Default is 90.
    :query data_source: (*optional*) -- Data source for the TLE data - either 'celestrak' or 'spacetrack'. Default is 'spacetrack'.

**Example Request**
    .. tabs::

        .. tab:: Browser

            https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90

        .. code-tab:: Python

            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/name/'
            params = {'name': 'STARLINK-1600',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'julian_date': 2460000.1,
                            'min_altitude': -90}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/name/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    [
        {
        "ALTITUDE-DEG": -9.80971257652,
        "AZIMUTH-DEG": 55.15478730961,
        "CATALOG_ID": 46161,
        "DATA_SOURCE": "spacetrack",
        "DDEC-DEG_PER_SEC": -0.05070574412,
        "DECLINATION-DEG": 18.61796683006,
        "DRA_COSDEC-DEG_PER_SEC": 0.01019243518,
        "ILLUMINATED": true,
        "JULIAN_DATE": 2460000.1,
        "NAME": "STARLINK-1600",
        "OBSERVER_GCRS_KM": [
        1000.044906440929,
        -4783.283201527772,
        4085.459180326725
        ],
        "PHASE_ANGLE-DEG": 109.24612785799,
        "RANGE-KM": 4095.040926172063,
        "RANGE_RATE-KM_PER_SEC": 6.284422469172,
        "RIGHT_ASCENSION-DEG": 43.04367601256,
        "SATELLITE_GCRS_KM": [
        2836.175695292651,
        2648.8215197690492,
        1307.3684135941762
        ],
        "TLE-DATE": "2024-02-05 16:12:42"
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
    :query stepjd: (*optional*) -- UT1 time step in Julian Days for ephemeris generation. Default is .05 (1.2 hours).
    :query min_altitude: (*optional*) -- Minimum altitude to return satellite positions (degrees). Default is 0.
    :query max_altitude: (*optional*) -- Maximum altitude to return satellite positions (degrees). Default is 90.
    :query data_source: (*optional*) -- Data source for the TLE data - either 'celestrak' or 'spacetrack'. Default is 'spacetrack'.

**Example Request**
    .. tabs::

        .. tab:: Browser

                https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90

        .. code-tab:: Python

            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/'
            params = {'catalog': '25544',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'startjd': 2460000.1,
                            'stopjd': 2460000.3,
                            'stepjd': 0.1,
                            'min_altitude': -90}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    [
        {
        "ALTITUDE-DEG": -38.53633089073,
        "AZIMUTH-DEG": 118.05686288053,
        "CATALOG_ID": 25544,
        "DATA_SOURCE": "spacetrack",
        "DDEC-DEG_PER_SEC": -0.0182556905,
        "DECLINATION-DEG": -43.1707018844,
        "DRA_COSDEC-DEG_PER_SEC": 0.03127755027,
        "ILLUMINATED": true,
        "JULIAN_DATE": 2460000.1,
        "NAME": "ISS (ZARYA)",
        "OBSERVER_GCRS_KM": [
        1000.044906440929,
        -4783.283201527772,
        4085.459180326725
        ],
        "PHASE_ANGLE-DEG": 122.63076525818,
        "RANGE-KM": 8616.09765998085,
        "RANGE_RATE-KM_PER_SEC": 5.327592257625,
        "RIGHT_ASCENSION-DEG": 30.89434330729,
        "SATELLITE_GCRS_KM": [
        5392.295524240439,
        3226.4992801338067,
        -5894.912235214352
        ],
        "TLE-DATE": "2024-02-05 16:12:40"
        },
        {
        "ALTITUDE-DEG": -50.46812397947,
        "AZIMUTH-DEG": 324.71176684274,
        "CATALOG_ID": 25544,
        "DATA_SOURCE": "spacetrack",
        "DDEC-DEG_PER_SEC": 0.02490119298,
        "DECLINATION-DEG": -5.59399390423,
        "DRA_COSDEC-DEG_PER_SEC": 0.02567883796,
        "ILLUMINATED": true,
        "JULIAN_DATE": 2460000.2,
        "NAME": "ISS (ZARYA)",
        "OBSERVER_GCRS_KM": [
        3628.0577317280786,
        -3281.0604185873253,
        4079.547075333211
        ],
        "PHASE_ANGLE-DEG": 15.24978839577,
        "RANGE-KM": 10411.732621192474,
        "RANGE_RATE-KM_PER_SEC": -4.272868987599,
        "RIGHT_ASCENSION-DEG": 159.49416406581,
        "SATELLITE_GCRS_KM": [
        -9705.566206822945,
        3629.8893184499234,
        -1014.9208422252426
        ],
        "TLE-DATE": "2024-02-05 16:12:40"
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
    :query min_altitude: (*optional*) -- Minimum altitude to return satellite positions (degrees). Default is 0.
    :query max_altitude: (*optional*) -- Maximum altitude to return satellite positions (degrees). Default is 90.
    :query data_source: (*optional*) -- Data source for the TLE data - either 'celestrak' or 'spacetrack'. Default is 'spacetrack'.

**Example Request**
    .. tabs::

        .. tab:: Browser

            https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90

        .. code-tab:: Python

            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/'
            params = {'catalog': '25544',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'julian_date': 2460000.1,
                            'min_altitude': -90}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number/?catalog=25544&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    [
        {
        "ALTITUDE-DEG": -38.53633089073,
        "AZIMUTH-DEG": 118.05686288053,
        "CATALOG_ID": 25544,
        "DATA_SOURCE": "spacetrack",
        "DDEC-DEG_PER_SEC": -0.0182556905,
        "DECLINATION-DEG": -43.1707018844,
        "DRA_COSDEC-DEG_PER_SEC": 0.03127755027,
        "ILLUMINATED": true,
        "JULIAN_DATE": 2460000.1,
        "NAME": "ISS (ZARYA)",
        "OBSERVER_GCRS_KM": [
        1000.044906440929,
        -4783.283201527772,
        4085.459180326725
        ],
        "PHASE_ANGLE-DEG": 122.63076525818,
        "RANGE-KM": 8616.09765998085,
        "RANGE_RATE-KM_PER_SEC": 5.327592257625,
        "RIGHT_ASCENSION-DEG": 30.89434330729,
        "SATELLITE_GCRS_KM": [
        5392.295524240439,
        3226.4992801338067,
        -5894.912235214352
        ],
        "TLE-DATE": "2024-02-05 16:12:40"
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
    :query stepjd: (*optional*) -- UT1 time step in Julian Days for ephemeris generation. Default is .05 (1.2 hours).
    :query min_altitude: (*optional*) -- Minimum altitude to return satellite positions (degrees). Default is 0.
    :query max_altitude: (*optional*) -- Maximum altitude to return satellite positions (degrees). Default is 90.

**Example Request**
    .. tabs::

        .. tab:: Browser

            https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90

        .. code-tab:: Python

            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/'
            params = {'tle': 'ISS (ZARYA) \n 1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\n2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'startjd': 2460000.1,
                            'stopjd': 2460000.3,
                            'stepjd': 0.1
                            'min_altitude': -90}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.01&min_altitude=-90" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/tle-jdstep/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.01&min_altitude=-90" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    [
        {
        "ALTITUDE-DEG": -59.42992120557,
        "AZIMUTH-DEG": 288.04620638774,
        "CATALOG_ID": "2554",
        "DATA_SOURCE": "user",
        "DDEC-DEG_PER_SEC": 0.02460147584,
        "DECLINATION-DEG": -25.64785198072,
        "DRA_COSDEC-DEG_PER_SEC": 0.02499960249,
        "ILLUMINATED": true,
        "JULIAN_DATE": 2460000.1,
        "NAME": "ISS (ZARYA)",
        "OBSERVER_GCRS_KM": [
        1000.044906440929,
        -4783.283201527772,
        4085.459180326725
        ],
        "PHASE_ANGLE-DEG": 41.69217956408,
        "RANGE-KM": 11477.324789805663,
        "RANGE_RATE-KM_PER_SEC": -3.431545486777,
        "RIGHT_ASCENSION-DEG": 134.21602941437,
        "SATELLITE_GCRS_KM": [
        -7215.27926739175,
        7415.482543610055,
        -4967.831324597148
        ],
        "TLE-DATE": null
        },
        {
        "ALTITUDE-DEG": -22.86735389391,
        "AZIMUTH-DEG": 142.33553116822,
        "CATALOG_ID": "2554",
        "DATA_SOURCE": "user",
        "DDEC-DEG_PER_SEC": -0.01420767889,
        "DECLINATION-DEG": -54.03105192755,
        "DRA_COSDEC-DEG_PER_SEC": 0.03650863588,
        "ILLUMINATED": true,
        "JULIAN_DATE": 2460000.2,
        "NAME": "ISS (ZARYA)",
        "OBSERVER_GCRS_KM": [
        3628.0577317280786,
        -3281.0604185873253,
        4079.547075333211
        ],
        "PHASE_ANGLE-DEG": 118.54352293428,
        "RANGE-KM": 5908.636912798006,
        "RANGE_RATE-KM_PER_SEC": 6.290602878885,
        "RIGHT_ASCENSION-DEG": 30.83552022903,
        "SATELLITE_GCRS_KM": [
        2979.848070910431,
        1778.8506970166927,
        -4782.069200596504
        ],
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
    :query min_altitude: (*optional*) -- Minimum altitude to return satellite positions (degrees). Default is 0.
    :query max_altitude: (*optional*) -- Maximum altitude to return satellite positions (degrees). Default is 90.

**Example Request**
    .. tabs::

        .. tab:: Browser

            https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90

        .. code-tab:: Python

            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/tle/'
            params = {'tle': 'ISS (ZARYA) \n 1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\n2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'julian_date': 2460000.1,
                            'min_altitude': -90}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://cps.iau.org/tools/satchecker/api/ephemeris/tle/?tle=ISS%20(ZARYA)%0A1%2025544U%2098067A%20%20%2023248.54842295%20%20.00012769%20%2000000+0%20%2022936-3%200%20%209997%0A2%2025544%20%2051.6416%20290.4299%200005730%20%2030.7454%20132.9751%2015.50238117414255&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1&min_altitude=-90" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    [
        {
        "ALTITUDE-DEG": -59.42992120557,
        "AZIMUTH-DEG": 288.04620638774,
        "CATALOG_ID": "2554",
        "DATA_SOURCE": "user",
        "DDEC-DEG_PER_SEC": 0.02460147584,
        "DECLINATION-DEG": -25.64785198072,
        "DRA_COSDEC-DEG_PER_SEC": 0.02499960249,
        "ILLUMINATED": true,
        "JULIAN_DATE": 2460000.1,
        "NAME": "ISS (ZARYA)",
        "OBSERVER_GCRS_KM": [
        1000.044906440929,
        -4783.283201527772,
        4085.459180326725
        ],
        "PHASE_ANGLE-DEG": 41.69217956408,
        "RANGE-KM": 11477.324789805663,
        "RANGE_RATE-KM_PER_SEC": -3.431545486777,
        "RIGHT_ASCENSION-DEG": 134.21602941437,
        "SATELLITE_GCRS_KM": [
        -7215.27926739175,
        7415.482543610055,
        -4967.831324597148
        ],
        "TLE-DATE": null
        }
    ]
