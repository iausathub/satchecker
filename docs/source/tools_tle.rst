TLE Data Access
================



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

Get nearest TLE
---------------------------------------------------------------

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
                "tle_data": [
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
---------------------------------------------------------------

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
                "tle_data": [
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
---------------------------------------------------------------

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
                "tle_data": [
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
