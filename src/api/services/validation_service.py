import astropy.units as u
import common.error_messages as error_messages
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
            parameters["julian_date"] = Time(
                parameters["julian_date"], format="jd", scale="ut1"
            )
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
