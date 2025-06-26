Field of View (FOV) Endpoints
==============================

The FOV API provides two main endpoints for checking satellite positions relative to a field of view or horizon.

Satellite passes Through FOV
-----------------------------

.. http:get:: /satellite-passes/
   :noindex:

    Get satellites that pass through a specified field of view during a time period. The field of view is
    defined by a center RA and Dec and a radius, both in degrees.

    Either a start time or observation mid point time can be provided, but one must be specified.

   :query latitude: (*required*) -- Observer's latitude in degrees
   :query longitude: (*required*) -- Observer's longitude in degrees
   :query elevation: (*required*) -- Observer's elevation in meters
   :query site: (*optional*) -- Site name (e.g. 'greenwich') - if provided, latitude, longitude, and elevation can't be used; see `astropy site names <https://www.astropy.org/astropy-data/coordinates/sites.json>`_ for a list of valid site names
   :query start_time_jd: (*optional*) -- Julian Date for start of observation window
   :query mid_obs_time_jd: (*optional*) -- Julian Date for middle of observation window
   :query duration: (*required*) -- Duration to check in seconds
   :query ra: (*required*) -- Right Ascension of FOV center in degrees
   :query dec: (*required*) -- Declination of FOV center in degrees
   :query fov_radius: (*required*) -- Radius of circular FOV in degrees
   :query group_by: (*optional*) -- How to group results ("satellite" or "time"). Default is "time" for chronological order
   :query include_tles: (*optional*) -- If True, include TLE data used to calculate the passes in the response. Default is False.
   :query constellation: (*optional*) -- Constellation name (e.g. 'starlink') - if provided, only satellites from this constellation will be returned.
   :query data_source: (*optional*) -- Data source to use for TLEs ("celestrak", "spacetrack", or "any"). Default is "any".

**Example Request**
    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/fov/satellite-passes/?latitude=33&longitude=-117&elevation=100&start_time_jd=2460623.394780&duration=2&ra=157.5&dec=20&fov_radius=3&group_by=satellite

        .. code-tab:: Python

            import requests
            import json

            url = 'https://satchecker.cps.iau.org/fov/satellite-passes/'
            params = {'latitude': 33, 'longitude': -117, 'elevation': 100, 'start_time_jd': 2460623.394780, 'duration': 2, 'ra': 157.5, 'dec': 20, 'fov_radius': 3, 'group_by': 'satellite'}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://satchecker.cps.iau.org/fov/satellite-passes/?latitude=33&longitude=-117&elevation=100&start_time_jd=2460623.394780&duration=2&ra=157.5&dec=20&fov_radius=3&group_by=satellite" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://satchecker.cps.iau.org/fov/satellite-passes/?latitude=33&longitude=-117&elevation=100&start_time_jd=2460623.394780&duration=2&ra=157.5&dec=20&fov_radius=3&group_by=satellite" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    [
        {
            "data": {
                "satellites": {
                    "ATLAS 2AS CENTAUR R/B (26636)": {
                        "name": "ATLAS 2AS CENTAUR R/B",
                        "norad_id": 26636,
                        "positions": [
                            {
                                "altitude": 3.82923609,
                                "angle": 2.77084316,
                                "azimuth": 288.11992936,
                                "date_time": "2024-11-08 21:28:28 UTC",
                                "dec": 17.38072389,
                                "julian_date": 2460623.39478,
                                "ra": 156.5457069,
                                "tle_epoch": "2024-11-08 14:22:35 UTC"
                            },
                            {
                                "altitude": 3.8301086,
                                "angle": 2.7698136,
                                "azimuth": 288.11836715,
                                "date_time": "2024-11-08 21:28:29 UTC",
                                "dec": 17.37990928,
                                "julian_date": 2460623.39479157,
                                "ra": 156.55155138,
                                "tle_epoch": "2024-11-08 14:22:35 UTC"
                            }
                        ]
                    },
                    "STARLINK-30904 (58364)": {
                        "name": "STARLINK-30904",
                        "norad_id": 58364,
                        "positions": [
                            {
                                "altitude": 8.10566642,
                                "angle": 2.95246402,
                                "azimuth": 291.92818711,
                                "date_time": "2024-11-08 21:28:28 UTC",
                                "dec": 22.88675663,
                                "julian_date": 2460623.39478,
                                "ra": 158.16558783,
                                "tle_epoch": "2024-11-08 14:22:35 UTC"
                            },
                            {
                                "altitude": 8.18998929,
                                "angle": 2.97995215,
                                "azimuth": 291.87936333,
                                "date_time": "2024-11-08 21:28:29 UTC",
                                "dec": 22.89132111,
                                "julian_date": 2460623.39479157,
                                "ra": 158.27515227,
                                "tle_epoch": "2024-11-08 14:22:35 UTC"
                            }
                        ]
                    },
                    "STARLINK-30925 (58406)": {
                        "name": "STARLINK-30925",
                        "norad_id": 58406,
                        "positions": [
                            {
                                "altitude": 3.8560731,
                                "angle": 2.30309691,
                                "azimuth": 289.0338456,
                                "date_time": "2024-11-08 21:28:28 UTC",
                                "dec": 18.15569881,
                                "julian_date": 2460623.39478,
                                "ra": 156.04031939,
                                "tle_epoch": "2024-11-08 14:22:35 UTC"
                            },
                            {
                                "altitude": 3.91713221,
                                "angle": 2.21383004,
                                "azimuth": 289.12315208,
                                "date_time": "2024-11-08 21:28:29 UTC",
                                "dec": 18.26370601,
                                "julian_date": 2460623.39479157,
                                "ra": 156.04618993,
                                "tle_epoch": "2024-11-08 14:22:35 UTC"
                            }
                        ]
                    }
                "total_position_results": 6,
                "total_satellites": 3
            },
            "source": "IAU CPS SatChecker",
            "version": "1.X.x"
        }
    ]


Satellites above the horizon
-----------------------------

.. http:get:: /satellites-above-horizon/
   :noindex:

    Get satellites that are above the horizon at a given time. A minimum altitude can be specified to filter results.

   :query latitude: (*required*) -- Observer's latitude in degrees
   :query longitude: (*required*) -- Observer's longitude in degrees
   :query elevation: (*required*) -- Observer's elevation in meters
   :query site: (*optional*) -- Site name (e.g. 'greenwich') - if provided, latitude, longitude, and elevation can't be used; see `astropy site names <https://www.astropy.org/astropy-data/coordinates/sites.json>`_ for a list of valid site names
   :query julian_date: (*required*) -- Julian Date for time to check
   :query min_altitude: (*optional*) -- Minimum altitude in degrees. Default is 0.
   :query min_range: (*optional*) -- Minimum range in kilometers. Default is 0.
   :query max_range: (*optional*) -- Maximum range in kilometers. Default is 1500000.
   :query illuminated_only: (*optional*) -- If True, only return satellites that are illuminated. Default is False.
   :query constellation: (*optional*) -- Constellation name (e.g. 'starlink') - if provided, only satellites from this constellation will be returned.


**Example Request**
    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/fov/satellites-above-horizon/?latitude=33&longitude=-117&elevation=100&julian_date=2460623.394780&min_altitude=10

        .. code-tab:: Python

            import requests
            import json

            url = 'https://satchecker.cps.iau.org/fov/satellites-above-horizon/'
            params = {'latitude': 33, 'longitude': -117, 'elevation': 100, 'julian_date': 2460623.394780, 'min_altitude': 10}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://satchecker.cps.iau.org/fov/satellites-above-horizon/?latitude=33&longitude=-117&elevation=100&julian_date=2460623.394780&min_altitude=10" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://satchecker.cps.iau.org/fov/satellites-above-horizon/?latitude=33&longitude=-117&elevation=100&julian_date=2460623.394780&min_altitude=10" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    [
        {
            "count": 1937,
            "data": [
                {
                    "altitude": 51.92871704504127,
                    "azimuth": 330.07034475807336,
                    "dec": 61.393238361137435,
                    "julian_date": 2460623.39478,
                    "name": "COSMOS 1217 DEB",
                    "norad_id": 27899,
                    "ra": 213.68861951924774,
                    "range": 37871.88385502476,
                    "tle_epoch": "2024-11-08 14:22:35 UTC"
                },
                {
                    "altitude": 46.76140648358198,
                    "azimuth": 39.30197941616954,
                    "dec": 57.20169110572095,
                    "julian_date": 2460623.39478,
                    "name": "TBA - TO BE ASSIGNED",
                    "norad_id": 270191,
                    "ra": 306.93103651702273,
                    "range": 1868.7413807374958,
                    "tle_epoch": "2024-11-08 14:22:35 UTC"
                },
                {
                    "altitude": 43.309023015726,
                    "azimuth": 297.19742445889455,
                    "dec": 40.865606494876005,
                    "julian_date": 2460623.39478,
                    "name": "TESS",
                    "norad_id": 43435,
                    "ra": 194.72756014363964,
                    "range": 120182.57514042286,
                    "tle_epoch": "2024-11-08 14:22:35 UTC"
                }
            ],
            "source": "IAU CPS SatChecker",
            "version": "1.X.x"
        }
    ]
