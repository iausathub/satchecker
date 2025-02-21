from datetime import datetime, timezone

from flask import abort, jsonify, request, send_file
from flask import current_app as app

from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.common.exceptions import ValidationError
from api.entrypoints.extensions import db, limiter
from api.services.tools_service import (
    get_active_satellites,
    get_adjacent_tle_results,
    get_all_tles_at_epoch_formatted,
    get_ids_for_satellite_name,
    get_names_for_satellite_id,
    get_nearest_tle_result,
    get_satellite_data,
    get_tle_data,
    get_tles_around_epoch_results,
)
from api.services.validation_service import validate_parameters

from . import api_main, api_source, api_v1, api_version


@api_v1.route("/tools/norad-ids-from-name/")
@api_main.route("/tools/norad-ids-from-name/")
@limiter.limit("100 per second, 2000 per minute")
def get_norad_ids_from_name():
    """
    Returns the NORAD ID(s) for a given satellite name.

    Args
    ----------
    name: str
        The name of the satellite.

    Returns
    -------
    response: list
        A list of NORAD IDs associated with the given satellite name.
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
        app.logger.error(e)
        return None


@api_v1.route("/tools/names-from-norad-id/")
@api_main.route("/tools/names-from-norad-id/")
@limiter.limit("100 per second, 2000 per minute")
def get_names_from_norad_id():
    """
    Returns the name(s) for a given NORAD id.

    Args
    ----------
    id: int
        The NORAD id of the satellite.

    Returns
    -------
    response: list
        A list of names associated with the given satellite NORAD id.
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
        app.logger.error(e)
        return None


@api_v1.route("/tools/get-tle-data/")
@api_main.route("/tools/get-tle-data/")
@limiter.limit("100 per second, 2000 per minute")
def get_tles():
    """
    Fetches Two-Line Element set (TLE) data for a given satellite.

    The function retrieves TLE data based on the satellite ID and ID type
    provided in the request arguments. It also allows for a date range to be
    specified for the TLE data.

    Parameters:
        id (str):
            The ID of the satellite.
        id_type (str):
            The type of the ID, either 'catalog' or 'name'.
        start_date_jd (str, optional):
            The start date of the date range for the TLE data,
            in Julian Date format.
        end_date_jd (str, optional):
            The end date of the date range for the TLE data,
            in Julian Date format.

    Returns:
        A JSON response containing the TLE data for the specified satellite
        and date range. Each TLE data entry includes the satellite name,
        satellite ID, TLE lines, epoch, date collected, and data source.

    Raises:
        400:
            If the satellite ID is not provided or the ID type is not
            'catalog' or 'name'.
        500:
            If there is a DataError when fetching the TLE data.
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
    """
    Returns a list of all active satellites in the database.
    A satellite is considered active if it has been launched and has not decayed.

    Parameters:
        object_type (str, optional):
            Filter results by object type (e.g., 'PAYLOAD', 'ROCKET BODY', 'DEBRIS').
            If not provided, returns all active satellites.

    Returns:
        response: JSON
            A list of active satellites, containing:
            - satellite_name: Name of the satellite
            - satellite_id: NORAD Catalog Number
            - object_type: Type of space object
            - launch_date: Date the object was launched
            - decay_date: (will be null since all objects here are still active)
            - international_designator: International Designator (COSPAR ID)
            - rcs_size: Radar Cross Section Size
            - source: API name
            - version: API version
    """
    session = db.session
    sat_repo = SqlAlchemySatelliteRepository(session)

    parameter_list = ["object_type"]
    try:
        parameters = validate_parameters(request, parameter_list, [])
    except ValidationError as e:
        abort(e.status_code, e.message)

    active_satellites = get_active_satellites(
        sat_repo, parameters.get("object_type"), api_source, api_version
    )

    return jsonify(active_satellites)


@api_v1.route("/tools/tles-at-epoch/")
@api_main.route("/tools/tles-at-epoch/")
@limiter.limit("100 per second, 2000 per minute")
def get_tles_at_epoch():
    """
    Fetches all TLEs at a specific epoch date.

    The function retrieves TLE data based on the epoch date provided in the request
    arguments. It also supports pagination to handle large result sets.

    Parameters:
        epoch (str):
            The epoch date for the TLE data, in Julian Date format.
        page (int, optional):
            The page number for pagination.
        per_page (int, optional):
            The number of results per page for pagination.

    Returns:
        A JSON response containing the TLE data for the specified epoch date.
        Each TLE data entry includes the satellite name, satellite ID, TLE lines,
        epoch, date collected, and data source.

    Raises:
        400:
            If the epoch date is not provided or is invalid.
        500:
            If there is a DataError when fetching the TLE data.
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

    tles = get_all_tles_at_epoch_formatted(
        tle_repo,
        epoch_date,
        format=format,
        page=page,
        per_page=per_page,
        api_source=api_source,
        api_version=api_version,
    )

    if format == "txt":
        return send_file(tles, mimetype="text/plain", as_attachment=False)
    elif format == "zip":
        return send_file(
            tles,
            mimetype="application/zip",
            as_attachment=True,
            download_name="tle_data.zip",
        )
    else:
        return jsonify(tles)


@api_v1.route("/tools/get-nearest-tle/")
@api_main.route("/tools/get-nearest-tle/")
@limiter.limit("100 per second, 2000 per minute")
def get_nearest_tle():
    """
    Fetches the TLE closest to the given epoch.

    Parameters:
        id (str): The ID of the satellite.
        id_type (str): The type of the ID, either 'catalog' or 'name'.
        epoch (float): The Julian Date to find the nearest TLE for.
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
    """
    Fetches the TLEs immediately before and after the given epoch.

    Parameters:
        id (str): The ID of the satellite.
        id_type (str): The type of the ID, either 'catalog' or 'name'.
        epoch_jd (float): The Julian Date to bracket.
    """
    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)
    parameter_list = ["id", "id_type", "epoch_jd"]
    required_parameters = ["id", "id_type", "epoch_jd"]
    parameters = validate_parameters(request, parameter_list, required_parameters)

    tle_data = get_adjacent_tle_results(
        tle_repo,
        parameters["id"],
        parameters["id_type"],
        parameters["epoch_jd"],
        api_source,
        api_version,
    )
    return jsonify(tle_data)


@api_v1.route("/tools/get-tle-data-around-epoch/")
@api_main.route("/tools/get-tle-data-around-epoch/")
@limiter.limit("100 per second, 2000 per minute")
def get_tles_around_epoch():
    """
    Fetches a specified number of TLEs before and after a given epoch.

    Parameters:
        id (str): The ID of the satellite.
        id_type (str): The type of the ID, either 'catalog' or 'name'.
        epoch_jd (float): The Julian Date to center the TLE search around.
        count_before (int, optional): Number of TLEs to fetch before the epoch.
        Default: 2
        count_after (int, optional): Number of TLEs to fetch after the epoch.
        Default: 2
    """
    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)
    parameter_list = ["id", "id_type", "epoch_jd", "count_before", "count_after"]
    required_parameters = ["id", "id_type", "epoch_jd"]
    parameters = validate_parameters(request, parameter_list, required_parameters)

    tle_data = get_tles_around_epoch_results(
        tle_repo,
        parameters["id"],
        parameters["id_type"],
        parameters["epoch_jd"],
        parameters.get("count_before", 2),
        parameters.get("count_after", 2),
        api_source,
        api_version,
    )
    return jsonify(tle_data)
