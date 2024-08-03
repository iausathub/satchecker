from api.common.exceptions import ValidationError
from extensions import get_forwarded_address, limiter
from flask import abort, request
from services.ephemeris_service import generate_ephemeris_data
from services.validation_service import validate_parameters

from . import api_main, api_v1


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
    parameter_list = [
        "name",
        "latitude",
        "longitude",
        "elevation",
        "julian_date",
        "min_altitude",
        "max_altitude",
        "data_source",
    ]

    try:
        parameters = validate_parameters(
            request,
            parameter_list,
            ["name", "latitude", "longitude", "elevation", "julian_date"],
        )
    except ValidationError as e:
        abort(e.status_code, e.message)

    position_data = generate_ephemeris_data(
        parameters["name"],
        "name",
        parameters["location"],
        parameters["julian_date"],
        parameters["min_altitude"],
        parameters["max_altitude"],
        parameters["data_source"],
    )

    return position_data
