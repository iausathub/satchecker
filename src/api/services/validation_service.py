import astropy.units as u
import common.error_messages as error_messages
import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from common.exceptions import ValidationError


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
    for param in parameter_list:
        parameters[param] = request.args.get(param, None)

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
            ValidationError(400, f"Missing parameter: {param}")

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
    try:
        parameters["location"] = EarthLocation(
            lat=float(parameters["latitude"]) * u.deg,
            lon=float(parameters["longitude"]) * u.deg,
            height=float(parameters["elevation"]) * u.m,
        )
    except Exception:
        ValidationError(500, "Invalid location")

    # if min_altitude is not none convert to float
    try:
        parameters["min_altitude"] = (
            float(parameters["min_altitude"])
            if parameters["min_altitude"] is not None
            else 0
        )
        parameters["max_altitude"] = (
            float(parameters["max_altitude"])
            if parameters["max_altitude"] is not None
            else 90
        )
    except Exception:
        ValidationError(500, error_messages.INVALID_PARAMETER)

    if "julian_date" in parameters.keys():
        try:
            # Convert the Julian Date to an astropy Time object - the new
            # parameter is a list to match the case for the jd range requests
            parameters["julian_dates"] = [
                Time(parameters["julian_date"], format="jd", scale="ut1")
            ]

        except Exception:
            ValidationError(500, error_messages.INVALID_JD)

    if "start_jd" in parameters.keys() and "stop_jd" in parameters.keys():
        try:
            # default to 2 min
            jd_step = (
                0.00138889
                if parameters["stepjd"] not in parameters
                else float(parameters["stepjd"])
            )

            julian_dates = jd_arange(
                float(parameters["startjd"]),
                float(parameters["stopjd"]),
                jd_step,
            )

            if len(julian_dates) > 1000:
                ValidationError(400, error_messages.TOO_MANY_RESULTS)

        except Exception:
            ValidationError(500, error_messages.INVALID_JD)

    if "data_source" in parameters.keys():
        parameters["data_source"] = (
            parameters["data_source"].lower()
            if parameters["data_source"] is not None
            else "any"
        )
        if parameters["data_source"] not in ["celestrak", "spacetrack", "any"]:
            ValidationError(500, "Invalid data source")

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
    except Exception:
        ValidationError(500, error_messages.INVALID_JD)

    return results
