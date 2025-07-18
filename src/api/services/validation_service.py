import re
from datetime import datetime, timedelta, timezone
from typing import Any

import astropy.units as u
import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time

import api.common.error_messages as error_messages
from api.common.exceptions import ValidationError
from api.domain.models.satellite import Satellite
from api.domain.models.tle import TLE
from api.utils.location_utils import get_location_from_astropy_site


def extract_parameters(request, parameter_list):
    """
    Extracts specified parameters from a request object.

    This function iterates over a list of parameters and attempts to retrieve
    each one from the request's arguments. If a parameter is not found, it is
    set to None.

    Parameters:
        request (flask.Request): The request object to extract parameters from.
        parameter_list (list of str): A list of parameter names to extract.

    Returns:
        dict: A dictionary where the keys are the parameter names and the values
        are the extracted parameters or None if the parameter was not found.
    """

    parameters = {}
    try:
        for param in parameter_list:
            parameters[param] = request.args.get(param, None)
    except Exception as e:
        raise ValidationError(500, error_messages.INVALID_PARAMETER, e) from e

    return parameters


def validate_parameters(
    request: Any, parameter_list: list[str], required_parameters: list[str]
) -> dict[str, Any]:
    """
    Validates and sanitizes parameters for satellite tracking.

    This function checks if all required parameters are present in the input parameters.
    It then converts latitude, longitude, and elevation to floats and constructs an
    EarthLocation object. It also sanitizes the min_altitude, max_altitude, and
    data_source parameters.

    Parameters:
        parameters (list of str): The input parameters to validate and sanitize.
        required_parameters (list of str): A list of parameter names that are required.

    Returns:
        dict: The validated and sanitized parameters.

    Raises:
        HTTPException: If a required parameter is missing, if the location parameters are
            invalid, if the altitude parameters are invalid, or if the data source is invalid.
    """  # noqa: E501
    parameters = extract_parameters(request, parameter_list)

    for param in required_parameters:
        if param not in parameters.keys() or parameters[param] is None:
            raise ValidationError(400, f"Missing parameter: {param}")

    # Check if site is provide first, so that if it and other location parameters
    # are provided, an error can be thrown
    if "site" in parameters.keys() and parameters["site"] is not None:
        if (
            ("latitude" in parameters.keys() and parameters["latitude"] is not None)
            or (
                "longitude" in parameters.keys() and parameters["longitude"] is not None
            )
            or (
                "elevation" in parameters.keys() and parameters["elevation"] is not None
            )
        ):
            raise ValidationError(400, error_messages.SITE_AND_LOCATION_ERROR)
        try:
            site_location = get_location_from_astropy_site(parameters["site"])
            parameters["location"] = site_location
        except Exception as e:
            raise ValidationError(500, error_messages.INVALID_SITE, e) from e

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
    if (
        "latitude" in parameters.keys()
        and parameters["latitude"] is not None
        and "longitude" in parameters.keys()
        and parameters["longitude"] is not None
        and "elevation" in parameters.keys()
        and parameters["elevation"] is not None
    ):
        try:
            parameters["location"] = EarthLocation(
                lat=float(parameters["latitude"]) * u.deg,
                lon=float(parameters["longitude"]) * u.deg,
                height=float(parameters["elevation"]) * u.m,
            )
        except Exception as e:
            raise ValidationError(500, "Invalid location", e) from e

    # if min_altitude is not none convert to float
    try:
        if "min_altitude" in parameters:
            parameters["min_altitude"] = (
                float(parameters["min_altitude"])
                if parameters["min_altitude"] is not None
                else 0
            )

        if "max_altitude" in parameters:
            parameters["max_altitude"] = (
                float(parameters["max_altitude"])
                if parameters["max_altitude"] is not None
                else 90
            )
    except Exception as e:
        raise ValidationError(500, error_messages.INVALID_PARAMETER, e) from e

    if "julian_date" in parameters.keys():
        try:
            # Convert the Julian Date to an astropy Time object - the new
            # parameter is a list to match the case for the jd range requests
            parameters["julian_dates"] = [
                Time(parameters["julian_date"], format="jd", scale="ut1")
            ]

        except Exception as e:
            raise ValidationError(
                500, error_messages.INVALID_JD + " - 'julian_date'"
            ) from e

    if "startjd" in parameters.keys() and "stopjd" in parameters.keys():
        try:
            # default to 2 min
            jd_step = (
                0.00138889
                if "stepjd" not in parameters
                else float(parameters["stepjd"])
            )

            julian_dates = jd_arange(
                float(parameters["startjd"]),
                float(parameters["stopjd"]),
                jd_step,
            )

            if len(julian_dates) > 1000:
                raise ValidationError(400, error_messages.TOO_MANY_RESULTS)

            parameters["julian_dates"] = julian_dates

        except Exception as e:
            if isinstance(e, ValidationError):
                raise e
            else:
                raise ValidationError(
                    500, error_messages.INVALID_JD + " - 'startjd' or 'stopjd'", e
                ) from e

    if "data_source" in parameters.keys():
        parameters["data_source"] = (
            parameters["data_source"].lower()
            if parameters["data_source"] is not None
            else "any"
        )
        if parameters["data_source"] not in ["celestrak", "spacetrack", "any"]:
            raise ValidationError(
                500,
                error_messages.INVALID_SOURCE
                + " - data_source must be 'celestrak', 'spacetrack', or 'any'",
            )

    if "tle" in parameters.keys():
        parameters["tle"] = parse_tle(parameters["tle"])

    # TODO: used for tools endpoints, might not be needed here (move to tools service?)
    if "name" in parameters.keys() and len(parameters) == 1:
        parameters["name"] = parameters["name"].upper()

    if "id_type" in parameters.keys():
        if parameters["id_type"] not in ["catalog", "name"]:
            raise ValidationError(
                400,
                error_messages.INVALID_PARAMETER
                + " id_type must be 'catalog' or 'name'",
            )

        # Special case for get-adjacent-tles endpoint
        if (
            request.path.endswith("/get-adjacent-tles/")
            and parameters["id_type"] != "catalog"
        ):
            raise ValidationError(
                400,
                "For get-adjacent-tles, only id_type='catalog' is currently supported",
            )

        if (
            request.path.endswith("/get-tles-around-epoch/")
            and parameters["id_type"] != "catalog"
        ):
            raise ValidationError(
                400,
                "For get-tles-around-epoch, only id_type='catalog' is currently supported",  # noqa: E501
            )

    if "end_date_jd" in parameters.keys() and parameters["end_date_jd"] is not None:
        try:
            parameters["end_date_jd"] = (
                Time(parameters["end_date_jd"], format="jd", scale="ut1")
                .to_datetime()
                .replace(tzinfo=timezone.utc)
            )
        except Exception as e:
            raise ValidationError(
                500, error_messages.INVALID_JD + " - 'end_date_jd'", e
            ) from e

    if "start_date_jd" in parameters.keys() and parameters["start_date_jd"] is not None:
        try:
            parameters["start_date_jd"] = (
                Time(parameters["start_date_jd"], format="jd", scale="ut1")
                .to_datetime()
                .replace(tzinfo=timezone.utc)
            )
        except Exception as e:
            raise ValidationError(
                500, error_messages.INVALID_JD + " - 'start_date_jd'", e
            ) from e

    # If either mid_obs_time_jd or start_time_jd is provided, use the appropriate one

    # Validate mid_obs_time_jd and start_time_jd are mutually exclusive
    if "mid_obs_time_jd" in parameters and "start_time_jd" in parameters:
        if (
            parameters["mid_obs_time_jd"] is not None
            and parameters["start_time_jd"] is not None
        ):
            raise ValidationError(
                400, "Cannot specify both mid_obs_time_jd and start_time_jd"
            )
        if (
            parameters["mid_obs_time_jd"] is None
            and parameters["start_time_jd"] is None
        ):
            raise ValidationError(
                400, "Must specify either mid_obs_time_jd or start_time_jd"
            )

    # Convert whichever time parameter is provided to a Time object
    if "mid_obs_time_jd" in parameters.keys() or "start_time_jd" in parameters.keys():
        time_param = (
            "mid_obs_time_jd"
            if parameters.get("mid_obs_time_jd") is not None
            else "start_time_jd"
        )
        try:
            parameters[time_param] = Time(
                parameters[time_param], format="jd", scale="ut1"
            )
        except Exception as e:
            raise ValidationError(
                500,
                error_messages.INVALID_JD + " - 'mid_obs_time_jd' or 'start_time_jd'",
                e,
            ) from e

    if "epoch" in parameters.keys() and parameters["epoch"] is not None:
        try:
            parameters["epoch"] = (
                Time(parameters["epoch"], format="jd", scale="ut1")
                .to_datetime()
                .replace(tzinfo=timezone.utc)
            )
        except Exception as e:
            raise ValidationError(
                500, error_messages.INVALID_JD + " - 'epoch'", e
            ) from e

    if "ra" in parameters.keys() and parameters["ra"] is not None:
        try:
            parameters["ra"] = float(parameters["ra"])
        except Exception as e:
            raise ValidationError(
                500, error_messages.INVALID_PARAMETER + " - ra", e
            ) from e

    if "dec" in parameters.keys() and parameters["dec"] is not None:
        try:
            parameters["dec"] = float(parameters["dec"])
        except Exception as e:
            raise ValidationError(
                500, error_messages.INVALID_PARAMETER + " - dec", e
            ) from e

    if "fov_radius" in parameters.keys() and parameters["fov_radius"] is not None:
        try:
            parameters["fov_radius"] = float(parameters["fov_radius"])
        except Exception as e:
            raise ValidationError(
                500, error_messages.INVALID_PARAMETER + " - fov_radius", e
            ) from e

    if "duration" in parameters.keys() and parameters["duration"] is not None:
        try:
            parameters["duration"] = float(parameters["duration"])
        except Exception as e:
            raise ValidationError(
                500, error_messages.INVALID_PARAMETER + " - duration", e
            ) from e

    if "count_before" in parameters.keys():
        if parameters["count_before"] is not None:
            try:
                if int(parameters["count_before"]) < 0:
                    raise ValidationError(
                        500,
                        error_messages.INVALID_PARAMETER
                        + " count_before must be greater than 0",
                    )
                parameters["count_before"] = int(parameters["count_before"])
            except Exception as e:
                raise ValidationError(500, error_messages.INVALID_PARAMETER, e) from e
        else:
            parameters["count_before"] = 2

    if "count_after" in parameters.keys():
        if parameters["count_after"] is not None:
            try:
                if int(parameters["count_after"]) < 0:
                    raise ValidationError(
                        500,
                        error_messages.INVALID_PARAMETER
                        + " count_after must be greater than 0",
                    )
                parameters["count_after"] = int(parameters["count_after"])
            except Exception as e:
                raise ValidationError(500, error_messages.INVALID_PARAMETER, e) from e
        else:
            parameters["count_after"] = 2

    if "format" in parameters.keys() and parameters["format"] is not None:
        parameters["format"] = parameters["format"].lower()

        if parameters["format"] not in ["json", "zip", "txt"]:
            raise ValidationError(500, error_messages.INVALID_FORMAT)

    if "group_by" in parameters.keys() and parameters["group_by"] is not None:
        parameters["group_by"] = (
            parameters["group_by"].lower()
            if parameters["group_by"] is not None
            else "time"
        )

        if parameters["group_by"] not in ["satellite", "time"]:
            raise ValidationError(
                400,
                error_messages.INVALID_PARAMETER
                + " group_by must be 'satellite' or 'time'",
            )

    if "include_tles" in parameters.keys() and parameters["include_tles"] is not None:
        if parameters["include_tles"] not in ["true", "false"]:
            raise ValidationError(
                400,
                error_messages.INVALID_PARAMETER
                + " include_tles must be 'true' or 'false'",
            )

        parameters["include_tles"] = parameters["include_tles"].lower() == "true"

    if "skip_cache" in parameters.keys() and parameters["skip_cache"] is not None:
        if parameters["skip_cache"] not in ["true", "false"]:
            raise ValidationError(
                400,
                error_messages.INVALID_PARAMETER
                + " skip_cache must be 'true' or 'false'",
            )

        parameters["skip_cache"] = parameters["skip_cache"].lower() == "true"

    if (
        "illuminated_only" in parameters.keys()
        and parameters["illuminated_only"] is not None
    ):
        if parameters["illuminated_only"] not in ["true", "false"]:
            raise ValidationError(
                400,
                error_messages.INVALID_PARAMETER
                + " illuminated_only must be 'true' or 'false'",
            )

        parameters["illuminated_only"] = (
            parameters["illuminated_only"].lower() == "true"
        )

    if "object_type" in parameters.keys() and parameters["object_type"] is not None:
        parameters["object_type"] = parameters["object_type"].lower()
        if parameters["object_type"] not in [
            "payload",
            "debris",
            "rocket body",
            "tba",
            "unknown",
        ]:
            raise ValidationError(
                400,
                error_messages.INVALID_PARAMETER
                + " object_type must be 'payload', 'debris', 'rocket body', "
                "'tba', or 'unknown'",
            )

    if "constellation" in parameters.keys() and parameters["constellation"] is not None:
        parameters["constellation"] = parameters["constellation"].lower()
        if parameters["constellation"] not in [
            "starlink",
            "oneweb",
            "kuiper",
            "planet",
            "ast",
        ]:
            raise ValidationError(
                400,
                error_messages.INVALID_PARAMETER
                + " constellation must be 'starlink', 'oneweb', "
                + "'kuiper', 'planet', or 'ast'",
            )

    try:
        if "min_range" in parameters:
            parameters["min_range"] = (
                float(parameters["min_range"])
                if parameters["min_range"] is not None
                else 0
            )

        if "max_range" in parameters:
            parameters["max_range"] = (
                float(parameters["max_range"])
                if parameters["max_range"] is not None
                else 1500000  # farthest possible distance in Earth's gravity
            )
    except Exception as e:
        raise ValidationError(500, error_messages.INVALID_PARAMETER, e) from e

    return dict(parameters)


def jd_arange(a, b, dr, decimals=11):
    """
    Generates a sequence of Julian Dates between two given dates with a specified increment.

    This function compensates for round-off errors by rounding the computed dates to a
    specified number of decimal places.

    Parameters
    ----------
    a : float
        The first Julian Date in the sequence.
    b : float
        The last Julian Date in the sequence. If the exact date `b` cannot be included due
        to the increment `dr`, the sequence will stop at the nearest date before `b`.
    dr : float
        The increment between consecutive Julian Dates in the sequence.
    decimals : int, optional
        The number of decimal places to which each computed Julian Date should be rounded.
        Default is 11.

    Returns
    -------
    results : astropy.time.core.Time
        An array of astropy Time objects representing the Julian Dates between `a` and `b`
        with an increment of `dr`.

    Raises
    ------
    500:
        If an invalid Julian Date is encountered.
    """  # noqa: E501
    try:
        res = [np.round(a, decimals)]
        k = 1
        while res[-1] < b:
            tmp = np.round(a + k * dr, decimals)
            if tmp > b:
                break
            res.append(tmp)
            k += 1
        dates = np.asarray(res)

        results = Time(dates, format="jd", scale="ut1")
    except Exception as e:
        raise ValidationError(500, error_messages.INVALID_JD, e) from e

    return results


def parse_tle(tle):
    """
    Parses a URL-encoded Two-Line Element (TLE) string and returns a TLE object.

    Args:
        tle (str): A URL-encoded TLE string. The string can be either two or three lines,
                   separated by newline characters (`\n` or `\\n`).

    Returns:
        TLE: An object containing the parsed TLE data.

    Raises:
        ValidationError: If the TLE format is incorrect

    Example:
        >>> tle_string = "1 25544U 98067A   21275.48835648  .00002182  00000-0  51170-4 0  9993\\n2 25544  51.6442  21.4776 0003887  45.3456  314.6567 15.48815347275345"
        >>> tle = parse_tle(tle_string)
        >>> print(tle)
        TLE(tle_line1='1 25544U 98067A   21275.48835648  .00002182  00000-0  51170-4 0  9993', tle_line2='2 25544  51.6442  21.4776 0003887  45.3456  314.6567 15.48815347275345', date_collected=None, name=None, catalog='2554', data_source='user')
    """  # noqa: E501
    try:
        # parse url encoded parameter to string to remove space encoding
        tle = tle.replace("%20", " ")

        # split string into three lines based on url encoded space character
        pattern = re.compile(r"\\n|\n")
        tle_data = pattern.split(tle)
    except Exception as e:
        raise ValidationError(500, error_messages.INVALID_TLE, e) from e

    try:
        if len(tle_data) == 3:
            name = tle_data[0].strip()
            tle_line_1 = tle_data[1].strip()
            tle_line_2 = tle_data[2].strip()
        else:
            name = ""
            tle_line_1 = tle_data[0].strip()
            tle_line_2 = tle_data[1].strip()

        # if any are null throw error
        if (
            [x for x in (tle_line_1, tle_line_2) if x is None]
            or len(tle_line_1) != 69
            or len(tle_line_2) != 69
        ):
            raise ValidationError(500, error_messages.INVALID_TLE)
    except Exception as e:
        raise ValidationError(500, error_messages.INVALID_TLE, e) from e

    # Parse the epoch from the TLE line 1
    # TLE epoch is in the format YYDDD.FRACTION at positions 18-32
    epoch_year = int(tle_line_1[18:20])
    epoch_year = epoch_year + (
        1900 if epoch_year >= 57 else 2000
    )  # Convert 2-digit year
    epoch_day = float(tle_line_1[20:32])

    # Day of year to date
    epoch_date = datetime(epoch_year, 1, 1, tzinfo=timezone.utc)
    epoch_date = epoch_date + timedelta(days=epoch_day - 1)

    catalog = int(tle_line_1[2:7])
    satellite = Satellite(sat_number=catalog, sat_name=name)
    tle = TLE(
        tle_line1=tle_line_1,
        tle_line2=tle_line_2,
        date_collected=datetime.now(timezone.utc),
        epoch=epoch_date,
        is_supplemental=False,
        satellite=satellite,
        data_source="user",
    )
    return tle
