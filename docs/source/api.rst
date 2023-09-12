Ephemeris API
=============

Retrieve satellite ephemeris by name with JD time step
-----------------------------------------------------------

.. http:get:: /namejdstep/
   :noindex:

    Retrieve ephemeris over a JD range at a specified time step
	
   :query name: (*required*) -- Name of satellite as displayed in CelesTrak TLE files
   :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
   :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg) 
   :query elevation: (*required*) -- Observer Elevation above WGS84 ellipsoid in meters (m)
   :query jdstart: (*required*) -- UT1 Julian Start Date
   :query jdstop: (*required*) -- UT1 Julian End Date (not included)
   :query jdstep: (*required*) -- UT1 time step in Julian Days for ephemeris generation


**Example Request**
    .. tabs::

        .. code-tab:: python
                    
            import requests
            import json

            url = 'http://localhost:5000/ephemeris/namejdstep/'
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

            curl -X GET "http://localhost:5000/ephemeris/namejdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1" -H "accept: application/json"


**Example Response**

.. sourcecode:: json

    [
        {
            "ALTITUDE-DEG":-29.78246259438,
            "AZIMUTH-DEG":238.15143403374,
            "DECLINATION-DEG":-41.96082320669,
            "JULIAN_DATE":2460000.1,
            "NAME":"STARLINK-1600",
            "RANGE-KM":7326.701930124387,
            "RIGHT_ASCENSION-DEG":185.13183802078,
            "TLE-DATE": "2023-09-05 16:20:25"
        },
        
        {
            "ALTITUDE-DEG":-42.16061726731,
            "AZIMUTH-DEG":84.00454809553,
            "DECLINATION-DEG":-21.92703874377,
            "JULIAN_DATE":2460000.2,
            "NAME":"STARLINK-1600",
            "RANGE-KM":9350.895389533023,
            "RIGHT_ASCENSION-DEG":85.23319796871,
            "TLE-DATE": "2023-09-05 16:20:25"
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

            url = 'http://localhost:5000/ephemeris/name/'
            params = {'name': 'STARLINK-1600',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'elevation': 222,
                            'julian_date': 2460000.1}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: bash

            curl -X GET "http://localhost:5000/ephemeris/name/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1" -H "accept: application/json"


**Example Response**

.. sourcecode:: json

    [
        {
            "ALTITUDE-DEG": -83.91400834026,
            "AZIMUTH-DEG": 74.32293067711,
            "DECLINATION-DEG": -38.21523985508,
            "JULIAN_DATE": 2460000.1,
            "NAME": "STARLINK-1600",
            "RANGE-KM": 13235.93643713937,
            "RIGHT_ASCENSION-DEG": 94.33852620559
        }
    ]

Retrieve ephemeris using TLE
-----------------------------------------------------------

.. http:get:: /tle/
    :noindex:

    Retrieve ephemeris for a satellite given a specified TLE

    .. warning::
        This is currently not working, so examples are not correct and are just included as a placeholder.
	
    :query tle: (*required*) -- The Two Line Element set for the specified satellite
    :query latitude: (*required*) -- Observer Latitude (North is positive) (decimal deg)
    :query longitude: (*required*) -- Observer Longitude (East is positive) (decimal deg)
    :query julian_date: (*required*) -- UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    :query elevation: (*optional*) -- The elevation of the observer in meters. Default is 0
    :query jpl: (*optional*) -- If 'true', will return JPL ephemeris response. If 'false', will return Skyfield ephemeris. Default is 'false'.
            This assumes that the TLE uses the ASCII representation for newline, which is '%0A'

**Example Request**
    .. tabs::

        .. code-tab:: python
                    
            import requests
            import json

            url = 'http://localhost:5000/ephemeris/tle/'
            params = {'tle': '1 44238U 19029B   20173.50000000  .00000000  00000-0  00000-0 0  9999%0A2 44238  53.0000  52.0000 0001400   0.0000  90.0000 15.05500000    10',
                            'latitude': 40.1106,
                            'longitude': -88.2073,
                            'julian_date': 2460000.1}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: bash

            curl -X GET "http://localhost:5000/ephemeris/tle/?tle=1 44238U 19029B   20173.50000000  .00000000  00000-0  00000-0 0  9999%0A2 44238  53.0000  52.0000 0001400   0.0000  90.0000 15.05500000    10&latitude=40.1106&longitude=-88.2073&julian_date=2460000.1" -H "accept: application/json"


**Example Response**

.. sourcecode:: json

    [
        {
            "RIGHT_ASCENSION-DEG":185.13183802078,
            "DECLINATION-DEG":-41.96082320669,
            "ALTITUDE-DEG":-29.78246259438,
            "AZIMUTH-DEG":238.15143403374
        }
    ]