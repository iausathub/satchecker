API Response Details
=====================

The API response is a JSON object with the following fields:

.. list-table::
   :header-rows: 1

   * - Field Name
     - Description
   * - altitude_deg
     - Satellite position altitude in degrees at the given time and location
   * - azimuth_deg
     - Satellite position azimuth in degrees at the given time and location
   * - catalog_id
     - NORAD ID of the satellite
   * - data_source
     - Source for the TLE data used to generate this satellite position (either Celestrak or Space-Track
   * - ddec_deg_per_sec
     - Change in declination in degrees per second
   * - declination_deg
     - Position (declination) of the satellite in degrees at the given time and location
   * - dra_cosdec_deg_per_sec
     - Change in right ascension in degrees per second
   * - illuminated
     - Whether the satellite is illuminated at the given time and location
   * - julian_date
     - The time corresponding to the given position prediction, in Julian Date format, in the UTC time standard.
   * - name
     - Name of the satellite (either specified by the user, or the one associated with the given NORAD ID and TLE data)
   * - observer_gcrs_km
     - Position vector for the observer (Geocentric Celestial Reference System (GCRS), relative to Earth's center)
   * - phase_angle_deg
     - The angle between the satellite, the observer, and the sun in degrees
   * - range_km
     - Distance to the satellite in kilometers
   * - range_rate_km_per_sec
     - Velocity of the satellite in kilometers per second
   * - right_ascension_deg
     - Position (right ascension) of the satellite in degrees at the given time and location
   * - satellite_gcrs_km
     - Position vector for the satellite (Geocentric Celestial Reference System (GCRS), relative to Earth's center)
   * - tle_date
     - Date that the TLE used to calculate the satellite position was collected from the specified data source (UTC timezone)
   * - international_designator
     - International Designator for the satellite (COSPAR ID)
   * - tle_epoch
     - Date that the TLE used to calculate the satellite position was created/valid for (UTC timezone)


The API response is structured as follows:

- ``count``: The number of satellite positions returned
- ``data``: A list of lists, where each inner list contains the data for a single satellite position
- ``fields``: A list of field names corresponding to the data in each inner list
- ``source``: The source of the satellite position data (IAU CPS SatChecker)
- ``version``: The version of the API used to generate the response


Example Response
------------------

.. sourcecode:: json

    {
        "count": 2,
        "data": [
            [
                "STARLINK-1600",
                46161,
                2460000.1,
                [
                    3836.22060173358,
                    -2134.4616817587225,
                    5392.8275939209025
                ],
                43.04367601,
                18.61796683,
                "2024-02-06 00:12:42 UTC",
                0.01019244,
                -0.05070574,
                -9.80971258,
                55.15478731,
                4095.040926,
                6.284422480176,
                109.24612786,
                true,
                "spacetrack",
                [
                    1000.0449064409289,
                    -4783.283201527772,
                    4085.4591803267244
                ],
                "2020-057AW"
            ],
            [
                "STARLINK-1600",
                46161,
                2460000.2,
                [
                    -3690.0978606869476,
                    2311.525710926265,
                    -5439.347123444699
                ],
                142.61268228,
                -45.94348489,
                "2024-02-06 00:12:42 UTC",
                0.03354248,
                0.00663582,
                -83.13771687,
                208.61161584,
                13245.443279,
                -0.265606961557,
                56.98343683,
                true,
                "spacetrack",
                [
                    3628.0577317280786,
                    -3281.0604185873253,
                    4079.547075333211
                ],
                "2020-057AW",
                "2024-02-06 00:12:42 UTC"
            ]
        ],
        "fields": [
            "name",
            "catalog_id",
            "satellite_gcrs_km",
            "right_ascension_deg",
            "declination_deg",
            "tle_date",
            "dra_cosdec_deg_per_sec",
            "ddec_deg_per_sec",
            "altitude_deg",
            "azimuth_deg",
            "range_km",
            "range_rate_km_per_sec",
            "phase_angle_deg",
            "illuminated",
            "data_source",
            "observer_gcrs_km",
            "international_designator",
            "tle_epoch"
        ],
        "source": "IAU CPS SatChecker",
        "version": "1.1.0"
    }
