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

        .. code-tab:: Python

            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/tools/norad-ids-from-name/'
            params = {'name': 'STARLINK-1600'}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/tools/norad-ids-from-name/?name=STARLINK-1600" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://cps.iau.org/tools/satchecker/api/tools/norad-ids-from-name/?name=STARLINK-1600" -H "accept: application/json"

        .. tab:: Link

            https://cps.iau.org/tools/satchecker/api/tools/norad-ids-from-name/?name=STARLINK-1600

**Example Response**

.. sourcecode:: json

    [
        {
            "date_added": "2024-02-06 00:12:42 UTC",
            "norad_id": 46161,
            "name": "STARLINK-1600"
        }
    ]

Retrieve any satellite names associated with a NORAD ID
-----------------------------------------------------------

.. http:get:: /names-from-norad-id/
   :noindex:

    Find which satellite names are associated with a given NORAD ID; names can occasionally
    change so can be more than one

   :query id: (*required*) -- NORAD id of satellite

**Example Request**
    .. tabs::

        .. code-tab:: Python

            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/tools/names-from-norad-id/'
            params = {'id': '59582'}
            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/tools/names-from-norad-id/?id=59582" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://cps.iau.org/tools/satchecker/api/tools/names-from-norad-id/?id=59582" -H "accept: application/json"

        .. tab:: Link

            https://cps.iau.org/tools/satchecker/api/tools/names-from-norad-id/?id=59582

**Example Response**

.. sourcecode:: json

    [
        {
            "date_added": "2024-05-01 16:30:20 UTC",
            "name": "STARLINK-31701",
            "norad_id": 59582
        },
        {
            "date_added": "2024-04-29 23:12:07 UTC",
            "name": "TBA - TO BE ASSIGNED",
            "norad_id": 59582
        }
    ]


Retrieve raw TLE data for a satellite over a given time period
---------------------------------------------------------------

.. http:get:: /get-tle-data/
   :noindex:

    Get the raw TLE data for a satellite over a given time period - the satellite can be
    identified by either name or NORAD ID. The time period is optional; if not provided,
    all TLE data available will be returned.

   :query id: (*required*) -- identifier of satellite (name or NORAD ID)
   :query id_type: (*required*) -- type of identifier: valid values are "name" or "catalog"
   :query start_date_jd: (*optional*) -- start date (Julian date format) of time period to retrieve TLE data for
   :query end_date_jd: (*optional*) -- end date (Julian date format) of time period to retrieve TLE data for


**Example Request**
    .. tabs::

        .. code-tab:: Python

            import requests
            import json

            url = 'https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/'
            params = {'id': '25544',
                      'id_type': 'catalog',
                      'start_date_jd': '2460425',
                      'end_date_jd': '2460427'
                    }

            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427" -H "accept: application/json"

        .. tab:: Link

            https://cps.iau.org/tools/satchecker/api/tools/get-tle-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427

**Example Response**

.. sourcecode:: json

    [
        {
            "date_collected": "2024-04-26 00:35:57 UTC",
            "epoch": "2024-04-25 18:22:37 UTC",
            "satellite_id": 25544,
            "satellite_name": "ISS (ZARYA)",
            "tle_line1": "1 25544U 98067A   24116.76570894  .00062894  00000+0  10654-2 0  9996",
            "tle_line2": "2 25544  51.6396 215.3361 0004566  95.7745   7.6568 15.50926567450413"
        }
    ]
