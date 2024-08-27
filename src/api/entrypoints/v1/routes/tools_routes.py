from flask import current_app as app
from flask import jsonify, request

from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.entrypoints.extensions import db, get_forwarded_address, limiter
from api.services.tools_service import (
    get_ids_for_satellite_name,
    get_names_for_satellite_id,
    get_tle_data,
)
from api.services.validation_service import validate_parameters

from . import api_main, api_source, api_v1, api_version


@api_v1.route("/tools/norad-ids-from-name/")
@api_main.route("/tools/norad-ids-from-name/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
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
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
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
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
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
