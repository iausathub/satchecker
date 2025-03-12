Satellite Information
=====================



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
            "version": "1.2.0"
    }
