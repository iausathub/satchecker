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