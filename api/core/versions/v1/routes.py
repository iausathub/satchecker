#!/usr/bin/python3
from datetime import timezone

import core.versions.v1.tasks as tasks
import requests
from astropy.time import Time
from core import error_messages
from core.database.satellite_access import (
    get_ids_for_satelltite_name,
    get_names_for_satellite_id,
    get_tles,
)
from core.database.tle_access import (
    get_tle,
    parse_tle,
)
from core.extensions import limiter
from core.utils import (
    extract_parameters,
    get_forwarded_address,
    jd_arange,
    validate_parameters,
)
from core.versions.v1 import api_main, api_v1
from flask import abort, jsonify, redirect, request
from flask import current_app as app
from sqlalchemy.exc import DataError


@api_main.app_errorhandler(404)
def page_not_found(error):
    """
    Handles page not found errors by returning the error message and a 404 status code.

    Args:
        e (HTTPException): The exception instance with details about the error.

    Returns:
        str: A string containing a custom error message.
        int: The HTTP status code for a page not found error (404).
    """
    return (
        "Error 404: Page not found<br /> \
        Check your spelling to ensure you are accessing the correct endpoint.",
        404,
    )


@api_main.app_errorhandler(400)
def missing_parameter(e):
    """
    Handles bad request errors by returning the error message and a 400 status code.

    Args:
        e (HTTPException): The exception instance with details about the error.

    Returns:
        str: A string containing a custom error message and the error's description.
        int: The HTTP status code for a bad request error (400).
    """
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    return (
        f"Error 400: Incorrect parameters or too many results to return \
        (maximum of 1000 in a single request)<br /> \
        Check your request and try again.<br /><br />{str(e)}",
        400,
    )


@api_main.app_errorhandler(429)
def ratelimit_handler(e):
    """
    Handles rate limit errors by returning the error message and a 429 status code.

    Args:
        e (HTTPException): The exception instance with details about the error.

    Returns:
        str: A string containing a custom error message and the error's description.
        int: The HTTP status code for a rate limit error (429).
    """
    return "Error 429: You have exceeded your rate limit:<br />" + e.description, 429


@api_main.app_errorhandler(500)
def internal_server_error(e):
    """
    Handles internal server errors by returning the error message and a 500 status code.

    Args:
        e (HTTPException): The exception instance with details about the error.

    Returns:
        str: A string containing a custom error message and the error's description.
        int: The HTTP status code for an internal server error (500).
    """
    return "Error 500: Internal server error:<br />" + e.description, 500


@api_v1.route("/")
@api_v1.route("/index")
@api_main.route("/")
@api_main.route("/index")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def root():
    """
    Redirect to API documentation
    """
    return redirect("https://satchecker.readthedocs.io/en/latest/")


@api_v1.route("/health")
@api_main.route("/health")
@limiter.exempt
def health():
    """
    Checks the health of the application by making a GET request to the IAU CPS URL.

    This function sends a GET request to the IAU CPS URL and checks the status of the
    response. If the request is successful, it returns a JSON response with a
    message indicating that the application is healthy. If the request fails for any
    reason, it aborts the request and returns a 503 status code with an error message.

    Returns:
        dict: A dictionary containing a message indicating the health of the
            application.
    Raises:
        HTTPException: An exception with a 503 status code and an error message if the
            GET request fails.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(
            "https://cps.iau.org/tools/satchecker/api/", headers=headers, timeout=10
        )
        response.raise_for_status()
    except Exception as e:
        abort(503, f"Error: Unable to connect to IAU CPS URL - {e}")
    else:
        return {"message": "Healthy"}


@api_v1.route("/fov_test/")
@api_main.route("/fov_test/")
def fov_test():
    # task = tasks.profile_function.apply()
    # return task.get()
    result_list_task = tasks.compare.apply()
    result_list = result_list_task.get()
    return result_list


@api_v1.route("/ephemeris/name/")
@api_main.route("/ephemeris/name/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_name():
    """
    Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's Two Line Element Data Set at a specified
    Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE
    epoch is necessary.**

    Parameters
    ----------
    name: str
        CelesTrak name of object
    latitude: float
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: float
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: float
        Elevation in meters
    julian_date: float
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    min_altitude: float
        Minimum satellite altitude in degrees
    max_altitude: float
        Maximum satellite altitude in degrees
    data_source: str
        Original source of TLE data (celestrak or spacetrack)

    Returns
    -------
    response: dict
        A dictionary containing satellite information. The format of the dictionary
        is defined by the json_output() function.
    """
    parameters = extract_parameters(
        request,
        [
            "name",
            "latitude",
            "longitude",
            "elevation",
            "julian_date",
            "min_altitude",
            "max_altitude",
            "data_source",
        ],
    )

    parameters = validate_parameters(
        parameters, ["name", "latitude", "longitude", "elevation", "julian_date"]
    )

    # Test JD format
    try:
        jd = Time(parameters["julian_date"], format="jd", scale="ut1")
    except Exception:
        abort(500, error_messages.INVALID_JD)

    tle = get_tle(
        parameters["name"], False, parameters["data_source"], jd.to_datetime()
    )

    result_list_task = tasks.create_result_list.apply(
        args=[
            parameters["location"],
            [jd],
            tle.tle_line1,
            tle.tle_line2,
            tle.date_collected,
            parameters["name"],
            parameters["min_altitude"],
            parameters["max_altitude"],
            tle.tle_satellite.sat_number,
            tle.data_source,
        ]
    )
    result_list = result_list_task.get()
    return result_list


@api_v1.route("/ephemeris/name-jdstep/")
@api_main.route("/ephemeris/name-jdstep/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_name_jdstep():
    """
    Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's name with the Two Line Element Data Set at
    a specified Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.**

    Parameters
    ----------
    name: str
        CelesTrak name of object
    latitude: float
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: float
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: float
        Elevation in meters
    startjd: float
        UT1 Universal Time Julian Date to start ephmeris calculation.
    stopjd: float
        UT1 Universal Time Julian Date to stop ephmeris calculation.
    stepjd: float
        UT1 Universal Time Julian Date timestep.
    min_altitude: float
        Minimum satellite altitude in degrees
    max_altitude: float
        Maximum satellite altitude in degrees
    data_source: str
        Original source of TLE data (celestrak or spacetrack)

    Returns
    -------
    response: dict
        A dictionary containing satellite information. The format of the dictionary
        is defined by the json_output() function.
    """

    parameters = extract_parameters(
        request,
        [
            "name",
            "latitude",
            "longitude",
            "elevation",
            "startjd",
            "stopjd",
            "stepjd",
            "min_altitude",
            "max_altitude",
            "data_source",
        ],
    )

    parameters = validate_parameters(
        parameters, ["name", "latitude", "longitude", "elevation", "startjd", "stopjd"]
    )

    jd0 = float(parameters["startjd"])
    jd1 = float(parameters["stopjd"])

    # default to 2 min
    jds = 0.00138889 if parameters["stepjd"] is None else float(parameters["stepjd"])

    jd = jd_arange(jd0, jd1, jds)

    if len(jd) > 1000:
        abort(400)

    tle = get_tle(
        parameters["name"], False, parameters["data_source"], jd[0].to_datetime()
    )

    result_list_task = tasks.create_result_list.apply(
        args=[
            parameters["location"],
            jd,
            tle.tle_line1,
            tle.tle_line2,
            tle.date_collected,
            parameters["name"],
            parameters["min_altitude"],
            parameters["max_altitude"],
            tle.tle_satellite.sat_number,
            tle.data_source,
        ]
    )
    result_list = result_list_task.get()
    return result_list


@api_v1.route("/ephemeris/catalog-number/")
@api_main.route("/ephemeris/catalog-number/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_catalog_number():
    """
    Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's catalog number using the Two Line Element
    Data Set at the specified Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.**

    Parameters
    ----------
    catalog: str
        Satellite Catalog Number of object
    latitude: float
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: float
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: float
        Elevation in meters
    julian_date: float
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    min_altitude: float
        Minimum satellite altitude in degrees
    max_altitude: float
        Maximum satellite altitude in degrees
    data_source: str
        Original source of TLE data (celestrak or spacetrack)

    Returns
    -------
    response: dict
        A dictionary containing satellite information. The format of the dictionary
        is defined by the json_output() function.
    """
    parameters = extract_parameters(
        request,
        [
            "catalog",
            "latitude",
            "longitude",
            "elevation",
            "julian_date",
            "min_altitude",
            "max_altitude",
            "data_source",
        ],
    )

    parameters = validate_parameters(
        parameters, ["catalog", "latitude", "longitude", "elevation", "julian_date"]
    )

    # Converting string to list
    try:
        jd = Time(parameters["julian_date"], format="jd", scale="ut1")
    except Exception:
        abort(500, error_messages.INVALID_JD)

    tle = get_tle(
        parameters["catalog"], True, parameters["data_source"], jd.to_datetime()
    )

    result_list_task = tasks.create_result_list.apply(
        args=[
            parameters["location"],
            [jd],
            tle.tle_line1,
            tle.tle_line2,
            tle.date_collected,
            tle.tle_satellite.sat_name,
            parameters["min_altitude"],
            parameters["max_altitude"],
            parameters["catalog"],
            tle.data_source,
        ]
    )
    result_list = result_list_task.get()
    return result_list


@api_v1.route("/ephemeris/catalog-number-jdstep/")
@api_main.route("/ephemeris/catalog-number-jdstep/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_catalog_number_jdstep():
    """
    Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's catalog number with the Two Line Element Data
    Set at the specified Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.**

    Parameters
    ----------
    catalog: str
        Satellite catalog number of object (NORAD ID)
    latitude: float
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: float
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: float
        Elevation in meters
    startjd: float
        UT1 Universal Time Julian Date to start ephmeris calculation.
    stopjd: float
        UT1 Universal Time Julian Date to stop ephmeris calculation.
    stepjd: float
        UT1 Universal Time Julian Date timestep.
    min_altitude: float
        Minimum satellite altitude in degrees
    max_altitude: float
        Maximum satellite altitude in degrees
    data_source: str
        Original source of TLE data (celestrak or spacetrack)

    Returns
    -------
    response: dict
        A dictionary containing satellite information. The format of the dictionary
        is defined by the json_output() function.
    """
    parameters = extract_parameters(
        request,
        [
            "catalog",
            "latitude",
            "longitude",
            "elevation",
            "startjd",
            "stopjd",
            "stepjd",
            "min_altitude",
            "max_altitude",
            "data_source",
        ],
    )

    parameters = validate_parameters(
        parameters,
        ["catalog", "latitude", "longitude", "elevation", "startjd", "stopjd"],
    )

    jd0 = float(parameters["startjd"])
    jd1 = float(parameters["stopjd"])

    # default to 2 min
    jds = 0.00138889 if parameters["stepjd"] is None else float(parameters["stepjd"])

    jd = jd_arange(jd0, jd1, jds)

    if len(jd) > 1000:
        app.logger.info("Too many results requested")
        abort(400)

    tle = get_tle(
        parameters["catalog"], True, parameters["data_source"], jd[0].to_datetime()
    )

    result_list_task = tasks.create_result_list.apply(
        args=[
            parameters["location"],
            jd,
            tle.tle_line1,
            tle.tle_line2,
            tle.date_collected,
            tle.tle_satellite.sat_name,
            parameters["min_altitude"],
            parameters["max_altitude"],
            parameters["catalog"],
            tle.data_source,
        ]
    )
    result_list = result_list_task.get()
    return result_list


@api_v1.route("/ephemeris/tle/")
@api_main.route("/ephemeris/tle/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_tle():
    """
    Returns satellite location and velocity information relative to the observer's
    coordinates for a given Two Line Element Data Set at the specified Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.**

    Parameters
    ----------
    tle: str
        Two line element set of object
    latitude: float
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: float
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: float
        Elevation in meters
    julian_date: float
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    min_altitude: float
        Minimum satellite altitude in degrees
    max_altitude: float
        Maximum satellite altitude in degrees

    Returns
    -------
    response: dict
        A dictionary containing satellite information. The format of the dictionary
        is defined by the json_output() function.
    """

    parameters = extract_parameters(
        request,
        [
            "tle",
            "latitude",
            "longitude",
            "elevation",
            "julian_date",
            "min_altitude",
            "max_altitude",
        ],
    )

    parameters = validate_parameters(
        parameters, ["tle", "latitude", "longitude", "elevation", "julian_date"]
    )

    # Converting string to list
    try:
        jd = Time(parameters["julian_date"], format="jd", scale="ut1")
    except Exception:
        abort(500, error_messages.INVALID_JD)

    tle = parse_tle(parameters["tle"])

    result_list_task = tasks.create_result_list.apply(
        args=[
            parameters["location"],
            [jd],
            tle.tle_line1,
            tle.tle_line2,
            tle.date_collected,
            tle.name,
            parameters["min_altitude"],
            parameters["max_altitude"],
            tle.catalog,
            "user",
        ]
    )
    result_list = result_list_task.get()
    return result_list


@api_v1.route("/ephemeris/tle-jdstep/")
@api_main.route("/ephemeris/tle-jdstep/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_tle_jdstep():
    """
    Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's catalog number with the Two Line Element Data
    Set at a specified Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.**

    Parameters
    ----------
    tle: str
        Two line element set of object
    latitude: float
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: float
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: float
        Elevation in meters
    startjd: float
        UT1 Universal Time Julian Date to start ephmeris calculation.
    stopjd: float
        UT1 Universal Time Julian Date to stop ephmeris calculation.
    stepjd: float
        UT1 Universal Time Julian Date timestep.
    min_altitude: float
        Minimum satellite altitude in degrees
    max_altitude: float
        Maximum satellite altitude in degrees

    Returns
    -------
    response: dict
        A dictionary containing satellite information. The format of the dictionary
        is defined by the json_output() function.
    """
    parameters = extract_parameters(
        request,
        [
            "tle",
            "latitude",
            "longitude",
            "elevation",
            "startjd",
            "stopjd",
            "stepjd",
            "min_altitude",
            "max_altitude",
        ],
    )

    parameters = validate_parameters(
        parameters, ["tle", "latitude", "longitude", "elevation", "startjd", "stopjd"]
    )

    jd0 = float(parameters["startjd"])
    jd1 = float(parameters["stopjd"])

    # default to 2 min
    jds = 0.00138889 if parameters["stepjd"] is None else float(parameters["stepjd"])

    jd = jd_arange(jd0, jd1, jds)

    if len(jd) > 1000:
        app.logger.info("Too many results requested")
        abort(400)

    tle = parse_tle(parameters["tle"])

    result_list_task = tasks.create_result_list.apply(
        args=[
            parameters["location"],
            jd,
            tle.tle_line1,
            tle.tle_line2,
            tle.date_collected,
            tle.name,
            parameters["min_altitude"],
            parameters["max_altitude"],
            tle.catalog,
            "user",
        ]
    )
    result_list = result_list_task.get()
    return result_list


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
    satellite_name = request.args.get("name").upper()

    if satellite_name is None:
        abort(400)

    try:
        norad_ids_and_dates = get_ids_for_satelltite_name(satellite_name)

        # Extract the IDs from the result set
        norad_ids_and_dates = [
            {
                "name": satellite_name,
                "norad_id": id_date[0],
                "date_added": id_date[1].strftime("%Y-%m-%d %H:%M:%S %Z"),
                "is_current_version": id_date[2],
            }
            for id_date in norad_ids_and_dates
        ]

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
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    satellite_id = request.args.get("id")
    if satellite_id is None:
        abort(400)

    try:
        satellite_names_and_dates = get_names_for_satellite_id(satellite_id)

        # Extract the names from the result set
        names_and_dates = [
            {
                "name": name_date[0],
                "norad_id": satellite_id,
                "date_added": name_date[1].strftime("%Y-%m-%d %H:%M:%S %Z"),
                "is_current_version": name_date[2],
            }
            for name_date in satellite_names_and_dates
        ]

        return jsonify(names_and_dates)
    except Exception as e:
        app.logger.error(e)
        return None


@api_v1.route("/tools/get-tle-data/")
@api_main.route("/tools/get-tle-data/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_tle_data():
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
        satellite ID, TLE lines, epoch, and date collected.

    Raises:
        400:
            If the satellite ID is not provided or the ID type is not
            'catalog' or 'name'.
        500:
            If there is a DataError when fetching the TLE data.
    """
    satellite_id = request.args.get("id")
    id_type = request.args.get("id_type")
    start_date = request.args.get("start_date_jd")
    end_date = request.args.get("end_date_jd")

    # TODO: Add more specific messages for 400 error codes
    if satellite_id is None:
        abort(400)

    if id_type != "catalog" and id_type != "name":
        abort(400)

    start_date = (
        Time(start_date, format="jd", scale="ut1")
        .to_datetime()
        .replace(tzinfo=timezone.utc)
        if start_date
        else None
    )
    end_date = (
        Time(end_date, format="jd", scale="ut1")
        .to_datetime()
        .replace(tzinfo=timezone.utc)
        if end_date
        else None
    )

    try:
        tle_data = get_tles(satellite_id, id_type, start_date, end_date)

        # Extract the TLE data from the result set
        tle_data = [
            {
                "satellite_name": tle.tle_satellite.sat_name,
                "satellite_id": tle.tle_satellite.sat_number,
                "tle_line1": tle.tle_line1,
                "tle_line2": tle.tle_line2,
                "epoch": tle.epoch.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "date_collected": tle.date_collected.strftime("%Y-%m-%d %H:%M:%S %Z"),
            }
            for tle in tle_data
        ]

        return jsonify(tle_data)

    except Exception as e:
        if isinstance(e, DataError):
            abort(500, f"{error_messages.NO_TLE_FOUND}, Exception: {str(e)}")
        app.logger.error(e)
        return None
