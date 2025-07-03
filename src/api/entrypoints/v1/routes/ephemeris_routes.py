# ruff: noqa: E501
from flask import abort, request

from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.common.exceptions import DataError
from api.entrypoints.extensions import db, limiter
from api.services.ephemeris_service import (
    generate_ephemeris_data,
    generate_ephemeris_data_user,
)
from api.services.validation_service import validate_parameters

from . import api_main, api_source, api_v1, api_version


@api_v1.route("/ephemeris/name/")
@api_main.route("/ephemeris/name/")
@limiter.limit("100 per second, 2000 per minute")
def get_ephemeris_by_name():
    """Get ephemeris data for a satellite by name.
    ---
    tags:
      - Ephemeris
    summary: Get ephemeris data by satellite name
    description: Returns satellite location and velocity information for a given satellite name at a specified Julian Date. For the most accurate results, a Julian Date close to the TLE epoch is necessary.
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: Name of the satellite
        example: "ISS"
      - name: latitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's latitude in decimal degrees (required if site not provided)
        example: 48.8566
      - name: longitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's longitude in decimal degrees (required if site not provided)
        example: 2.3522
      - name: elevation
        in: query
        type: number
        format: float
        required: false
        description: Observer's elevation in meters (required if site not provided)
        example: 35.0
      - name: site
        in: query
        type: string
        required: false
        description: Predefined site name/alias from AstroPy list (https://www.astropy.org/astropy-data/coordinates/sites.json), can be used instead of latitude/longitude/elevation
        example: "rubin"
      - name: julian_date
        in: query
        type: number
        format: float
        required: true
        description: UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
        example: 2459000.5
      - name: min_altitude
        in: query
        type: number
        format: float
        required: false
        description: Minimum satellite altitude in degrees (default is 0)
        example: 10.0
      - name: max_altitude
        in: query
        type: number
        format: float
        required: false
        description: Maximum satellite altitude in degrees (default is 90)
        example: 90.0
      - name: data_source
        in: query
        type: string
        required: false
        description: Original source of TLE data (default is whichever has the closest TLE epoch)
        enum: ["celestrak", "spacetrack"]
        example: "celestrak"
    responses:
      200:
        description: Satellite position and velocity data
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of satellite positions returned
                data:
                  type: array
                  description: A list of lists, where each inner list contains the data for a single satellite position
                  items:
                    type: array
                    items:
                      oneOf:
                        - type: string
                        - type: number
                        - type: boolean
                        - type: array
                          items:
                            type: number
                fields:
                  type: array
                  description: A list of field names corresponding to the data in each inner list
                  items:
                    type: string
                    enum: [
                      "name", "catalog_id", "julian_date", "satellite_gcrs_km",
                      "right_ascension_deg", "declination_deg", "tle_date",
                      "dra_cosdec_deg_per_sec", "ddec_deg_per_sec", "altitude_deg",
                      "azimuth_deg", "range_km", "range_rate_km_per_sec",
                      "phase_angle_deg", "illuminated", "data_source",
                      "observer_gcrs_km", "international_designator", "tle_epoch"
                    ]
                source:
                  type: string
                  description: The source of the satellite position data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to missing or invalid parameters
      404:
        description: Satellite not found
      500:
        description: Internal server error
    """
    session = db.session
    satellite_repository = SqlAlchemySatelliteRepository(session)
    tle_repository = SqlAlchemyTLERepository(session)

    parameter_list = [
        "name",
        "latitude",
        "longitude",
        "elevation",
        "site",
        "julian_date",
        "min_altitude",
        "max_altitude",
        "data_source",
    ]

    if "site" not in request.args:
        required_parameters = [
            "name",
            "latitude",
            "longitude",
            "elevation",
            "julian_date",
        ]
    else:
        required_parameters = ["name", "site", "julian_date"]

    parameters = validate_parameters(
        request,
        parameter_list,
        required_parameters,
    )

    try:
        position_data = generate_ephemeris_data(
            satellite_repository,
            tle_repository,
            parameters["name"],
            "name",
            parameters["location"],
            parameters["julian_dates"],
            parameters["min_altitude"],
            parameters["max_altitude"],
            api_source,
            api_version,
            parameters["data_source"],
        )
    except DataError as e:
        abort(e.status_code, e.message)

    session.close()

    return position_data


@api_v1.route("/ephemeris/name-jdstep/")
@api_main.route("/ephemeris/name-jdstep/")
@limiter.limit("100 per second, 2000 per minute")
def get_ephemeris_by_name_jdstep():
    """Get ephemeris data for a satellite by name over a time range.
    ---
    tags:
      - Ephemeris
    summary: Get ephemeris data by satellite name over a time range
    description: Returns satellite location and velocity information for a given satellite name over a specified time range. For the most accurate results, a time range close to the TLE epoch is necessary.
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: Name of the satellite
        example: "ISS"
      - name: latitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's latitude in decimal degrees (required if site not provided)
        example: 48.8566
      - name: longitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's longitude in decimal degrees (required if site not provided)
        example: 2.3522
      - name: elevation
        in: query
        type: number
        format: float
        required: false
        description: Observer's elevation in meters (required if site not provided)
        example: 35.0
      - name: site
        in: query
        type: string
        required: false
        description: Predefined site name/alias from AstroPy list (https://www.astropy.org/astropy-data/coordinates/sites.json), can be used instead of latitude/longitude/elevation
        example: "rubin"
      - name: startjd
        in: query
        type: number
        format: float
        required: true
        description: Start time of the ephemeris calculation in Julian date
        example: 2459000.5
      - name: stopjd
        in: query
        type: number
        format: float
        required: true
        description: End time of the ephemeris calculation in Julian date
        example: 2459001.0
      - name: stepjd
        in: query
        type: number
        format: float
        required: false
        description: UT1 time step in Julian Days for ephemeris generation. Default is .05 (1.2 hours).
        example: 0.01
      - name: min_altitude
        in: query
        type: number
        format: float
        required: false
        description: Minimum satellite altitude in degrees (default is 0)
        example: 10.0
      - name: max_altitude
        in: query
        type: number
        format: float
        required: false
        description: Maximum satellite altitude in degrees (default is 90)
        example: 90.0
      - name: data_source
        in: query
        type: string
        required: false
        description: Original source of TLE data (default is whichever has the closest TLE epoch)
        enum: ["celestrak", "spacetrack"]
        example: "celestrak"
    responses:
      200:
        description: Satellite position and velocity data over time
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of satellite positions returned
                data:
                  type: array
                  description: A list of lists, where each inner list contains the data for a single satellite position
                  items:
                    type: array
                    items:
                      oneOf:
                        - type: string
                        - type: number
                        - type: boolean
                        - type: array
                          items:
                            type: number
                fields:
                  type: array
                  description: A list of field names corresponding to the data in each inner list
                  items:
                    type: string
                    enum: [
                      "name", "catalog_id", "julian_date", "satellite_gcrs_km",
                      "right_ascension_deg", "declination_deg", "tle_date",
                      "dra_cosdec_deg_per_sec", "ddec_deg_per_sec", "altitude_deg",
                      "azimuth_deg", "range_km", "range_rate_km_per_sec",
                      "phase_angle_deg", "illuminated", "data_source",
                      "observer_gcrs_km", "international_designator", "tle_epoch"
                    ]
                source:
                  type: string
                  description: The source of the satellite position data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to missing or invalid parameters
      404:
        description: Satellite not found
      500:
        description: Internal server error
    """
    session = db.session
    satellite_repository = SqlAlchemySatelliteRepository(session)
    tle_repository = SqlAlchemyTLERepository(session)

    parameter_list = [
        "name",
        "latitude",
        "longitude",
        "elevation",
        "site",
        "startjd",
        "stopjd",
        "stepjd",
        "min_altitude",
        "max_altitude",
        "data_source",
    ]

    if "site" not in request.args:
        required_parameters = [
            "name",
            "latitude",
            "longitude",
            "elevation",
            "startjd",
            "stopjd",
        ]
    else:
        required_parameters = ["name", "site", "startjd", "stopjd"]

    parameters = validate_parameters(
        request,
        parameter_list,
        required_parameters,
    )

    try:
        position_data = generate_ephemeris_data(
            satellite_repository,
            tle_repository,
            parameters["name"],
            "name",
            parameters["location"],
            parameters["julian_dates"],
            parameters["min_altitude"],
            parameters["max_altitude"],
            api_source,
            api_version,
            parameters["data_source"],
        )
    except DataError as e:
        abort(e.status_code, e.message)
    session.close()

    return position_data


@api_v1.route("/ephemeris/catalog-number/")
@api_main.route("/ephemeris/catalog-number/")
@limiter.limit("100 per second, 2000 per minute")
def get_ephemeris_by_catalog_number():
    """Get ephemeris data for a satellite by NORAD ID.
    ---
    tags:
      - Ephemeris
    summary: Get ephemeris data by NORAD ID
    description: Returns satellite location and velocity information for a given NORAD ID at a specified Julian Date. For the most accurate results, a Julian Date close to the TLE epoch is necessary.
    parameters:
      - name: catalog
        in: query
        type: string
        required: true
        description: NORAD Catalog Number (ID) of the satellite
        example: "25544"
      - name: latitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's latitude in decimal degrees (required if site not provided)
        example: 48.8566
      - name: longitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's longitude in decimal degrees (required if site not provided)
        example: 2.3522
      - name: elevation
        in: query
        type: number
        format: float
        required: false
        description: Observer's elevation in meters (required if site not provided)
        example: 35.0
      - name: site
        in: query
        type: string
        required: false
        description: Predefined site name/alias from AstroPy list (https://www.astropy.org/astropy-data/coordinates/sites.json), can be used instead of latitude/longitude/elevation
        example: "rubin"
      - name: julian_date
        in: query
        type: number
        format: float
        required: true
        description: UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
        example: 2459000.5
      - name: min_altitude
        in: query
        type: number
        format: float
        required: false
        description: Minimum satellite altitude in degrees (default is 0)
        example: 10.0
      - name: max_altitude
        in: query
        type: number
        format: float
        required: false
        description: Maximum satellite altitude in degrees (default is 90)
        example: 90.0
      - name: data_source
        in: query
        type: string
        required: false
        description: Original source of TLE data (default is whichever has the closest TLE epoch)
        enum: ["celestrak", "spacetrack"]
        example: "celestrak"
    responses:
      200:
        description: Satellite position and velocity data
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of satellite positions returned
                data:
                  type: array
                  description: A list of lists, where each inner list contains the data for a single satellite position
                  items:
                    type: array
                    items:
                      oneOf:
                        - type: string
                        - type: number
                        - type: boolean
                        - type: array
                          items:
                            type: number
                fields:
                  type: array
                  description: A list of field names corresponding to the data in each inner list
                  items:
                    type: string
                    enum: [
                      "name", "catalog_id", "julian_date", "satellite_gcrs_km",
                      "right_ascension_deg", "declination_deg", "tle_date",
                      "dra_cosdec_deg_per_sec", "ddec_deg_per_sec", "altitude_deg",
                      "azimuth_deg", "range_km", "range_rate_km_per_sec",
                      "phase_angle_deg", "illuminated", "data_source",
                      "observer_gcrs_km", "international_designator", "tle_epoch"
                    ]
                source:
                  type: string
                  description: The source of the satellite position data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to missing or invalid parameters
      404:
        description: Satellite not found
      500:
        description: Internal server error
    """
    session = db.session
    satellite_repository = SqlAlchemySatelliteRepository(session)
    tle_repository = SqlAlchemyTLERepository(session)

    parameter_list = [
        "catalog",
        "latitude",
        "longitude",
        "elevation",
        "site",
        "julian_date",
        "min_altitude",
        "max_altitude",
        "data_source",
    ]

    if "site" not in request.args:
        required_parameters = [
            "catalog",
            "latitude",
            "longitude",
            "elevation",
            "julian_date",
        ]
    else:
        required_parameters = ["catalog", "site", "julian_date"]

    parameters = validate_parameters(
        request,
        parameter_list,
        required_parameters,
    )

    position_data = generate_ephemeris_data(
        satellite_repository,
        tle_repository,
        parameters["catalog"],
        "catalog_number",
        parameters["location"],
        parameters["julian_dates"],
        parameters["min_altitude"],
        parameters["max_altitude"],
        api_source,
        api_version,
        parameters["data_source"],
    )
    session.close()

    return position_data


@api_v1.route("/ephemeris/catalog-number-jdstep/")
@api_main.route("/ephemeris/catalog-number-jdstep/")
@limiter.limit("100 per second, 2000 per minute")
def get_ephemeris_by_catalog_number_jdstep():
    """Get ephemeris data for a satellite by NORAD ID over a time range.
    ---
    tags:
      - Ephemeris
    summary: Get ephemeris data by NORAD ID over a time range
    description: Returns satellite location and velocity information for a given NORAD ID over a specified time range. For the most accurate results, a time range close to the TLE epoch is necessary.
    parameters:
      - name: catalog
        in: query
        type: string
        required: true
        description: NORAD Catalog Number (ID) of the satellite
        example: "25544"
      - name: latitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's latitude in decimal degrees (required if site not provided)
        example: 48.8566
      - name: longitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's longitude in decimal degrees (required if site not provided)
        example: 2.3522
      - name: elevation
        in: query
        type: number
        format: float
        required: false
        description: Observer's elevation in meters (required if site not provided)
        example: 35.0
      - name: site
        in: query
        type: string
        required: false
        description: Predefined site name/alias from AstroPy list (https://www.astropy.org/astropy-data/coordinates/sites.json), can be used instead of latitude/longitude/elevation
        example: "rubin"
      - name: startjd
        in: query
        type: number
        format: float
        required: true
        description: Start time of the ephemeris calculation in Julian date
        example: 2459000.5
      - name: stopjd
        in: query
        type: number
        format: float
        required: true
        description: End time of the ephemeris calculation in Julian date
        example: 2459001.0
      - name: stepjd
        in: query
        type: number
        format: float
        required: false
        description: UT1 time step in Julian Days for ephemeris generation. Default is .05 (1.2 hours).
        example: 0.01
      - name: min_altitude
        in: query
        type: number
        format: float
        required: false
        description: Minimum satellite altitude in degrees (default is 0)
        example: 10.0
      - name: max_altitude
        in: query
        type: number
        format: float
        required: false
        description: Maximum satellite altitude in degrees (default is 90)
        example: 90.0
      - name: data_source
        in: query
        type: string
        required: false
        description: Original source of TLE data (default is whichever has the closest TLE epoch)
        enum: ["celestrak", "spacetrack"]
        example: "celestrak"
    responses:
      200:
        description: Satellite position and velocity data over time
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of satellite positions returned
                data:
                  type: array
                  description: A list of lists, where each inner list contains the data for a single satellite position
                  items:
                    type: array
                    items:
                      oneOf:
                        - type: string
                        - type: number
                        - type: boolean
                        - type: array
                          items:
                            type: number
                fields:
                  type: array
                  description: A list of field names corresponding to the data in each inner list
                  items:
                    type: string
                    enum: [
                      "name", "catalog_id", "julian_date", "satellite_gcrs_km",
                      "right_ascension_deg", "declination_deg", "tle_date",
                      "dra_cosdec_deg_per_sec", "ddec_deg_per_sec", "altitude_deg",
                      "azimuth_deg", "range_km", "range_rate_km_per_sec",
                      "phase_angle_deg", "illuminated", "data_source",
                      "observer_gcrs_km", "international_designator", "tle_epoch"
                    ]
                source:
                  type: string
                  description: The source of the satellite position data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to missing or invalid parameters
      404:
        description: Satellite not found
      500:
        description: Internal server error
    """
    session = db.session
    satellite_repository = SqlAlchemySatelliteRepository(session)
    tle_repository = SqlAlchemyTLERepository(session)

    parameter_list = [
        "catalog",
        "latitude",
        "longitude",
        "elevation",
        "site",
        "startjd",
        "stopjd",
        "stepjd",
        "min_altitude",
        "max_altitude",
        "data_source",
    ]

    if "site" not in request.args:
        required_parameters = [
            "catalog",
            "latitude",
            "longitude",
            "elevation",
            "startjd",
            "stopjd",
        ]
    else:
        required_parameters = ["catalog", "site", "startjd", "stopjd"]

    parameters = validate_parameters(
        request,
        parameter_list,
        required_parameters,
    )

    try:
        position_data = generate_ephemeris_data(
            satellite_repository,
            tle_repository,
            parameters["catalog"],
            "catalog_number",
            parameters["location"],
            parameters["julian_dates"],
            parameters["min_altitude"],
            parameters["max_altitude"],
            api_source,
            api_version,
            parameters["data_source"],
        )
    except DataError as e:
        abort(e.status_code, e.message)
    session.close()

    return position_data


@api_v1.route("/ephemeris/tle/")
@api_main.route("/ephemeris/tle/")
@limiter.limit("100 per second, 2000 per minute")
def get_ephemeris_by_tle():
    """Get ephemeris data for a custom TLE.
    ---
    tags:
      - Ephemeris
    summary: Get ephemeris data from a custom TLE
    description: Returns satellite location and velocity information for a custom Two-Line Element set at a specified Julian Date. For the most accurate results, a Julian Date close to the TLE epoch is necessary.
    parameters:
      - name: tle
        in: query
        type: string
        required: true
        description: Two-line element set (full TLE) of the satellite
        example: "1 25544U 98067A   22273.60868672  .00009356  00000+0  17303-3 0  9993\n2 25544  51.6432 335.0388 0003454 276.8059 212.5635 15.50267821360921"
      - name: latitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's latitude in decimal degrees (required if site not provided)
        example: 48.8566
      - name: longitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's longitude in decimal degrees (required if site not provided)
        example: 2.3522
      - name: elevation
        in: query
        type: number
        format: float
        required: false
        description: Observer's elevation in meters (required if site not provided)
        example: 35.0
      - name: site
        in: query
        type: string
        required: false
        description: Predefined site name/alias from AstroPy list (https://www.astropy.org/astropy-data/coordinates/sites.json) , can be used instead of latitude/longitude/elevation
        example: "rubin"
      - name: julian_date
        in: query
        type: number
        format: float
        required: true
        description: UT1 Universal Time Julian Date (use 0 to use the TLE epoch)
        example: 2459000.5
      - name: min_altitude
        in: query
        type: number
        format: float
        required: false
        description: Minimum satellite altitude in degrees (default is 0)
        example: 10.0
      - name: max_altitude
        in: query
        type: number
        format: float
        required: false
        description: Maximum satellite altitude in degrees (default is 90)
        example: 90.0
    responses:
      200:
        description: Satellite position and velocity data
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of satellite positions returned
                data:
                  type: array
                  description: A list of lists, where each inner list contains the data for a single satellite position
                  items:
                    type: array
                    items:
                      oneOf:
                        - type: string
                        - type: number
                        - type: boolean
                        - type: array
                          items:
                            type: number
                fields:
                  type: array
                  description: A list of field names corresponding to the data in each inner list
                  items:
                    type: string
                    enum: [
                      "name", "catalog_id", "julian_date", "satellite_gcrs_km",
                      "right_ascension_deg", "declination_deg", "tle_date",
                      "dra_cosdec_deg_per_sec", "ddec_deg_per_sec", "altitude_deg",
                      "azimuth_deg", "range_km", "range_rate_km_per_sec",
                      "phase_angle_deg", "illuminated", "data_source",
                      "observer_gcrs_km", "international_designator", "tle_epoch"
                    ]
                source:
                  type: string
                  description: The source of the satellite position data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to missing, invalid parameters or invalid TLE format
      500:
        description: Internal server error
    """
    session = db.session
    parameter_list = [
        "tle",
        "latitude",
        "longitude",
        "elevation",
        "site",
        "julian_date",
        "min_altitude",
        "max_altitude",
    ]

    if "site" not in request.args:
        required_parameters = [
            "tle",
            "latitude",
            "longitude",
            "elevation",
            "julian_date",
        ]
    else:
        required_parameters = ["tle", "site", "julian_date"]

    parameters = validate_parameters(
        request,
        parameter_list,
        required_parameters,
    )

    position_data = generate_ephemeris_data_user(
        parameters["tle"],
        parameters["location"],
        parameters["julian_dates"],
        parameters["min_altitude"],
        parameters["max_altitude"],
        api_source,
        api_version,
    )
    session.close()

    return position_data


@api_v1.route("/ephemeris/tle-jdstep/")
@api_main.route("/ephemeris/tle-jdstep/")
@limiter.limit("100 per second, 2000 per minute")
def get_ephemeris_by_tle_jdstep():
    """Get ephemeris data for a custom TLE over a time range.
    ---
    tags:
      - Ephemeris
    summary: Get ephemeris data from a custom TLE over a time range
    description: Returns satellite location and velocity information for a custom Two-Line Element set over a specified time range. For the most accurate results, a time range close to the TLE epoch is necessary.
    parameters:
      - name: tle
        in: query
        type: string
        required: true
        description: Two-line element set (full TLE) of the satellite
        example: "1 25544U 98067A   22273.60868672  .00009356  00000+0  17303-3 0  9993\n2 25544  51.6432 335.0388 0003454 276.8059 212.5635 15.50267821360921"
      - name: latitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's latitude in decimal degrees (required if site not provided)
        example: 48.8566
      - name: longitude
        in: query
        type: number
        format: float
        required: false
        description: Observer's longitude in decimal degrees (required if site not provided)
        example: 2.3522
      - name: elevation
        in: query
        type: number
        format: float
        required: false
        description: Observer's elevation in meters (required if site not provided)
        example: 35.0
      - name: site
        in: query
        type: string
        required: false
        description: Predefined site name/alias from AstroPy list (https://www.astropy.org/astropy-data/coordinates/sites.json), can be used instead of latitude/longitude/elevation
        example: "rubin"
      - name: startjd
        in: query
        type: number
        format: float
        required: true
        description: Start time of the ephemeris calculation in Julian date
        example: 2459000.5
      - name: stopjd
        in: query
        type: number
        format: float
        required: true
        description: End time of the ephemeris calculation in Julian date
        example: 2459001.0
      - name: stepjd
        in: query
        type: number
        format: float
        required: false
        description: UT1 time step in Julian Days for ephemeris generation. Default is .05 (1.2 hours).
        example: 0.01
      - name: min_altitude
        in: query
        type: number
        format: float
        required: false
        description: Minimum satellite altitude in degrees (default is 0)
        example: 10.0
      - name: max_altitude
        in: query
        type: number
        format: float
        required: false
        description: Maximum satellite altitude in degrees (default is 90)
        example: 90.0
    responses:
      200:
        description: Satellite position and velocity data over time
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of satellite positions returned
                data:
                  type: array
                  description: A list of lists, where each inner list contains the data for a single satellite position
                  items:
                    type: array
                    items:
                      oneOf:
                        - type: string
                        - type: number
                        - type: boolean
                        - type: array
                          items:
                            type: number
                fields:
                  type: array
                  description: A list of field names corresponding to the data in each inner list
                  items:
                    type: string
                    enum: [
                      "name", "catalog_id", "julian_date", "satellite_gcrs_km",
                      "right_ascension_deg", "declination_deg", "tle_date",
                      "dra_cosdec_deg_per_sec", "ddec_deg_per_sec", "altitude_deg",
                      "azimuth_deg", "range_km", "range_rate_km_per_sec",
                      "phase_angle_deg", "illuminated", "data_source",
                      "observer_gcrs_km", "international_designator", "tle_epoch"
                    ]
                source:
                  type: string
                  description: The source of the satellite position data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to missing, invalid parameters or invalid TLE format
      500:
        description: Internal server error
    """
    session = db.session
    parameter_list = [
        "tle",
        "latitude",
        "longitude",
        "elevation",
        "site",
        "startjd",
        "stopjd",
        "stepjd",
        "min_altitude",
        "max_altitude",
    ]

    if "site" not in request.args:
        required_parameters = [
            "tle",
            "latitude",
            "longitude",
            "elevation",
            "startjd",
            "stopjd",
        ]
    else:
        required_parameters = ["tle", "site", "startjd", "stopjd"]

    parameters = validate_parameters(
        request,
        parameter_list,
        required_parameters,
    )

    position_data = generate_ephemeris_data_user(
        parameters["tle"],
        parameters["location"],
        parameters["julian_dates"],
        parameters["min_altitude"],
        parameters["max_altitude"],
        api_source,
        api_version,
    )
    session.close()

    return position_data
