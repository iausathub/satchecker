from flask import abort, request

from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.common.exceptions import DataError, ValidationError
from api.entrypoints.extensions import db, get_forwarded_address, limiter
from api.services.ephemeris_service import (
    generate_ephemeris_data,
    generate_ephemeris_data_user,
)
from api.services.validation_service import validate_parameters

from . import api_main, api_source, api_v1, api_version


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
    session = db.session
    satellite_repository = SqlAlchemySatelliteRepository(session)
    tle_repository = SqlAlchemyTLERepository(session)

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

    try:
        position_data = generate_ephemeris_data(
            satellite_repository,
            tle_repository,
            parameters["name"],
            "name",
            parameters["location"],
            parameters["julian_dates"],
            parameters["min_altitude"],
            parameters["max_altitude"],
            api_source,
            api_version,
            parameters["data_source"],
        )
    except DataError as e:
        abort(e.status_code, e.message)

    session.close()

    return position_data


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
    session = db.session
    satellite_repository = SqlAlchemySatelliteRepository(session)
    tle_repository = SqlAlchemyTLERepository(session)

    parameter_list = [
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
    ]

    try:
        parameters = validate_parameters(
            request,
            parameter_list,
            ["name", "latitude", "longitude", "elevation", "startjd", "stopjd"],
        )
    except ValidationError as e:
        abort(e.status_code, e.message)

    try:
        position_data = generate_ephemeris_data(
            satellite_repository,
            tle_repository,
            parameters["name"],
            "name",
            parameters["location"],
            parameters["julian_dates"],
            parameters["min_altitude"],
            parameters["max_altitude"],
            api_source,
            api_version,
            parameters["data_source"],
        )
    except DataError as e:
        abort(e.status_code, e.message)
    session.close()

    return position_data


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
    session = db.session
    satellite_repository = SqlAlchemySatelliteRepository(session)
    tle_repository = SqlAlchemyTLERepository(session)

    parameter_list = [
        "catalog",
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
            ["catalog", "latitude", "longitude", "elevation", "julian_date"],
        )
    except ValidationError as e:
        abort(e.status_code, e.message)

    position_data = generate_ephemeris_data(
        satellite_repository,
        tle_repository,
        parameters["catalog"],
        "catalog_number",
        parameters["location"],
        parameters["julian_dates"],
        parameters["min_altitude"],
        parameters["max_altitude"],
        api_source,
        api_version,
        parameters["data_source"],
    )
    session.close()

    return position_data


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
    session = db.session
    satellite_repository = SqlAlchemySatelliteRepository(session)
    tle_repository = SqlAlchemyTLERepository(session)

    parameter_list = [
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
    ]

    try:
        parameters = validate_parameters(
            request,
            parameter_list,
            ["catalog", "latitude", "longitude", "elevation", "startjd", "stopjd"],
        )
    except ValidationError as e:
        abort(e.status_code, e.message)

    try:
        position_data = generate_ephemeris_data(
            satellite_repository,
            tle_repository,
            parameters["catalog"],
            "catalog_number",
            parameters["location"],
            parameters["julian_dates"],
            parameters["min_altitude"],
            parameters["max_altitude"],
            api_source,
            api_version,
            parameters["data_source"],
        )
    except DataError as e:
        abort(e.status_code, e.message)
    session.close()

    return position_data


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
    session = db.session
    parameter_list = [
        "tle",
        "latitude",
        "longitude",
        "elevation",
        "julian_date",
        "min_altitude",
        "max_altitude",
    ]

    try:
        parameters = validate_parameters(
            request,
            parameter_list,
            ["tle", "latitude", "longitude", "elevation", "julian_date"],
        )
    except ValidationError as e:
        abort(e.status_code, e.message)

    position_data = generate_ephemeris_data_user(
        parameters["tle"],
        parameters["location"],
        parameters["julian_dates"],
        parameters["min_altitude"],
        parameters["max_altitude"],
        api_source,
        api_version,
    )
    session.close()

    return position_data


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
    session = db.session
    parameter_list = [
        "tle",
        "latitude",
        "longitude",
        "elevation",
        "startjd",
        "stopjd",
        "stepjd",
        "min_altitude",
        "max_altitude",
    ]

    try:
        parameters = validate_parameters(
            request,
            parameter_list,
            ["tle", "latitude", "longitude", "elevation", "startjd", "stopjd"],
        )
    except ValidationError as e:
        abort(e.status_code, e.message)

    position_data = generate_ephemeris_data_user(
        parameters["tle"],
        parameters["location"],
        parameters["julian_dates"],
        parameters["min_altitude"],
        parameters["max_altitude"],
        api_source,
        api_version,
    )
    session.close()

    return position_data
