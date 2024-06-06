API Response Details
=====================

The API response is a JSON object with the following fields:

.. list-table::
   :header-rows: 1

   * - Field Name
     - Description
   * - ALTITUDE-DEG
     - Satellite position altitude in degrees at the given time and location
   * - AZIMUTH-DEG
     - Satellite position azimuth in degrees at the given time and location
   * - CATALOG_ID
     - NORAD ID of the satellite
   * - DATA_SOURCE
     - Source for the TLE data used to generate this satellite position (either Celestrak or Space-Track
   * - DDEC-DEG_PER_SEC
     - Change in declination in degrees per second
   * - DECLINATION-DEG
     - Position (declination) of the satellite in degrees at the given time and location
   * - DRA_COSDEC-DEG_PER_SEC
     - Change in right ascension in degrees per second
   * - ILLUMINATED
     - Whether the satellite is illuminated at the given time and location
   * - JULIAN_DATE
     - The date/time corresponding to the given position prediction
   * - NAME
     - Name of the satellite (either specified by the user, or the one associated with the given NORAD ID and TLE data)
   * - OBSERVER_GCRS-KM
     - Position vector for the observer (Geocentric Celestial Reference System (GCRS))
   * - PHASE_ANGLE-DEG
     - The angle between the satellite, the observer, and the sun in degrees
   * - RANGE-KM
     - Distance to the satellite in kilometers
   * - RANGE_RATE-KM_PER_SEC
     - Velocity of the satellite in kilometers per second
   * - RIGHT_ASCENSION-DEG
     - Position (right ascension) of the satellite in degrees at the given time and location
   * - SATELLITE_GCRS-KM
     - Position vector for the satellite (Geocentric Celestial Reference System (GCRS))
   * - TLE_DATE
     - Epoch date of the TLE used to calculate the satellite position (UTC timezone)



Example Response
------------------

.. sourcecode:: json

    [
        {
        "ALTITUDE-DEG": -9.80971257652,
        "AZIMUTH-DEG": 55.15478730961,
        "CATALOG_ID": 46161,
        "DATA_SOURCE": "spacetrack",
        "DDEC-DEG_PER_SEC": -0.05070574412,
        "DECLINATION-DEG": 18.61796683006,
        "DRA_COSDEC-DEG_PER_SEC": 0.01019243518,
        "ILLUMINATED": true,
        "JULIAN_DATE": 2460000.1,
        "NAME": "STARLINK-1600",
        "OBSERVER_GCRS-KM": [
        1000.044906440929,
        -4783.283201527772,
        4085.459180326725
        ],
        "PHASE_ANGLE-DEG": 109.24612785799,
        "RANGE-KM": 4095.040926172063,
        "RANGE_RATE-KM_PER_SEC": 6.284422469172,
        "RIGHT_ASCENSION-DEG": 43.04367601256,
        "SATELLITE_GCRS-KM": [
        2836.175695292651,
        2648.8215197690492,
        1307.3684135941762
        ],
        "TLE_DATE": "2024-02-05 16:12:42 UTC"
        }
    ]
