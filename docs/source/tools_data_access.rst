Orbital Data Access
===================

SatChecker stores orbital data in two formats:

- **TLE** (two-line element set) -- the classic format. TLEs remain the record for
  historical dates and are available through the ``get-tle-data``, ``tles-at-epoch``,
  ``get-nearest-tle``, ``get-adjacent-tles``, and ``get-tles-around-epoch`` endpoints.
- **OMM** (Orbital Mean-Element Message) -- the CCSDS orbital-element format sourced
  from CelesTrak and Space-Track, used going forward and available through the matching
  ``get-omm-data``, ``omms-at-epoch``, ``get-nearest-omm``, ``get-adjacent-omms``, and
  ``get-omms-around-epoch`` endpoints.

The two sets of endpoints are symmetric: for every TLE endpoint there is an OMM
endpoint that accepts the same query parameters and returns the same response
envelope, differing only in the per-record payload (``tle_line1``/``tle_line2`` for
TLE, an ``orbital_elements`` object of CCSDS OMM fields for OMM).

The data source is provided with each record, since occasionally satellites with a
given NORAD ID can have different preliminary names after launch. This also helps
distinguish between similar or identical records with different ``date_collected``
values.

TLE Data Access
---------------

Retrieve raw TLE data for a satellite over a given time period
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. http:get:: /tools/get-tle-data/
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

Get full TLE set at epoch
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
                    }
                ],
                "page": 1,
                "per_page": 5,
                "source": "IAU CPS SatChecker",
                "total_results": 385,
                "version": "1.X.x"
            }
        ]

Get nearest TLE
~~~~~~~~~~~~~~~~

This endpoint fetches the TLE closest to a specific epoch date. It supports searching
by either name or NORAD ID, but due to inconsistencies in satellite naming, it is recommended
to use the NORAD ID. Sometimes the closest TLE by name might not actually be the closest
TLE for a particular object if the name changed around that time. If you use the name,
check the epoch of the TLE to make sure that it is suitable for your needs.

**Endpoint**

.. http:get:: /tools/get-nearest-tle/

    **Parameters**

    :query id: (*required*) -- The identifier of the satellite (name or NORAD ID).
    :query id_type: (*required*) -- The type of identifier: valid values are "name" or "catalog".
    :query epoch: (*required*) -- The epoch date for the TLE data, in Julian Date format.

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-nearest-tle/?id=25544&id_type=catalog&epoch=2460000

        .. tab:: Python

            .. code-tab:: Python

                import requests
                import json

                url = 'https://satchecker.cps.iau.org/tools/get-nearest-tle/'
                params = {'id': '25544',
                          'id_type': 'catalog',
                          'epoch': '2460000'
                        }

                r = requests.get(url, params=params)
                print(json.dumps(r.json(), indent=4))

        .. tab:: Bash

            .. code-tab:: Bash

                curl -X GET "https://satchecker.cps.iau.org/tools/get-nearest-tle/?id=25544&id_type=catalog&epoch=2460000" -H "accept: application/json"

        .. tab:: Powershell

            .. code-tab:: Powershell

                curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-nearest-tle/?id=25544&id_type=catalog&epoch=2460000" -H "accept: application/json"

    **Example Response**

    .. sourcecode:: json

        [
            {
                "source": "IAU CPS SatChecker",
                "orbital_data": [
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-06-04 19:16:53 UTC",
                        "epoch": "2024-01-30 02:26:07 UTC",
                        "satellite_id": 25544,
                        "satellite_name": "ISS (ZARYA)",
                        "tle_line1": "1 25544U 98067A   24030.10147156  .00014904  00000-0  27473-3 0  9998",
                        "tle_line2": "2 25544  51.6414 284.5574 0002475 176.3471 287.7672 15.49357173436989"
                    }
                ],
                "version": "1.X.x"
            }
        ]

Get adjacent TLEs
~~~~~~~~~~~~~~~~~~

This endpoint fetches the TLEs right before and after a specific epoch date. It currently only supports searching
by NORAD ID.

**Endpoint**

.. http:get:: /tools/get-adjacent-tles/

    **Parameters**

    :query id: (*required*) -- The identifier of the satellite  (NORAD ID).
    :query id_type: (*required*) -- The type of identifier: valid values are "catalog".
    :query epoch: (*required*) -- The epoch date for the TLE data, in Julian Date format.

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-adjacent-tles/?id=25544&id_type=catalog&epoch=2460000

        .. tab:: Python

            .. code-tab:: Python

                import requests
                import json

                url = 'https://satchecker.cps.iau.org/tools/get-adjacent-tles/'
                params = {'id': '25544',
                          'id_type': 'catalog',
                          'epoch': '2460000'
                        }

                r = requests.get(url, params=params)
                print(json.dumps(r.json(), indent=4))

        .. tab:: Bash

            .. code-tab:: Bash

                curl -X GET "https://satchecker.cps.iau.org/tools/get-adjacent-tles/?id=25544&id_type=catalog&epoch=2460000" -H "accept: application/json"

        .. tab:: Powershell

            .. code-tab:: Powershell

                curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-adjacent-tles/?id=25544&id_type=catalog&epoch=2460000" -H "accept: application/json"

    **Example Response**

    .. sourcecode:: json

        [
            {
                "source": "IAU CPS SatChecker",
                "orbital_data": [
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-11-26 17:37:22 UTC",
                        "epoch": "2019-06-30 20:27:51 UTC",
                        "satellite_id": 25544,
                        "satellite_name": "ISS (ZARYA)",
                        "tle_line1": "1 25544U 98067A   19181.85268126 -.00006926  00000-0 -10819-3 0  9995",
                        "tle_line2": "2 25544  51.6486 293.4711 0008267 104.5225  41.1392 15.51249855177371"
                    },
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-06-04 19:16:53 UTC",
                        "epoch": "2024-01-30 02:26:07 UTC",
                        "satellite_id": 25544,
                        "satellite_name": "ISS (ZARYA)",
                        "tle_line1": "1 25544U 98067A   24030.10147156  .00014904  00000-0  27473-3 0  9998",
                        "tle_line2": "2 25544  51.6414 284.5574 0002475 176.3471 287.7672 15.49357173436989"
                    }
                ],
                "version": "1.X.x"
            }
        ]

Get TLEs around a specific epoch date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This endpoint fetches a requested number of TLEs before and/or after a specific epoch date.
It currently only supports searching by NORAD ID.

**Endpoint**

.. http:get:: /tools/get-tles-around-epoch/

    **Parameters**

    :query id: (*required*) -- The identifier of the satellite  (NORAD ID).
    :query id_type: (*required*) -- The type of identifier: valid values are "catalog".
    :query epoch: (*required*) -- The epoch date for the TLE data, in Julian Date format.
    :query count_before: (*optional*) -- The number of TLEs before the specified epoch date. Defaults to 2.
    :query count_after: (*optional*) -- The number of TLEs after the specified epoch date. Defaults to 2.

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch=2460000&count_before=1&count_after=1

        .. tab:: Python

            .. code-tab:: Python

                import requests
                import json

                url = 'https://satchecker.cps.iau.org/tools/get-tles-around-epoch/'
                params = {'id': '25544',
                          'id_type': 'catalog',
                          'epoch': '2460000',
                          'count_before': '1',
                          'count_after': '1'
                        }

                r = requests.get(url, params=params)
                print(json.dumps(r.json(), indent=4))

        .. tab:: Bash

            .. code-tab:: Bash

                curl -X GET "https://satchecker.cps.iau.org/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch=2460000&count_before=1&count_after=1" -H "accept: application/json"

        .. tab:: Powershell

            .. code-tab:: Powershell

                curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch=2460000&count_before=1&count_after=1" -H "accept: application/json"

    **Example Response**

    .. sourcecode:: json

        [
            {
                "source": "IAU CPS SatChecker",
                "orbital_data": [
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-11-26 17:37:22 UTC",
                        "epoch": "2019-06-30 20:27:51 UTC",
                        "satellite_id": 25544,
                        "satellite_name": "ISS (ZARYA)",
                        "tle_line1": "1 25544U 98067A   19181.85268126 -.00006926  00000-0 -10819-3 0  9995",
                        "tle_line2": "2 25544  51.6486 293.4711 0008267 104.5225  41.1392 15.51249855177371"
                    },
                    {
                        "data_source": "spacetrack",
                        "date_collected": "2024-06-04 19:16:53 UTC",
                        "epoch": "2024-01-30 02:26:07 UTC",
                        "satellite_id": 25544,
                        "satellite_name": "ISS (ZARYA)",
                        "tle_line1": "1 25544U 98067A   24030.10147156  .00014904  00000-0  27473-3 0  9998",
                        "tle_line2": "2 25544  51.6414 284.5574 0002475 176.3471 287.7672 15.49357173436989"
                    }
                ],
                "version": "1.X.x"
            }
        ]

OMM Data Access
---------------

The OMM endpoints mirror the TLE endpoints above. Each accepts the same query
parameters as its TLE counterpart and returns the same response envelope; the
per-record payload replaces ``tle_line1``/``tle_line2`` with an ``orbital_elements``
object containing the CCSDS OMM fields (``OBJECT_NAME``, ``OBJECT_ID``, ``EPOCH``,
``MEAN_MOTION``, ``ECCENTRICITY``, ``INCLINATION``, ``RA_OF_ASC_NODE``,
``ARG_OF_PERICENTER``, ``MEAN_ANOMALY``, ``EPHEMERIS_TYPE``, ``CLASSIFICATION_TYPE``,
``NORAD_CAT_ID``, ``ELEMENT_SET_NO``, ``REV_AT_EPOCH``, ``BSTAR``, ``MEAN_MOTION_DOT``,
``MEAN_MOTION_DDOT``). These are the exact field names required by
``sgp4.omm.initialize()``, so the ``orbital_elements`` object can be passed straight
to an OMM propagator.

.. note::
    The ``EPOCH`` inside ``orbital_elements`` uses the CCSDS ISO format
    (``YYYY-MM-DDTHH:MM:SS.ffffff``), while the record-level ``epoch`` field uses the
    SatChecker ``YYYY-MM-DD HH:MM:SS UTC`` format for consistency with the TLE
    endpoints.

Retrieve OMM data for a satellite over a given time period
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. http:get:: /tools/get-omm-data/
   :noindex:

    Get the OMM data for a satellite over a given time period - the satellite can be
    identified by either name or NORAD ID. The time period is optional; if not provided,
    all OMM data available will be returned.

   :query id: (*required*) -- identifier of satellite (name or NORAD ID)
   :query id_type: (*required*) -- type of identifier: valid values are "name" or "catalog"
   :query start_date_jd: (*optional*) -- start date (Julian date format) of time period to retrieve OMM data for
   :query end_date_jd: (*optional*) -- end date (Julian date format) of time period to retrieve OMM data for


**Example Request**
    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-omm-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427

        .. code-tab:: Python

            import requests
            import json

            url = 'https://satchecker.cps.iau.org/tools/get-omm-data/'
            params = {'id': '25544',
                      'id_type': 'catalog',
                      'start_date_jd': '2460425',
                      'end_date_jd': '2460427'
                    }

            r = requests.get(url, params=params)
            print(json.dumps(r.json(), indent=4))

        .. code-tab:: Bash

            curl -X GET "https://satchecker.cps.iau.org/tools/get-omm-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427" -H "accept: application/json"

        .. code-tab:: Powershell

            curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-omm-data/?id=25544&id_type=catalog&start_date_jd=2460425&end_date_jd=2460427" -H "accept: application/json"

**Example Response**

.. sourcecode:: json

        {
            "count": 1,
            "data": [
                {
                    "satellite_name": "ISS (ZARYA)",
                    "satellite_id": 25544,
                    "orbital_elements": {
                        "OBJECT_NAME": "ISS (ZARYA)",
                        "OBJECT_ID": "1998-067A",
                        "EPOCH": "2024-04-25T18:22:37.000000",
                        "MEAN_MOTION": 15.50926567,
                        "ECCENTRICITY": 0.0004566,
                        "INCLINATION": 51.6396,
                        "RA_OF_ASC_NODE": 215.3361,
                        "ARG_OF_PERICENTER": 95.7745,
                        "MEAN_ANOMALY": 7.6568,
                        "EPHEMERIS_TYPE": 0,
                        "CLASSIFICATION_TYPE": "U",
                        "NORAD_CAT_ID": 25544,
                        "ELEMENT_SET_NO": 999,
                        "REV_AT_EPOCH": 45041,
                        "BSTAR": 0.0010654,
                        "MEAN_MOTION_DOT": 0.00062894,
                        "MEAN_MOTION_DDOT": 0.0
                    },
                    "epoch": "2024-04-25 18:22:37 UTC",
                    "date_collected": "2024-04-26 00:35:57 UTC",
                    "data_source": "celestrak"
                }
            ],
            "source": "IAU CPS SatChecker",
            "version": "1.X.x"
        }

Get full OMM set at epoch
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This endpoint fetches all OMMs at a specific epoch date. It supports pagination to handle large result sets.
If the epoch date is not provided, it defaults to returning the most recent OMM for every active satellite/object
in the database (no decay date and current NORAD ID).

.. note::
    If you need the OMM data in a single zip file, you can set the ``format`` query parameter to ``zip``,
    which returns a CSV using the CCSDS OMM field names plus the SatChecker metadata columns.

**Endpoint**

.. http:get:: /tools/omms-at-epoch/

    **Parameters**

    :query epoch: (*optional*) -- The epoch date for the OMM data, in Julian Date format. Defaults to the current date if not provided.
    :query page: (*optional*) -- The page number for pagination. Defaults to 1.
    :query per_page: (*optional*) -- The number of results per page for pagination. Defaults to 100.
    :query format: (*optional*) -- The format of the response. Valid values are "json" (default) or "zip". The "zip" option will return a zip file containing a CSV file with the OMM data.

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/omms-at-epoch/?epoch=2460500.5&page=1&per_page=10

        .. tab:: Python

            .. code-tab:: Python

                import requests
                import json

                url = 'https://satchecker.cps.iau.org/tools/omms-at-epoch/'
                params = {'epoch': '2460500.5',
                          'page': '1',
                          'per_page': '10'
                        }

                r = requests.get(url, params=params)
                print(json.dumps(r.json(), indent=4))

        .. tab:: Bash

            .. code-tab:: Bash

                curl -X GET "https://satchecker.cps.iau.org/tools/omms-at-epoch/?epoch=2460500.5&page=1&per_page=10" -H "accept: application/json"

        .. tab:: Powershell

            .. code-tab:: Powershell

                curl.exe -X GET "https://satchecker.cps.iau.org/tools/omms-at-epoch/?epoch=2460500.5&page=1&per_page=10" -H "accept: application/json"

    **Example Response**

    .. sourcecode:: json

        [
            {
                "data": [
                    {
                        "satellite_name": "ISS (ZARYA)",
                        "satellite_id": 25544,
                        "orbital_elements": {
                            "OBJECT_NAME": "ISS (ZARYA)",
                            "OBJECT_ID": "1998-067A",
                            "EPOCH": "2024-07-14T12:00:00.000000",
                            "MEAN_MOTION": 15.50218234,
                            "ECCENTRICITY": 0.0002983,
                            "INCLINATION": 51.6372,
                            "RA_OF_ASC_NODE": 120.4521,
                            "ARG_OF_PERICENTER": 88.1234,
                            "MEAN_ANOMALY": 271.9876,
                            "EPHEMERIS_TYPE": 0,
                            "CLASSIFICATION_TYPE": "U",
                            "NORAD_CAT_ID": 25544,
                            "ELEMENT_SET_NO": 999,
                            "REV_AT_EPOCH": 46200,
                            "BSTAR": 0.00021456,
                            "MEAN_MOTION_DOT": 0.00018342,
                            "MEAN_MOTION_DDOT": 0.0
                        },
                        "epoch": "2024-07-14 12:00:00 UTC",
                        "date_collected": "2024-07-14 18:04:11 UTC",
                        "data_source": "spacetrack"
                    }
                ],
                "page": 1,
                "per_page": 10,
                "source": "IAU CPS SatChecker",
                "total_results": 385,
                "version": "1.X.x"
            }
        ]

Get nearest OMM
~~~~~~~~~~~~~~~~

This endpoint fetches the OMM closest to a specific epoch date. It supports searching
by either name or NORAD ID, but due to inconsistencies in satellite naming, it is recommended
to use the NORAD ID.

**Endpoint**

.. http:get:: /tools/get-nearest-omm/

    **Parameters**

    :query id: (*required*) -- The identifier of the satellite (name or NORAD ID).
    :query id_type: (*required*) -- The type of identifier: valid values are "name" or "catalog".
    :query epoch: (*required*) -- The epoch date for the OMM data, in Julian Date format.

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-nearest-omm/?id=25544&id_type=catalog&epoch=2460500

        .. tab:: Python

            .. code-tab:: Python

                import requests
                import json

                url = 'https://satchecker.cps.iau.org/tools/get-nearest-omm/'
                params = {'id': '25544',
                          'id_type': 'catalog',
                          'epoch': '2460500'
                        }

                r = requests.get(url, params=params)
                print(json.dumps(r.json(), indent=4))

        .. tab:: Bash

            .. code-tab:: Bash

                curl -X GET "https://satchecker.cps.iau.org/tools/get-nearest-omm/?id=25544&id_type=catalog&epoch=2460500" -H "accept: application/json"

        .. tab:: Powershell

            .. code-tab:: Powershell

                curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-nearest-omm/?id=25544&id_type=catalog&epoch=2460500" -H "accept: application/json"

    **Example Response**

    .. sourcecode:: json

        [
            {
                "source": "IAU CPS SatChecker",
                "orbital_data": [
                    {
                        "satellite_name": "ISS (ZARYA)",
                        "satellite_id": 25544,
                        "orbital_elements": {
                            "OBJECT_NAME": "ISS (ZARYA)",
                            "OBJECT_ID": "1998-067A",
                            "EPOCH": "2024-07-14T12:00:00.000000",
                            "MEAN_MOTION": 15.50218234,
                            "ECCENTRICITY": 0.0002983,
                            "INCLINATION": 51.6372,
                            "RA_OF_ASC_NODE": 120.4521,
                            "ARG_OF_PERICENTER": 88.1234,
                            "MEAN_ANOMALY": 271.9876,
                            "EPHEMERIS_TYPE": 0,
                            "CLASSIFICATION_TYPE": "U",
                            "NORAD_CAT_ID": 25544,
                            "ELEMENT_SET_NO": 999,
                            "REV_AT_EPOCH": 46200,
                            "BSTAR": 0.00021456,
                            "MEAN_MOTION_DOT": 0.00018342,
                            "MEAN_MOTION_DDOT": 0.0
                        },
                        "epoch": "2024-07-14 12:00:00 UTC",
                        "date_collected": "2024-07-14 18:04:11 UTC",
                        "data_source": "spacetrack"
                    }
                ],
                "version": "1.X.x"
            }
        ]

Get adjacent OMMs
~~~~~~~~~~~~~~~~~~

This endpoint fetches the OMMs right before and after a specific epoch date. It currently only supports searching
by NORAD ID.

**Endpoint**

.. http:get:: /tools/get-adjacent-omms/

    **Parameters**

    :query id: (*required*) -- The identifier of the satellite  (NORAD ID).
    :query id_type: (*required*) -- The type of identifier: valid values are "catalog".
    :query epoch: (*required*) -- The epoch date for the OMM data, in Julian Date format.

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-adjacent-omms/?id=25544&id_type=catalog&epoch=2460500

        .. tab:: Python

            .. code-tab:: Python

                import requests
                import json

                url = 'https://satchecker.cps.iau.org/tools/get-adjacent-omms/'
                params = {'id': '25544',
                          'id_type': 'catalog',
                          'epoch': '2460500'
                        }

                r = requests.get(url, params=params)
                print(json.dumps(r.json(), indent=4))

        .. tab:: Bash

            .. code-tab:: Bash

                curl -X GET "https://satchecker.cps.iau.org/tools/get-adjacent-omms/?id=25544&id_type=catalog&epoch=2460500" -H "accept: application/json"

        .. tab:: Powershell

            .. code-tab:: Powershell

                curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-adjacent-omms/?id=25544&id_type=catalog&epoch=2460500" -H "accept: application/json"

    **Example Response**

    .. sourcecode:: json

        [
            {
                "source": "IAU CPS SatChecker",
                "orbital_data": [
                    {
                        "satellite_name": "ISS (ZARYA)",
                        "satellite_id": 25544,
                        "orbital_elements": {
                            "OBJECT_NAME": "ISS (ZARYA)",
                            "OBJECT_ID": "1998-067A",
                            "EPOCH": "2024-07-13T09:31:22.000000",
                            "MEAN_MOTION": 15.50201145,
                            "ECCENTRICITY": 0.0002951,
                            "INCLINATION": 51.6375,
                            "RA_OF_ASC_NODE": 126.7788,
                            "ARG_OF_PERICENTER": 90.4412,
                            "MEAN_ANOMALY": 269.7215,
                            "EPHEMERIS_TYPE": 0,
                            "CLASSIFICATION_TYPE": "U",
                            "NORAD_CAT_ID": 25544,
                            "ELEMENT_SET_NO": 999,
                            "REV_AT_EPOCH": 46184,
                            "BSTAR": 0.00021002,
                            "MEAN_MOTION_DOT": 0.00018011,
                            "MEAN_MOTION_DDOT": 0.0
                        },
                        "epoch": "2024-07-13 09:31:22 UTC",
                        "date_collected": "2024-07-13 15:02:47 UTC",
                        "data_source": "spacetrack"
                    },
                    {
                        "satellite_name": "ISS (ZARYA)",
                        "satellite_id": 25544,
                        "orbital_elements": {
                            "OBJECT_NAME": "ISS (ZARYA)",
                            "OBJECT_ID": "1998-067A",
                            "EPOCH": "2024-07-14T12:00:00.000000",
                            "MEAN_MOTION": 15.50218234,
                            "ECCENTRICITY": 0.0002983,
                            "INCLINATION": 51.6372,
                            "RA_OF_ASC_NODE": 120.4521,
                            "ARG_OF_PERICENTER": 88.1234,
                            "MEAN_ANOMALY": 271.9876,
                            "EPHEMERIS_TYPE": 0,
                            "CLASSIFICATION_TYPE": "U",
                            "NORAD_CAT_ID": 25544,
                            "ELEMENT_SET_NO": 999,
                            "REV_AT_EPOCH": 46200,
                            "BSTAR": 0.00021456,
                            "MEAN_MOTION_DOT": 0.00018342,
                            "MEAN_MOTION_DDOT": 0.0
                        },
                        "epoch": "2024-07-14 12:00:00 UTC",
                        "date_collected": "2024-07-14 18:04:11 UTC",
                        "data_source": "spacetrack"
                    }
                ],
                "version": "1.X.x"
            }
        ]

Get OMMs around a specific epoch date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This endpoint fetches a requested number of OMMs before and/or after a specific epoch date.
It currently only supports searching by NORAD ID.

**Endpoint**

.. http:get:: /tools/get-omms-around-epoch/

    **Parameters**

    :query id: (*required*) -- The identifier of the satellite  (NORAD ID).
    :query id_type: (*required*) -- The type of identifier: valid values are "catalog".
    :query epoch: (*required*) -- The epoch date for the OMM data, in Julian Date format.
    :query count_before: (*optional*) -- The number of OMMs before the specified epoch date. Defaults to 2.
    :query count_after: (*optional*) -- The number of OMMs after the specified epoch date. Defaults to 2.

    **Example Request**

    .. tabs::

        .. tab:: Browser

            https://satchecker.cps.iau.org/tools/get-omms-around-epoch/?id=25544&id_type=catalog&epoch=2460500&count_before=1&count_after=1

        .. tab:: Python

            .. code-tab:: Python

                import requests
                import json

                url = 'https://satchecker.cps.iau.org/tools/get-omms-around-epoch/'
                params = {'id': '25544',
                          'id_type': 'catalog',
                          'epoch': '2460500',
                          'count_before': '1',
                          'count_after': '1'
                        }

                r = requests.get(url, params=params)
                print(json.dumps(r.json(), indent=4))

        .. tab:: Bash

            .. code-tab:: Bash

                curl -X GET "https://satchecker.cps.iau.org/tools/get-omms-around-epoch/?id=25544&id_type=catalog&epoch=2460500&count_before=1&count_after=1" -H "accept: application/json"

        .. tab:: Powershell

            .. code-tab:: Powershell

                curl.exe -X GET "https://satchecker.cps.iau.org/tools/get-omms-around-epoch/?id=25544&id_type=catalog&epoch=2460500&count_before=1&count_after=1" -H "accept: application/json"

    **Example Response**

    The response has the same structure as :http:get:`/tools/get-adjacent-omms/`, with the
    number of records before and after the epoch controlled by ``count_before`` and
    ``count_after``.
