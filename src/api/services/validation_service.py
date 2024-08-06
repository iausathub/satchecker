import re

import astropy.units as u
import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time

import src.api.common.error_messages as error_messages
from src.api.common.exceptions import ValidationError
from src.api.domain.models.satellite import Satellite
from src.api.domain.models.tle import TLE


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


def validate_parameters(request, parameter_list, required_parameters):
    """
    Validates and sanitizes parameters for satellite tracking.

    This function checks if all required parameters are present in the input parameters.
    It then converts latitude, longitude, and elevation to floats and constructs an
    EarthLocation object. It also sanitizes the min_altitude, max_altitude, and
    data_source parameters.

    Parameters:
        parameters (dict): The input parameters to validate and sanitize.
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

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
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
            raise ValidationError(500, error_messages.INVALID_JD, e) from e

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
                raise ValidationError(500, error_messages.INVALID_JD, e) from e

    if "data_source" in parameters.keys():
        parameters["data_source"] = (
            parameters["data_source"].lower()
            if parameters["data_source"] is not None
            else "any"
        )
        if parameters["data_source"] not in ["celestrak", "spacetrack", "any"]:
            raise ValidationError(500, "Invalid data source")

    if "tle" in parameters.keys():
        parameters["tle"] = parse_tle(parameters["tle"])

    return parameters


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
    # parse url encoded parameter to string to remove space encoding
    tle = tle.replace("%20", " ")

    # split string into three lines based on url encoded space character
    try:
        pattern = re.compile(r"\\n|\n")
        tle_data = pattern.split(tle)
    except Exception as e:
        raise ValidationError(500, "Incorrect TLE format", e) from e

    try:
        if len(tle_data) == 3:
            name = tle_data[0].strip()
            tle_line_1 = tle_data[1].strip()
            tle_line_2 = tle_data[2].strip()
        else:
            name = None
            tle_line_1 = tle_data[0].strip()
            tle_line_2 = tle_data[1].strip()

        # if any are null throw error
        if (
            [x for x in (tle_line_1, tle_line_2) if x is None]
            or len(tle_line_1) != 69
            or len(tle_line_2) != 69
        ):
            raise ValidationError(500, "Incorrect TLE format")
    except Exception as e:
        raise ValidationError(500, "Incorrect TLE format", e) from e

    catalog = tle_line_1[2:7]
    satellite = Satellite(sat_number=catalog, sat_name=name)
    tle = TLE(
        tle_line1=tle_line_1,
        tle_line2=tle_line_2,
        date_collected=None,
        epoch=None,
        is_supplemental=False,
        satellite=satellite,
        data_source="user",
    )
    return tle
