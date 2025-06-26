# ruff: noqa: E501
from flask import abort, jsonify, request
from flask import current_app as app

from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.common.exceptions import ValidationError
from api.entrypoints.extensions import db, limiter
from api.services.fov_service import (
    get_satellite_passes_in_fov,
    get_satellites_above_horizon,
    # get_satellites_above_horizon_range,
)
from api.services.validation_service import validate_parameters

from . import api_main, api_source, api_v1, api_version


@api_v1.route("/fov/satellite-passes/")
@api_main.route("/fov/satellite-passes/")
@limiter.limit("50 per second, 1000 per minute")
def get_satellite_passes():
    """Get satellites that pass through a specified field of view.
    ---
    tags:
      - Field of View
    summary: Get satellite passes in a field of view
    description: Get satellites that pass through a specified field of view during an observation period
    parameters:
      - name: latitude
        in: query
        type: number
        format: float
        required: false
        description: Latitude of observation site in decimal degrees (required if site not provided)
        example: 48.8566
      - name: longitude
        in: query
        type: number
        format: float
        required: false
        description: Longitude of observation site in decimal degrees (required if site not provided)
        example: 2.3522
      - name: elevation
        in: query
        type: number
        format: float
        required: false
        description: Elevation of observation site in meters (required if site not provided)
        example: 35.0
      - name: site
        in: query
        type: string
        required: false
        description: Predefined site name/alias from AstroPy list (https://www.astropy.org/astropy-data/coordinates/sites.json), can be used instead of latitude/longitude/elevation
        example: "rubin"
      - name: duration
        in: query
        type: number
        format: float
        required: true
        description: Duration of observation in seconds
        example: 60.0
      - name: ra
        in: query
        type: number
        format: float
        required: true
        description: Right ascension of field center in decimal degrees
        example: 15.0
      - name: dec
        in: query
        type: number
        format: float
        required: true
        description: Declination of field center in decimal degrees
        example: 30.0
      - name: fov_radius
        in: query
        type: number
        format: float
        required: true
        description: Radius of field of view in decimal degrees
        example: 0.5
      - name: start_time_jd
        in: query
        type: number
        format: float
        required: false
        description: Start time of observation in Julian date (either this or mid_obs_time_jd must be provided)
        example: 2459000.5
      - name: mid_obs_time_jd
        in: query
        type: number
        format: float
        required: false
        description: Mid-observation time in Julian date (either this or start_time_jd must be provided)
        example: 2459000.5
      - name: group_by
        in: query
        type: string
        required: false
        description: Group results by 'satellite' or 'time' (default is 'time' for chronological order)
        enum: [satellite, time]
        example: satellite
      - name: include_tles
        in: query
        type: boolean
        required: false
        description: Whether to include TLE data used to calculate the passes in the response
        example: true
      - name: skip_cache
        in: query
        type: boolean
        required: false
        description: Whether to skip the cache and calculate the passes from scratch
        example: false
      - name: constellation
        in: query
        type: string
        required: false
        description: Constellation of the satellites to include in the response
        example: "starlink"
      - name: data_source
        in: query
        type: string
        required: false
        description: Data source to use for TLEs ("celestrak" or "spacetrack"). Default is any/all sources.
        example: "celestrak"
    responses:
      200:
        description: Successful response with satellite passes
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    satellites:
                      type: object
                      additionalProperties:
                        type: object
                        properties:
                          name:
                            type: string
                            description: Name of the satellite
                          norad_id:
                            type: integer
                            description: NORAD catalog ID of the satellite
                          positions:
                            type: array
                            items:
                              type: object
                              properties:
                                altitude:
                                  type: number
                                  format: float
                                  description: Altitude above horizon in degrees
                                angle:
                                  type: number
                                  format: float
                                  description: Angular distance from FOV center in degrees
                                azimuth:
                                  type: number
                                  format: float
                                  description: Azimuth angle in degrees
                                date_time:
                                  type: string
                                  description: UTC time in YYYY-MM-DD HH:MM:SS TZ format
                                dec:
                                  type: number
                                  format: float
                                  description: Declination in degrees
                                julian_date:
                                  type: number
                                  format: float
                                  description: Julian date for this position
                                ra:
                                  type: number
                                  format: float
                                  description: Right ascension in degrees
                                tle_epoch:
                                  type: string
                                  description: Epoch date of the TLE used for calculation
                                tle_data:
                                  type: object
                                  description: TLE data for this satellite (only included when include_tles=true)
                                  properties:
                                    tle_line1:
                                      type: string
                                      description: First line of the TLE
                                    tle_line2:
                                      type: string
                                      description: Second line of the TLE
                                    source:
                                      type: string
                                      description: Source of the TLE data (celestrak or spacetrack)
                    total_position_results:
                      type: integer
                      description: Total number of position results
                    total_satellites:
                      type: integer
                      description: Total number of satellites found
                source:
                  type: string
                  description: The source of the satellite position data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to incorrect parameters
      500:
        description: Internal server error
    """
    parameters = [
        "latitude",
        "longitude",
        "elevation",
        "site",
        "duration",
        "ra",
        "dec",
        "fov_radius",
        "start_time_jd",
        "mid_obs_time_jd",
        "group_by",
        "include_tles",
        "skip_cache",
        "constellation",
        "data_source",
    ]

    if "site" not in request.args:
        required_parameters = [
            "latitude",
            "longitude",
            "elevation",
            "duration",
            "ra",
            "dec",
            "fov_radius",
        ]
    else:
        required_parameters = ["site", "duration", "ra", "dec", "fov_radius"]

    try:
        validated_parameters = validate_parameters(
            request, parameters, required_parameters
        )
    except ValidationError as e:
        abort(e.status_code, e.message)

    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)

    try:
        satellite_passes = get_satellite_passes_in_fov(
            tle_repo,
            validated_parameters["location"],
            validated_parameters["mid_obs_time_jd"],
            validated_parameters["start_time_jd"],
            validated_parameters["duration"],
            validated_parameters["ra"],
            validated_parameters["dec"],
            validated_parameters["fov_radius"],
            validated_parameters["group_by"],
            validated_parameters["include_tles"],
            validated_parameters["skip_cache"],
            validated_parameters["constellation"],
            validated_parameters["data_source"],
            api_source,
            api_version,
        )
        if not satellite_passes:
            return {
                "info": "No position information found with this criteria",
                "api_source": api_source,
                "version": api_version,
            }

        return jsonify(satellite_passes)
    except ValueError as e:
        app.logger.error(e)
        return jsonify({"error": "Incorrect parameters"}), 400
    except Exception as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500


@api_v1.route("/fov/satellites-above-horizon/")
@api_main.route("/fov/satellites-above-horizon/")
@limiter.limit("50 per second, 1000 per minute")
def get_all_satellites_above_horizon():
    """Get satellites above horizon at a specific time.
    ---
    tags:
      - Field of View
    summary: Get satellites above horizon at a specific time
    description: Get a list of satellites that are above the horizon at a specific Julian date for a given location
    parameters:
      - name: latitude
        in: query
        type: number
        format: float
        required: false
        description: Latitude of observation site in decimal degrees (required if site not provided)
        example: 48.8566
      - name: longitude
        in: query
        type: number
        format: float
        required: false
        description: Longitude of observation site in decimal degrees (required if site not provided)
        example: 2.3522
      - name: elevation
        in: query
        type: number
        format: float
        required: false
        description: Elevation of observation site in meters (required if site not provided)
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
        description: Time at which to check for satellites above horizon in Julian date format
        example: 2459000.5
      - name: min_altitude
        in: query
        type: number
        format: float
        required: false
        description: Minimum altitude above horizon in degrees (default is 0)
        example: 15.0
      - name: illuminated_only
        in: query
        type: boolean
        required: false
        description: Whether to include only illuminated satellites (default is false)
        example: true
      - name: min_range
        in: query
        type: number
        format: float
        required: false
        description: Minimum range of satellites in kilometers (default is 0.0)
        example: 300.0
      - name: max_range
        in: query
        type: number
        format: float
        required: false
        description: Maximum range of satellites in kilometers (default is infinity)
        example: 500.0
      - name: constellation
        in: query
        type: string
        required: false
        description: Constellation of the satellites to include in the response
        example: "starlink"
    responses:
      200:
        description: Successful response with satellites above horizon
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of satellites found above the horizon
                data:
                  type: array
                  description: List of satellites above the horizon
                  items:
                    type: object
                    properties:
                      name:
                        type: string
                        description: Name of the satellite
                      norad_id:
                        type: integer
                        description: NORAD catalog ID of the satellite
                      julian_date:
                        type: number
                        format: float
                        description: Julian date for the position
                      altitude:
                        type: number
                        format: float
                        description: Altitude above horizon in degrees
                      azimuth:
                        type: number
                        format: float
                        description: Azimuth angle in degrees
                      ra:
                        type: number
                        format: float
                        description: Right ascension in degrees
                      dec:
                        type: number
                        format: float
                        description: Declination in degrees
                      range:
                        type: number
                        format: float
                        description: Distance to the satellite in kilometers
                      tle_epoch:
                        type: string
                        description: Epoch date of the TLE used for calculation in YYYY-MM-DD HH:MM:SS TZ format
                source:
                  type: string
                  description: The source of the satellite position data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to incorrect parameters
      500:
        description: Internal server error
    """
    return _handle_satellites_above_horizon(with_duration=False)


@api_v1.route("/fov/satellites-above-horizon-range/")
@api_main.route("/fov/satellites-above-horizon-range/")
@limiter.limit("50 per second, 1000 per minute")
def get_all_satellites_above_horizon_range():
    """Get satellites above horizon over a time range.
    ---
    tags:
      - Field of View
    summary: Get satellites above horizon over a time range
    description: Get a list of satellites that are above the horizon during a specified time range for a given location
    parameters:
      - name: latitude
        in: query
        type: number
        format: float
        required: true
        description: Latitude of observation site in decimal degrees (required if site not provided)
        example: 48.8566
      - name: longitude
        in: query
        type: number
        format: float
        required: true
        description: Longitude of observation site in decimal degrees (required if site not provided)
        example: 2.3522
      - name: elevation
        in: query
        type: number
        format: float
        required: true
        description: Elevation of observation site in meters (required if site not provided)
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
        description: Start time of the observation period in Julian date
        example: 2459000.5
      - name: duration
        in: query
        type: number
        format: float
        required: true
        description: Duration of observation period in seconds
        example: 120.0
      - name: min_altitude
        in: query
        type: number
        format: float
        required: false
        description: Minimum altitude above horizon in degrees (default is 0)
        example: 15.0
      - name: illuminated_only
        in: query
        type: boolean
        required: false
        description: Whether to include only illuminated satellites (default is false)
        example: true
      - name: min_range
        in: query
        type: number
        format: float
        required: false
        description: Minimum range of satellites in kilometers (default is 0.0)
        example: 300.0
      - name: max_range
        in: query
        type: number
        format: float
        required: false
        description: Maximum range of satellites in kilometers (default is infinity)
        example: 500.0
    responses:
      200:
        description: Successful response with satellites above horizon during the specified period
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of satellites found above the horizon
                data:
                  type: array
                  description: List of satellites above the horizon
                  items:
                    type: object
                    properties:
                      tbd
                source:
                  type: string
                  description: The source of the satellite position data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to incorrect parameters
      500:
        description: Internal server error
    """
    return _handle_satellites_above_horizon(with_duration=True)


def _handle_satellites_above_horizon(with_duration=False):
    """Helper function to reduce code duplication between the similar endpoints."""
    # Base parameters for both endpoints
    parameters = [
        "latitude",
        "longitude",
        "elevation",
        "site",
        "julian_date",
        "min_altitude",
        "illuminated_only",
        "min_range",
        "max_range",
        "constellation",
    ]

    # Add duration parameter if needed
    if with_duration:
        parameters.append("duration")

    # Define required parameters based on presence of site and duration
    if "site" not in request.args:
        required_parameters = ["latitude", "longitude", "elevation", "julian_date"]
    else:
        required_parameters = ["site", "julian_date"]

    # Add duration to required parameters if needed
    if with_duration:
        required_parameters.append("duration")

    try:
        validated_parameters = validate_parameters(
            request, parameters, required_parameters
        )
    except ValidationError as e:
        abort(e.status_code, e.message)

    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)

    try:
        # Choose the appropriate service function based on whether duration is included
        if with_duration:
            """
            satellite_passes = get_satellites_above_horizon_range(
                tle_repo,
                validated_parameters["location"],
                validated_parameters["julian_dates"],
                validated_parameters["min_altitude"],
                validated_parameters["min_range"],
                validated_parameters["max_range"],
                validated_parameters["illuminated_only"],
                validated_parameters["duration"],
                api_source,
                api_version,
            )
            """
            pass
        else:
            satellite_passes = get_satellites_above_horizon(
                tle_repo,
                validated_parameters["location"],
                validated_parameters["julian_dates"],
                validated_parameters["min_altitude"],
                validated_parameters["min_range"],
                validated_parameters["max_range"],
                validated_parameters["illuminated_only"],
                validated_parameters["constellation"],
                api_source,
                api_version,
            )

        if not satellite_passes:
            return {
                "info": "No position information found with this criteria",
                "source": api_source,
                "version": api_version,
            }

        return jsonify(satellite_passes)
    except ValueError as e:
        app.logger.error(e)
        return jsonify({"error": "Incorrect parameters"}), 400
    except Exception as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500
