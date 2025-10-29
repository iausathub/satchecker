Tools API
=============

Retrieve any NORAD ID(s) associated with a satellite name
-----------------------------------------------------------

.. http:get:: /norad-ids-from-name/
   :noindex:

    Find which NORAD ID(s) are associated with a satellite name, can be multiple in the case of
    temporary IDs

   :query name: (*required*) -- Name of satellite

**Example Request**
    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/norad-ids-from-name/?name=STARLINK-1600

        .. code-tab:: Python

            import requests
            import json

            url = 'https://satchecker.cps.iau.org/tools/norad-ids-from-name/'
            params = {'name': 'STARLINK-1600'}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://satchecker.cps.iau.org/tools/norad-ids-from-name/?name=STARLINK-1600" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://satchecker.cps.iau.org/tools/norad-ids-from-name/?name=STARLINK-1600" -H "accept: application/json"

**Example Response**

.. sourcecode:: json
    {
        "count": 1,
        "data": [
            {
                "date_added": "2024-02-06 00:12:42 UTC",
                "is_current_version": true,
                "norad_id": 46161,
                "name": "STARLINK-1600"
            }
        ],
        "source": "IAU CPS SatChecker",
        "version": "1.X.x"
    }

Retrieve any satellite names associated with a NORAD ID
-----------------------------------------------------------

.. http:get:: /names-from-norad-id/
   :noindex:

    Find which satellite names are associated with a given NORAD ID; names can occasionally
    change so can be more than one

   :query id: (*required*) -- NORAD id of satellite

**Example Request**
    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/names-from-norad-id/?id=59582

        .. code-tab:: Python

            import requests
            import json

            url = 'https://satchecker.cps.iau.org/tools/names-from-norad-id/'
            params = {'id': '59582'}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://satchecker.cps.iau.org/tools/names-from-norad-id/?id=59582" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://satchecker.cps.iau.org/tools/names-from-norad-id/?id=59582" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    {
        "count": 2,
        "data": [
            {
                "date_added": "2024-05-01 16:30:20 UTC",
                "is_current_version": true,
                "name": "STARLINK-31701",
                "norad_id": 59582
        },
        {
            "date_added": "2024-04-29 23:12:07 UTC",
            "is_current_version": false,
            "name": "TBA - TO BE ASSIGNED",
            "norad_id": 59582
            }
        ],
        "source": "IAU CPS SatChecker",
        "version": "1.X.x"
    }


Retrieve raw TLE data for a satellite over a given time period
---------------------------------------------------------------

.. http:get:: /get-tle-data/
   :noindex:

    Get the raw TLE data for a satellite over a given time period - the satellite can be
    identified by either name or NORAD ID. The time period is optional; if not provided,
    all TLE data available will be returned. The data source is also provided, since occasionally
    satellites with a given NORAD ID can have different preliminary names after launch. This will
    also help distinguish between similar or identical TLEs with different ``date_collected`` values.

   :query id: (*required*) -- identifier of satellite (name or NORAD ID)
   :query id_type: (*required*) -- type of identifier: valid values are "name" or "catalog"
   :query start_date_jd: (*optional*) -- start date (Julian date format) of time period to retrieve TLE data for
   :query end_date_jd: (*optional*) -- end date (Julian date format) of time period to retrieve TLE data for


**Example Request**
    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-tle-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427

        .. code-tab:: Python

            import requests
            import json

            url = 'https://satchecker.cps.iau.org/tools/get-tle-data/'
            params = {'id': '25544',
                      'id_type': 'catalog',
                      'start_date_jd': '2460425',
                      'end_date_jd': '2460427'
                    }

            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://satchecker.cps.iau.org/tools/get-tle-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-tle-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    {
        "count": 1,
        "data": [
            {
                "data_source": "celestrak",
                "date_collected": "2024-04-26 00:35:57 UTC",
                "epoch": "2024-04-25 18:22:37 UTC",
                "satellite_id": 25544,
                "satellite_name": "ISS (ZARYA)",
            "tle_line1": "1 25544U 98067A   24116.76570894  .00062894  00000+0  10654-2 0  9996",
            "tle_line2": "2 25544  51.6396 215.3361 0004566  95.7745   7.6568 15.50926567450413"
            }
        ],
        "source": "IAU CPS SatChecker",
        "version": "1.X.x"
    }


Retrieve satellite metadata
---------------------------------------------------------------

.. http:get:: /get-satellite-data/
   :noindex:

    Get the metadata that SatChecker currently has for a given satellite. This includes the
    satellite's name, NORAD ID, international designator, launch date, decay date, and
    any other relevant information.

   :query id: (*required*) -- identifier of satellite (name or NORAD ID)
   :query id_type: (*required*) -- type of identifier: valid values are "name" or "catalog"


**Example Request**
    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-satellite-data/?id=25544&id_type=catalog

        .. code-tab:: Python

            import requests
            import json

            url = 'https://satchecker.cps.iau.org/tools/get-satellite-data/'
            params = {'id': '25544',
                      'id_type': 'catalog'
                    }

            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://satchecker.cps.iau.org/tools/get-satellite-data/?id=25544&id_type=catalog" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-satellite-data/?id=25544&id_type=catalog" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

    {
        "count": 1,
        "data": [
            {
                "decay_date": null,
            "international_designator": "1998-067A",
            "launch_date": "1998-11-20",
            "object_type": "PAYLOAD",
            "rcs_size": "LARGE",
            "satellite_id": 25544,
            "satellite_name": "ISS (ZARYA)"
            }
        ],
        "source": "IAU CPS SatChecker",
        "version": "1.X.x"
    }


Get full TLE set at Epoch
---------------------------------------------------------------

This endpoint fetches all TLEs at a specific epoch date. It supports pagination to handle large result sets.
If the epoch date is not provided, it defaults to returning the most recent TLE for every active satellite/object
in the database (no decay date and current NORAD ID).

.. note::
    For an example on how to use this endpoint to get all TLEs for the current date using Python and a Pandas DataFrame,
    check out the :doc:`examples page <examples>`.

    If you need the TLE data in a single zip file, you can set the ``format`` query parameter to ``zip``.

**Endpoint**

.. http:get:: /tools/tles-at-epoch/

    **Parameters**

    :query epoch: (*optional*) -- The epoch date for the TLE data, in Julian Date format. Defaults to the current date if not provided.
    :query page: (*optional*) -- The page number for pagination. Defaults to 1.
    :query per_page: (*optional*) -- The number of results per page for pagination. Defaults to 100.
    :query format: (*optional*) -- The format of the response. Valid values are "json" (default), "txt", or "zip". The "zip" option will return a zip file containing a CSV file with the TLE data.

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/tles-at-epoch/?epoch=2459488.5&page=1&per_page=10

        .. tab:: Python

            .. code-tab:: Python

                import requests
                import json

                url = 'https://satchecker.cps.iau.org/tools/tles-at-epoch/'
                params = {'epoch': '2459488.5',
                          'page': '1',
                          'per_page': '10'
                        }

                r = requests.get(url, params=params)
                print(json.dumps(r.json(), indent=4))

        .. tab:: Bash

            .. code-tab:: Bash

                curl -X GET "https://satchecker.cps.iau.org/tools/tles-at-epoch/?epoch=2459488.5&page=1&per_page=10" -H "accept: application/json"

        .. tab:: Powershell

            .. code-tab:: Powershell

                curl.exe -X GET "https://satchecker.cps.iau.org/tools/tles-at-epoch/?epoch=2459488.5&page=1&per_page=10" -H "accept: application/json"

    **Example Response**

    .. sourcecode:: json

        [
            {
                "data": [
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-07-17 19:06:09 UTC",
                        "epoch": "2024-06-18 14:40:11 UTC",
                        "satellite_id": 26967,
                        "satellite_name": "DELTA 2 DEB",
                        "tle_line1": "1 26967U 93017E   24170.61124217  .00016791  00000-0  44967-3 0  9995",
                        "tle_line2": "2 26967  34.9300 154.9280 3885867 208.4643 123.3999  7.71838818573239"
                    },
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-07-17 19:06:09 UTC",
                        "epoch": "2024-06-20 16:17:21 UTC",
                        "satellite_id": 31723,
                        "satellite_name": "FENGYUN 1C DEB",
                        "tle_line1": "1 31723U 99025CDW 24172.67871604  .00004507  00000-0  26310-2 0  9996",
                        "tle_line2": "2 31723  97.8187 334.7099 0122012 256.7917 101.9619 14.05166935558935"
                    },
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-07-17 19:06:14 UTC",
                        "epoch": "2024-06-29 11:39:33 UTC",
                        "satellite_id": 270291,
                        "satellite_name": "TBA - TO BE ASSIGNED",
                        "tle_line1": "1 T0291U 11061F   24181.48580305  .07957539  53890-5  11314-2 0  9997",
                        "tle_line2": "2 T0291 101.6670  18.4903 0018493 268.3973  91.5188 16.34237302695039"
                    },
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-07-17 19:06:14 UTC",
                        "epoch": "2024-07-02 15:04:27 UTC",
                        "satellite_id": 59979,
                        "satellite_name": "TITAN 3C TRANSTAGE DEB",
                        "tle_line1": "1 59979U 68081AM  24184.62809922 -.00000169  00000-0  00000-0 0  9996",
                        "tle_line2": "2 59979   1.0181  53.6452 0044622 145.5716  26.1521  1.03320921 55136"
                    },
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-07-17 19:06:14 UTC",
                        "epoch": "2024-07-02 17:27:58 UTC",
                        "satellite_id": 59982,
                        "satellite_name": "TITAN 3C TRANSTAGE DEB",
                        "tle_line1": "1 59982U 68081AQ  24184.72776552 -.00000306  00000-0  00000-0 0  9996",
                        "tle_line2": "2 59982   1.7568 344.5114 0737782 293.5946  58.6594  0.99574789 12914"
                    }
                ],
                "page": 1,
                "per_page": 5,
                "source": "IAU CPS SatChecker",
                "total_results": 385,
                "version": "1.X.x"
            }
        ]

Retrieve active satellites
---------------------------------------------------------------

This endpoint retrieves all active satellites/objects from the database. Active satellites are defined
as those with no decay date and as having a current NORAD ID. This endpoint also supports filtering
by object type - "PAYLOAD", "DEBRIS", "ROCKET BODY", "TBA", or "UNKNOWN".

**Endpoint**

.. http:get:: /tools/get-active-satellites/

    **Parameters**

    :query object_type: (*optional*) -- The type of the object, either "payload", "debris", "rocket body", "tba", or "unknown".

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-active-satellites/?object_type=unknown

        .. code-tab:: Python

            import requests
            import json

            url = 'https://satchecker.cps.iau.org/tools/get-active-satellites/'
            params = {'object_type': 'unknown'}

            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. tab:: Bash

            curl -X GET "https://satchecker.cps.iau.org/tools/get-active-satellites/?object_type=unknown" -H "accept: application/json"

        .. tab:: Powershell

            curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-active-satellites/?object_type=unknown" -H "accept: application/json"

    **Example Response**

    .. sourcecode:: json

        {
            "count": 2,
            "data": [
                {
                    "decay_date": null,
                    "international_designator": "2024-110D",
                    "launch_date": "2024-06-06",
                    "object_type": "UNKNOWN",
                    "rcs_size": "SMALL",
                    "satellite_id": 60015,
                    "satellite_name": "OBJECT D"
                },
                {
                    "decay_date": null,
                    "international_designator": "2024-128A",
                    "launch_date": "2024-07-09",
                    "object_type": "UNKNOWN",
                    "rcs_size": "SMALL",
                    "satellite_id": 60235,
                    "satellite_name": "OBJECT A"
                }
            ],
            "source": "IAU CPS SatChecker",
            "version": "1.X.x"
    }


Search all satellites
---------------------------------------------------------------

This endpoint allows for searching all satellites/objects in the database. Search parameters
include the satellite name, NORAD ID, international designator, launch date, decay date, and
object type.

**Endpoint**

.. http:get:: /tools/search-satellites/

    **Parameters**

    :query name: (*optional*) -- The name of the satellite (partial matches supported)
    :query norad_id: (*optional*) -- The NORAD ID/catalog number of the satellite
    :query object_id: (*optional*) -- The international designator/COSPAR ID (e.g., "1998-067A")
    :query rcs_size: (*optional*) -- The radar cross-section size ("SMALL", "MEDIUM", "LARGE")
    :query launch_id: (*optional*) -- Search by launch ID (partial international designator, e.g., "1998-067")
    :query object_type: (*optional*) -- The type of object ("PAYLOAD", "DEBRIS", "ROCKET BODY", "TBA", "UNKNOWN")
    :query launch_date_start: (*optional*) -- Filter objects launched after this date (Julian Date)
    :query launch_date_end: (*optional*) -- Filter objects launched before this date (Julian Date)
    :query decay_date_start: (*optional*) -- Filter objects that decayed after this date (Julian Date)
    :query decay_date_end: (*optional*) -- Filter objects that decayed before this date (Julian Date)

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/search-satellites/?object_type=payload&launch_date_start=2024-01-01

        .. code-tab:: Python

            import requests
            import json

            url = 'https://satchecker.cps.iau.org/tools/search-satellites/'
            params = {
                'object_type': 'payload',
                'launch_date_start': '2460311.5'
            }

            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://satchecker.cps.iau.org/tools/search-satellites/?object_type=payload&launch_date_start=2024-01-01" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://satchecker.cps.iau.org/tools/search-satellites/?object_type=payload&launch_date_start=2024-01-01" -H "accept: application/json"

    **Example Response**

    .. sourcecode:: json

        {
            "count": 2,
            "data": [
                {
                    "decay_date": null,
                    "international_designator": "2024-110D",
                    "launch_date": "2024-06-06",
                    "object_type": "PAYLOAD",
                    "rcs_size": "SMALL",
                    "satellite_id": 60015,
                    "satellite_name": "STARLINK-5234"
                },
                {
                    "decay_date": null,
                    "international_designator": "2024-128A",
                    "launch_date": "2024-07-09",
                    "object_type": "PAYLOAD",
                    "rcs_size": "SMALL",
                    "satellite_id": 60235,
                    "satellite_name": "STARLINK-5678"
                }
            ],
            "source": "IAU CPS SatChecker",
            "version": "1.X.x"
        }
