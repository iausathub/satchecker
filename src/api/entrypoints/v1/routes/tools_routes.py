# ruff: noqa: E501
import io
from datetime import datetime, timezone

from flask import current_app as app
from flask import jsonify, request, send_file

from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.entrypoints.extensions import db, limiter
from api.services.tools_service import (
    get_active_satellites,
    get_adjacent_tle_results,
    get_all_tles_at_epoch_formatted,
    get_ids_for_satellite_name,
    get_names_for_satellite_id,
    get_nearest_tle_result,
    get_satellite_data,
    get_starlink_generations,
    get_tle_data,
    get_tles_around_epoch_results,
)
from api.services.validation_service import validate_parameters

from . import api_main, api_source, api_v1, api_version


@api_v1.route("/tools/norad-ids-from-name/")
@api_main.route("/tools/norad-ids-from-name/")
@limiter.limit("100 per second, 2000 per minute")
def get_norad_ids_from_name():
    """Get NORAD ID(s) for a given satellite name.
    ---
    tags:
      - Tools
    summary: Find NORAD IDs by satellite name
    description: Returns the NORAD ID(s) for a given satellite name
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: The name of the satellite (full or partial)
        example: "ISS"
    responses:
      200:
        description: A list of NORAD IDs and their associated dates
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  satellite_id:
                    type: integer
                    example: 25544
                  start_date:
                    type: string
                    format: date-time
                    example: "1998-11-20T06:40:00Z"
                  end_date:
                    type: string
                    format: date-time
                    nullable: true
                    example: null
                  source:
                    type: string
                  version:
                    type: string
      400:
        description: Bad request due to missing or invalid parameters
      500:
        description: Internal server error
    """
    parameters = validate_parameters(request, ["name"], ["name"])

    session = db.session
    sat_repo = SqlAlchemySatelliteRepository(session)

    try:
        norad_ids_and_dates = get_ids_for_satellite_name(
            sat_repo, parameters["name"], api_source, api_version
        )
        if not norad_ids_and_dates:
            return jsonify([]), 200

        return jsonify(norad_ids_and_dates)
    except Exception as e:
        app.logger.error(f"Error getting NORAD IDs from name: {str(e)}")
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "message": "An error occurred while retrieving NORAD IDs",
                    "status_code": 500,
                }
            ),
            500,
        )


@api_v1.route("/tools/names-from-norad-id/")
@api_main.route("/tools/names-from-norad-id/")
@limiter.limit("100 per second, 2000 per minute")
def get_names_from_norad_id():
    """Get satellite name(s) for a given NORAD ID.
    ---
    tags:
      - Tools
    summary: Find satellite names by NORAD ID
    description: Returns the historical and current names for a given satellite NORAD ID
    parameters:
      - name: id
        in: query
        type: integer
        required: true
        description: The NORAD ID (catalog number) of the satellite
        example: 25544
    responses:
      200:
        description: A list of satellite names and their associated dates
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  satellite_name:
                    type: string
                    example: "INTERNATIONAL SPACE STATION"
                  start_date:
                    type: string
                    format: date-time
                    example: "1998-11-20T06:40:00Z"
                  end_date:
                    type: string
                    format: date-time
                    nullable: true
                    example: null
                  source:
                    type: string
                  version:
                    type: string
      400:
        description: Bad request due to missing or invalid parameters
      500:
        description: Internal server error
    """
    parameters = validate_parameters(request, ["id"], ["id"])

    session = db.session
    sat_repo = SqlAlchemySatelliteRepository(session)

    try:
        satellite_names_and_dates = get_names_for_satellite_id(
            sat_repo, parameters["id"], api_source, api_version
        )
        if not satellite_names_and_dates:
            return jsonify([]), 200

        return jsonify(satellite_names_and_dates)
    except Exception as e:
        app.logger.error(f"Error getting names from NORAD ID: {str(e)}")
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "message": "An error occurred while retrieving satellite names",
                    "status_code": 500,
                }
            ),
            500,
        )


@api_v1.route("/tools/get-starlink-generations/")
@api_main.route("/tools/get-starlink-generations/")
@limiter.limit("100 per second, 2000 per minute")
def get_starlink_generations_list():
    """Get a list of all Starlink satellite generations.
    ---
    tags:
      - Tools
    summary: Get a list of all generations of Starlink satellites in the database
    description: Returns a list of all generations of Starlink satellites in the database,
                including their earliest and latest launch dates.
    responses:
      200:
        description: A list of all generations of Starlink satellites in the database
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: Number of Starlink generations found
                  example: 2
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      generation:
                        type: string
                        description: The generation identifier
                        example: "gen1"
                      earliest_launch_date:
                        type: string
                        description: The earliest launch date for this generation
                        example: "2019-05-10 00:00:00 UTC"
                      latest_launch_date:
                        type: string
                        description: The latest launch date for this generation
                        example: "2019-05-20 00:00:00 UTC"
                source:
                  type: string
                  description: The API source identifier
                  example: "api"
                version:
                  type: string
                  description: The API version identifier
                  example: "1.0"
    """
    session = db.session
    sat_repo = SqlAlchemySatelliteRepository(session)

    try:
        starlink_generations = get_starlink_generations(
            sat_repo, api_source, api_version
        )
        if not starlink_generations:
            return jsonify([]), 200

        return jsonify(starlink_generations)
    except Exception as e:
        app.logger.error(f"Error getting Starlink generations: {str(e)}")
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "message": "An error occurred while retrieving Starlink generations",
                    "status_code": 500,
                }
            ),
            500,
        )


@api_v1.route("/tools/get-tle-data/")
@api_main.route("/tools/get-tle-data/")
@limiter.limit("100 per second, 2000 per minute")
def get_tles():
    """Get Two-Line Element set (TLE) data for a satellite.
    ---
    tags:
      - Tools
    summary: Get TLE data for a satellite
    description: Fetches Two-Line Element set (TLE) data for a given satellite within an optional date range
    parameters:
      - name: id
        in: query
        type: string
        required: true
        description: The ID of the satellite (NORAD ID or name)
        example: "25544"
      - name: id_type
        in: query
        type: string
        required: true
        description: The type of ID provided
        enum: ["catalog", "name"]
        example: "catalog"
      - name: start_date_jd
        in: query
        type: number
        format: float
        required: false
        description: Start date of the date range in Julian Date format
        example: 2459000.5
      - name: end_date_jd
        in: query
        type: number
        format: float
        required: false
        description: End date of the date range in Julian Date format
        example: 2459100.5
    responses:
      200:
        description: TLE data for the specified satellite
        content:
          application/json:
            schema:
              type: object
              properties:
                tles:
                  type: array
                  items:
                    type: object
                    properties:
                      satellite_name:
                        type: string
                        example: "ISS (ZARYA)"
                      satellite_id:
                        type: integer
                        example: 25544
                      tle_line1:
                        type: string
                        example: "1 25544U 98067A   22273.60868672  .00009356  00000+0  17303-3 0  9993"
                      tle_line2:
                        type: string
                        example: "2 25544  51.6432 335.0388 0003454 276.8059 212.5635 15.50267821360921"
                      epoch:
                        type: number
                        format: float
                        example: 2459851.10868672
                      date_collected:
                        type: string
                        format: date-time
                        example: "2022-09-30T14:36:31Z"
                      data_source:
                        type: string
                        example: "celestrak"
                source:
                  type: string
                version:
                  type: string
      400:
        description: Bad request due to missing or invalid parameters
      404:
        description: No TLE data found
      500:
        description: Internal server error
    """
    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)

    parameter_list = ["id", "id_type", "start_date_jd", "end_date_jd"]
    required_parameters = ["id", "id_type"]
    parameters = validate_parameters(request, parameter_list, required_parameters)

    tle_data = get_tle_data(
        tle_repo,
        parameters["id"],
        parameters["id_type"],
        parameters["start_date_jd"],
        parameters["end_date_jd"],
        api_source,
        api_version,
    )

    return jsonify(tle_data)


@api_v1.route("/tools/get-satellite-data/")
@api_main.route("/tools/get-satellite-data/")
@limiter.limit("100 per second, 2000 per minute")
def get_satellite_data_list():
    """Get detailed satellite metadata.
    ---
    tags:
      - Tools
    summary: Get satellite metadata
    description: Fetches detailed information about a satellite including launch data, status, and classification
    parameters:
      - name: id
        in: query
        type: string
        required: true
        description: The ID of the satellite (NORAD ID or name)
        example: "25544"
      - name: id_type
        in: query
        type: string
        required: true
        description: The type of ID provided, "catalog" for NORAD ID or "name" for satellite name
        enum: ["catalog", "name"]
        example: "catalog"
    responses:
      200:
        description: Satellite metadata
        content:
          application/json:
            schema:
              type: object
              properties:
                satellite_id:
                  type: integer
                  example: 25544
                satellite_name:
                  type: string
                  example: "ISS (ZARYA)"
                international_designator:
                  type: string
                  example: "1998-067A"
                object_type:
                  type: string
                  example: "PAYLOAD"
                launch_date:
                  type: string
                  format: date
                  example: "1998-11-20"
                decay_date:
                  type: string
                  format: date
                  nullable: true
                  example: null
                rcs_size:
                  type: string
                  example: "LARGE"
      400:
        description: Bad request due to missing or invalid parameters
      404:
        description: Satellite not found
      500:
        description: Internal server error
    """
    session = db.session
    sat_repo = SqlAlchemySatelliteRepository(session)

    parameter_list = ["id", "id_type"]
    required_parameters = ["id", "id_type"]
    parameters = validate_parameters(request, parameter_list, required_parameters)

    satellite_data = get_satellite_data(
        sat_repo,
        parameters["id"],
        parameters["id_type"],
        api_source,
        api_version,
    )

    return jsonify(satellite_data)


@api_v1.route("/tools/get-active-satellites/")
@api_main.route("/tools/get-active-satellites/")
@limiter.limit("100 per second, 2000 per minute")
def get_active_satellites_list():
    """Get a list of all active satellites.
    ---
    tags:
      - Tools
    summary: List all active satellites
    description: Returns a list of all active satellites (launched and not decayed)
    parameters:
      - name: object_type
        in: query
        type: string
        required: false
        description: Filter results by object type - either "PAYLOAD", "DEBRIS", "ROCKET BODY", "TBA", or "UNKNOWN"
        enum: ["PAYLOAD", "ROCKET BODY", "DEBRIS", "UNKNOWN", "TBA"]
        example: "PAYLOAD"
    responses:
      200:
        description: A list of active satellites
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of satellites returned
                data:
                  type: array
                  description: List of active satellites
                  items:
                    type: object
                    properties:
                      satellite_name:
                        type: string
                        example: "ISS (ZARYA)"
                      satellite_id:
                        type: integer
                        example: 25544
                      object_type:
                        type: string
                        example: "PAYLOAD"
                      launch_date:
                        type: string
                        format: date
                        example: "1998-11-20"
                      decay_date:
                        type: string
                        format: date
                        nullable: true
                        example: null
                      international_designator:
                        type: string
                        example: "1998-067A"
                      rcs_size:
                        type: string
                        example: "LARGE"
                source:
                  type: string
                  description: The source of the data
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to invalid parameters
      500:
        description: Internal server error
    """
    session = db.session
    sat_repo = SqlAlchemySatelliteRepository(session)

    parameter_list = ["object_type"]
    parameters = validate_parameters(request, parameter_list, [])

    active_satellites = get_active_satellites(
        sat_repo, parameters.get("object_type"), api_source, api_version
    )

    return jsonify(active_satellites)


@api_v1.route("/tools/tles-at-epoch/")
@api_main.route("/tools/tles-at-epoch/")
@limiter.limit("100 per second, 2000 per minute")
def get_tles_at_epoch():
    """Get all TLEs at a specific epoch date.
    ---
    tags:
      - Tools
    summary: Get TLEs at a specific epoch
    description: Fetches all TLEs at a specific epoch date with pagination support
    parameters:
      - name: epoch
        in: query
        type: string
        required: false
        description: The epoch date in Julian Date format (defaults to current time if not provided)
        example: "2459000.5"
      - name: page
        in: query
        type: integer
        required: false
        description: The page number for pagination (starts at 1)
        example: 1
      - name: per_page
        in: query
        type: integer
        required: false
        description: Number of results per page (defaults to 100)
        example: 100
      - name: format
        in: query
        type: string
        required: false
        description: Output format for TLE data; zip contains a CSV file
        enum: ["json", "txt", "zip"]
        example: "json"
    responses:
      200:
        description: TLEs matching the specified epoch
        content:
          application/json:
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: The number of TLEs returned
                data:
                  type: array
                  description: List of TLEs
                  items:
                    type: object
                    properties:
                      satellite_name:
                        type: string
                      satellite_id:
                        type: integer
                      tle_line1:
                        type: string
                      tle_line2:
                        type: string
                      epoch:
                        type: number
                        format: float
                      date_collected:
                        type: string
                        format: date-time
                      data_source:
                        type: string
                page:
                  type: integer
                per_page:
                  type: integer
                total_results:
                  type: integer
                source:
                  type: string
                version:
                  type: string
          text/plain:
            schema:
              type: string
              description: TLEs in standard text format (when format=txt)
          application/zip:
            schema:
              type: string
              format: binary
              description: Zipped TLE data (when format=zip)
      400:
        description: Bad request due to invalid parameters
      500:
        description: Internal server error
    """
    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)

    parameter_list = ["epoch", "page", "per_page", "format"]
    parameters = validate_parameters(request, parameter_list, [])

    epoch_date = parameters.get("epoch")
    if not epoch_date:
        epoch_date = datetime.now(timezone.utc)

    # paginated results by default
    format = parameters.get("format")
    if not format:
        format = "json"

    page = int(parameters.get("page", 1) or 1)
    per_page = int(parameters.get("per_page") or 100)

    result = get_all_tles_at_epoch_formatted(
        tle_repo,
        epoch_date,
        format=format,
        page=page,
        per_page=per_page,
        api_source=api_source,
        api_version=api_version,
    )

    if format == "txt" and isinstance(result, io.BytesIO):
        return send_file(result, mimetype="text/plain", as_attachment=False)
    elif format == "zip" and isinstance(result, io.BytesIO):
        return send_file(
            result,
            mimetype="application/zip",
            as_attachment=True,
            download_name="tle_data.zip",
        )
    else:
        return jsonify(result)


@api_v1.route("/tools/get-nearest-tle/")
@api_main.route("/tools/get-nearest-tle/")
@limiter.limit("100 per second, 2000 per minute")
def get_nearest_tle():
    """Get the TLE closest to a specific epoch.
    ---
    tags:
      - Tools
    summary: Get nearest TLE to epoch
    description: Fetches the TLE closest in time to the given epoch for a specific satellite
    parameters:
      - name: id
        in: query
        type: string
        required: true
        description: The ID of the satellite (NORAD ID or name)
        example: "25544"
      - name: id_type
        in: query
        type: string
        required: true
        description: The type of ID provided, "catalog" for NORAD ID or "name" for satellite name
        enum: ["catalog", "name"]
        example: "catalog"
      - name: epoch
        in: query
        type: number
        format: float
        required: true
        description: The Julian Date to find the nearest TLE for
        example: 2459000.5
    responses:
      200:
        description: The TLE closest to the specified epoch
        content:
          application/json:
            schema:
              type: object
              properties:
                tle_data:
                  type: array
                  description: The TLE data closest to the specified epoch
                  items:
                    type: object
                    properties:
                      satellite_name:
                        type: string
                        example: "ISS (ZARYA)"
                      satellite_id:
                        type: integer
                        example: 25544
                      tle_line1:
                        type: string
                        example: "1 25544U 98067A   22273.60868672  .00009356  00000+0  17303-3 0  9993"
                      tle_line2:
                        type: string
                        example: "2 25544  51.6432 335.0388 0003454 276.8059 212.5635 15.50267821360921"
                      epoch:
                        type: string
                        description: Epoch date of the TLE
                        example: "2024-01-30 02:26:07 UTC"
                      date_collected:
                        type: string
                        format: date-time
                        description: Date when the TLE was collected
                        example: "2024-06-04 19:16:53 UTC"
                      data_source:
                        type: string
                        description: Source of the TLE data
                        example: "spacetrack"
                source:
                  type: string
                  description: API source
                  example: "IAU CPS SatChecker"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to missing or invalid parameters
      404:
        description: No matching TLE found
      500:
        description: Internal server error
    """
    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)
    parameter_list = ["id", "id_type", "epoch"]
    required_parameters = ["id", "id_type", "epoch"]
    parameters = validate_parameters(request, parameter_list, required_parameters)

    tle_data = get_nearest_tle_result(
        tle_repo,
        parameters["id"],
        parameters["id_type"],
        parameters["epoch"],
        api_source,
        api_version,
    )
    return jsonify(tle_data)


@api_v1.route("/tools/get-adjacent-tles/")
@api_main.route("/tools/get-adjacent-tles/")
@limiter.limit("100 per second, 2000 per minute")
def get_adjacent_tles():
    """Get TLEs immediately before and after a specific epoch.
    ---
    tags:
      - Tools
    summary: Get adjacent TLEs around epoch
    description: Fetches the TLEs immediately before and after the given epoch for a specific satellite
    parameters:
      - name: id
        in: query
        type: string
        required: true
        description: The ID of the satellite (NORAD ID or name)
        example: "25544"
      - name: id_type
        in: query
        type: string
        required: true
        description: The type of ID provided, "catalog" for NORAD ID or "name" for satellite name
        enum: ["catalog", "name"]
        example: "catalog"
      - name: epoch
        in: query
        type: number
        format: float
        required: true
        description: The Julian Date to bracket with TLEs
        example: 2459000.5
    responses:
      200:
        description: TLEs immediately before and after the specified epoch
        content:
          application/json:
            schema:
              type: object
              properties:
                source:
                  type: string
                  description: API source
                  example: "IAU CPS SatChecker"
                tle_data:
                  type: array
                  description: Array containing the TLEs before and after the specified epoch
                  items:
                    type: object
                    properties:
                      satellite_name:
                        type: string
                        example: "ISS (ZARYA)"
                      satellite_id:
                        type: integer
                        example: 25544
                      tle_line1:
                        type: string
                        example: "1 25544U 98067A   22273.60868672  .00009356  00000+0  17303-3 0  9993"
                      tle_line2:
                        type: string
                        example: "2 25544  51.6432 335.0388 0003454 276.8059 212.5635 15.50267821360921"
                      epoch:
                        type: string
                        description: Epoch date of the TLE
                        example: "2019-06-30 20:27:51 UTC"
                      date_collected:
                        type: string
                        format: date-time
                        description: Date when the TLE was collected
                        example: "2024-06-04 19:16:53 UTC"
                      data_source:
                        type: string
                        description: Source of the TLE data
                        example: "spacetrack"
                version:
                  type: string
                  description: The version of the API
                  example: "1.X.x"
      400:
        description: Bad request due to missing or invalid parameters
      404:
        description: No adjacent TLEs found
      500:
        description: Internal server error
    """
    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)
    parameter_list = ["id", "id_type", "epoch"]
    required_parameters = ["id", "id_type", "epoch"]
    parameters = validate_parameters(request, parameter_list, required_parameters)

    tle_data = get_adjacent_tle_results(
        tle_repo,
        parameters["id"],
        parameters["id_type"],
        parameters["epoch"],
        api_source,
        api_version,
    )
    return jsonify(tle_data)


@api_v1.route("/tools/get-tles-around-epoch/")
@api_main.route("/tools/get-tles-around-epoch/")
@limiter.limit("100 per second, 2000 per minute")
def get_tles_around_epoch():
    """Get multiple TLEs before and after a specific epoch.
    ---
    tags:
      - Tools
    summary: Get multiple TLEs around epoch
    description: Fetches a specified number of TLEs before and after a given epoch for a specific satellite
    parameters:
      - name: id
        in: query
        type: string
        required: true
        description: The ID of the satellite (NORAD ID or name)
        example: "25544"
      - name: id_type
        in: query
        type: string
        required: true
        description: The type of ID provided, "catalog" for NORAD ID or "name" for satellite name
        enum: ["catalog", "name"]
        example: "catalog"
      - name: epoch
        in: query
        type: number
        format: float
        required: true
        description: The Julian Date to center the TLE search around
        example: 2459000.5
      - name: count_before
        in: query
        type: integer
        required: false
        description: Number of TLEs to fetch before the epoch (default is 2)
        example: 2
      - name: count_after
        in: query
        type: integer
        required: false
        description: Number of TLEs to fetch after the epoch (default is 2)
        example: 2
    responses:
      200:
        description: TLEs before and after the specified epoch
        content:
          application/json:
            schema:
              type: object
              properties:
                tles:
                  type: array
                  items:
                    type: object
                    properties:
                      satellite_name:
                        type: string
                      satellite_id:
                        type: integer
                      tle_line1:
                        type: string
                      tle_line2:
                        type: string
                      epoch:
                        type: number
                        format: float
                      date_collected:
                        type: string
                        format: date-time
                      data_source:
                        type: string
                source:
                  type: string
                version:
                  type: string
      400:
        description: Bad request due to missing or invalid parameters
      404:
        description: No TLEs found around the specified epoch
      500:
        description: Internal server error
    """
    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)
    parameter_list = ["id", "id_type", "epoch", "count_before", "count_after"]
    required_parameters = ["id", "id_type", "epoch"]
    parameters = validate_parameters(request, parameter_list, required_parameters)

    tle_data = get_tles_around_epoch_results(
        tle_repo,
        parameters["id"],
        parameters["id_type"],
        parameters["epoch"],
        parameters.get("count_before", 2),
        parameters.get("count_after", 2),
        api_source,
        api_version,
    )
    return jsonify(tle_data)
