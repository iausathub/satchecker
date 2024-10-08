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

    [
        {
            "date_added": "2024-02-06 00:12:42 UTC",
            "is_current_version": true,
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

    [
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
    ]


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

    [
        {
            "data_source": "celestrak",
            "date_collected": "2024-04-26 00:35:57 UTC",
            "epoch": "2024-04-25 18:22:37 UTC",
            "satellite_id": 25544,
            "satellite_name": "ISS (ZARYA)",
            "tle_line1": "1 25544U 98067A   24116.76570894  .00062894  00000+0  10654-2 0  9996",
            "tle_line2": "2 25544  51.6396 215.3361 0004566  95.7745   7.6568 15.50926567450413"
        }
    ]


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

    [
        {
            "decay_date": null,
            "international_designator": "1998-067A",
            "launch_date": "1998-11-20",
            "object_type": "PAYLOAD",
            "rcs_size": "LARGE",
            "satellite_id": 25544,
            "satellite_name": "ISS (ZARYA)"
        }
    ]
