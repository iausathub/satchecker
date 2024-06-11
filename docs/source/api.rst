Ephemeris API
=============

Retrieve satellite ephemeris by name with JD time step
-----------------------------------------------------------

.. http:get:: /name-jdstep/
   :noindex:

    Retrieve the satellite ephemeris over a JD range at a specified time step. The time step is the interval between each ephemeris point, and
    is specified as a Julian Day (JD) value. *.05 JD* is approximately 1.2 hours.

   :query name: (*required*) -- Name of satellite as displayed in CelesTrak TLE files
   :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
   :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg)
   :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
   :query startjd: (*required*) -- UT1 Julian Start Date
   :query stopjd: (*required*) -- UT1 Julian End Date
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

`API Response Details <api_response.html>`_


Retrieve satellite ephemeris by name
-----------------------------------------------------------

.. http:get:: /name/
    :noindex:

    Retrieve the ephemeris for specified satellite at a specific Julian Date given its name

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

`API Response Details <api_response.html>`_


Retrieve satellite ephemeris by catalog number with JD time step
-----------------------------------------------------------------

.. http:get:: /catalog-number-jdstep/
    :noindex:

    Retrieve the satellite ephemeris over a JD range at a specified time step (optional). The time step is the interval between each ephemeris point, and
    is specified as a Julian Day (JD) value. *.05 JD* is approximately 1.2 hours. The catalog number is the NORAD ID of the satellite.

    :query catalog: (*required*) -- Satellite catalog number (NORAD ID)
    :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
    :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg)
    :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
    :query startjd: (*required*) -- UT1 Julian Start Date
    :query stopjd: (*required*) -- UT1 Julian End Date
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

`API Response Details <api_response.html>`_


Retrieve satellite ephemeris by catalog number
-----------------------------------------------------------

.. http:get:: /catalog-number/
    :noindex:

    Retrieve the ephemeris for a satellite at a specific Julian Date given its catalog number (NORAD ID)

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

`API Response Details <api_response.html>`_


Calculate satellite ephemeris given a TLE with JD time step
-----------------------------------------------------------

.. http:get:: /tle-jdstep/
   :noindex:

    Calculate satellite ephemeris with a user-specified TLE over a JD range at a specified time step

    :query tle: (*required*) -- Two line element set
    :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
    :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg)
    :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
    :query startjd: (*required*) -- UT1 Julian Start Date
    :query stopjd: (*required*) -- UT1 Julian End Date
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

`API Response Details <api_response.html>`_


Calculate satellite ephemeris with a given TLE
-----------------------------------------------------------

.. http:get:: /tle/
    :noindex:

    Calculate satellite ephemeris with a user-specified TLE at a specific Julian Date

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

`API Response Details <api_response.html>`_
