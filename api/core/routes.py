#!/usr/bin/python3
import re
from collections import namedtuple

import astropy.units as u
import numpy as np
import requests
from astropy.coordinates import EarthLocation
from astropy.time import Time, TimeDelta
from flask import abort, redirect, request
from flask_limiter.util import get_remote_address
from skyfield.api import EarthSatellite, load, wgs84
from sqlalchemy import func

from core import app, limiter
from core.database import models
from core.extensions import db


# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return (
        "Error 404: Page not found<br /> \
        Check your spelling to ensure you are accessing the correct endpoint.",
        404,
    )


@app.errorhandler(400)
def missing_parameter(e):
    return (
        "Error 400: Incorrect parameters or too many results to return \
        (maximum of 1000 in a single request)<br /> \
        Check your request and try again.",
        400,
    )


@app.errorhandler(429)
def ratelimit_handler(e):
    return "Error 429: You have exceeded your rate limit:<br />" + e.description, 429


@app.errorhandler(500)
def internal_server_error(e):
    return "Error 500: Internal server error:<br />" + e.description, 500


# Redirects user to the Center for the Protection of Dark and Quiet Sky homepage
@app.route("/")
@app.route("/index")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def root():
    return redirect("https://satchecker.readthedocs.io/en/latest/")


@app.route("/health")
@limiter.exempt
def health():
    try:
        response = requests.get("https://cps.iau.org/tools/satchecker/api/", timeout=10)
        response.raise_for_status()
    except Exception:
        abort(503, "Error: Unable to connect to IAU CPS URL")
    else:
        return {"message": "Healthy"}


@app.route("/ephemeris/name/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_name():
    """Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's Two Line Element Data Set at a specified
    Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE
    epoch is necessary.

    Parameters
    ----------
    name: 'str'
        CelesTrak name of object
    latitude: 'float'
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: 'float'
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: 'float'
        Elevation in meters
    julian_date: 'float'
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    min_altitude: 'float'
        Minimum satellite altitude in degrees
    max_altitude: 'float'
        Maximum satellite altitude in degrees
    data_source: 'str'
        Original source of TLE data (celestrak or spacetrack)

    Returns
    -------
    response: 'dictionary'
        JSON output with satellite information - see json_output() for format
    """
    name = request.args.get("name")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    elevation = request.args.get("elevation")
    julian_date = request.args.get("julian_date")
    min_altitude = request.args.get("min_altitude")
    max_altitude = request.args.get("max_altitude")
    data_source = request.args.get("data_source")

    # check for mandatory parameters
    if [x for x in (name, latitude, longitude, elevation, julian_date) if x is None]:
        abort(400)

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
    try:
        location = EarthLocation(
            lat=float(latitude) * u.deg,
            lon=float(longitude) * u.deg,
            height=float(elevation) * u.m,
        )
    except Exception:
        abort(500, "Error: Invalid location parameters")

    try:
        # if min_altitude is not none convert to float
        min_altitude = float(min_altitude) if min_altitude is not None else None
        max_altitude = float(max_altitude) if max_altitude is not None else None
        if min_altitude is None:
            min_altitude = 0
        if max_altitude is None:
            max_altitude = 90
    except Exception:
        abort(500, "Error: Invalid parameter format")

    # Test JD format
    try:
        jd = Time(julian_date, format="jd", scale="ut1")
    except Exception:
        abort(500, "Error: Invalid Julian Date")

    try:
        data_source = data_source.lower() if data_source is not None else None
        if data_source is None:
            data_source = "spacetrack"
        if data_source not in ["celestrak", "spacetrack"]:
            raise Exception
    except Exception:
        abort(500, "Error: Invalid data source")

    tle = get_tle(name, False, data_source, jd.to_datetime())
    return create_result_list(
        location,
        [jd],
        tle[0].tle_line1,
        tle[0].tle_line2,
        tle[0].date_collected,
        name,
        min_altitude,
        max_altitude,
        tle[1].sat_number,
        data_source,
    )


@app.route("/ephemeris/name-jdstep/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_name_jdstep():
    """Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's name with the Two Line Element Data Set at
    a specified Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.

    Parameters
    ----------
    name: 'str'
        CelesTrak name of object
    latitude: 'float'
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: 'float'
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: 'float'
        Elevation in meters
    startjd: 'float'
        UT1 Universal Time Julian Date to start ephmeris calculation.
    stopjd: 'float'
        UT1 Universal Time Julian Date to stop ephmeris calculation.
    stepjd: 'float'
        UT1 Universal Time Julian Date timestep.
    min_altitude: 'float'
        Minimum satellite altitude in degrees
    max_altitude: 'float'
        Maximum satellite altitude in degrees
    data_source: 'str'
        Original source of TLE data (celestrak or spacetrack)

    Returns
    -------
    response: 'dictionary'
        JSON output with satellite information - see json_output() for format
    """
    name = request.args.get("name")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    elevation = request.args.get("elevation")
    startjd = request.args.get("startjd")
    stopjd = request.args.get("stopjd")
    stepjd = request.args.get("stepjd")
    min_altitude = request.args.get("min_altitude")
    max_altitude = request.args.get("max_altitude")
    data_source = request.args.get("data_source")

    # check for mandatory parameters
    if [
        x for x in (name, latitude, longitude, elevation, startjd, stopjd) if x is None
    ]:
        abort(400)

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
    try:
        location = EarthLocation(
            lat=float(latitude) * u.deg,
            lon=float(longitude) * u.deg,
            height=float(elevation) * u.m,
        )
    except Exception:
        abort(500, "Error: Invalid location parameters")

    try:
        min_altitude = float(min_altitude) if min_altitude is not None else None
        max_altitude = float(max_altitude) if max_altitude is not None else None
        if min_altitude is None:
            min_altitude = 0
        if max_altitude is None:
            max_altitude = 90
    except Exception:
        abort(500, "Error: Invalid parameter format")

    try:
        data_source = data_source.lower() if data_source is not None else None
        if data_source is None:
            data_source = "spacetrack"
        if data_source not in ["celestrak", "spacetrack"]:
            raise Exception
    except Exception:
        abort(500, "Error: Invalid data source")

    jd0 = float(startjd)
    jd1 = float(stopjd)

    jds = 0.00138889 if stepjd is None else float(stepjd)  # default to 2 min

    jd = jd_arange(jd0, jd1, jds)

    if len(jd) > 1000:
        abort(400)

    tle = get_tle(name, False, data_source, jd[0].to_datetime())
    return create_result_list(
        location,
        jd,
        tle[0].tle_line1,
        tle[0].tle_line2,
        tle[0].date_collected,
        name,
        min_altitude,
        max_altitude,
        tle[1].sat_number,
        data_source,
    )


@app.route("/ephemeris/catalog-number/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_catalog_number():
    """Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's catalog number using the Two Line Element
    Data Set at the specified Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.

    Parameters
    ----------
    catalog: 'str'
        Satellite Catalog Number of object
    latitude: 'float'
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: 'float'
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: 'float'
        Elevation in meters
    julian_date: 'float'
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    min_altitude: 'float'
        Minimum satellite altitude in degrees
    max_altitude: 'float'
        Maximum satellite altitude in degrees
    data_source: 'str'
        Original source of TLE data (celestrak or spacetrack)

    Returns
    -------
    response: 'dictionary'
        JSON output with satellite information - see json_output() for format
    """
    catalog = request.args.get("catalog")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    elevation = request.args.get("elevation")
    julian_date = request.args.get("julian_date")
    min_altitude = request.args.get("min_altitude")
    max_altitude = request.args.get("max_altitude")
    data_source = request.args.get("data_source")

    # check for mandatory parameters
    if [x for x in (catalog, latitude, longitude, elevation, julian_date) if x is None]:
        abort(400)

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
    try:
        location = EarthLocation(
            lat=float(latitude) * u.deg,
            lon=float(longitude) * u.deg,
            height=float(elevation) * u.m,
        )
    except Exception:
        abort(500, "Error: Invalid location parameters")

    try:
        min_altitude = float(min_altitude) if min_altitude is not None else None
        max_altitude = float(max_altitude) if max_altitude is not None else None
        if min_altitude is None:
            min_altitude = 0
        if max_altitude is None:
            max_altitude = 90
    except Exception:
        abort(500, "Error: Invalid parameter format")

    # Converting string to list
    try:
        jd = Time(julian_date, format="jd", scale="ut1")
    except Exception:
        abort(500, "Error: Invalid Julian Date")

    try:
        data_source = data_source.lower() if data_source is not None else None
        if data_source is None:
            data_source = "spacetrack"
        if data_source not in ["celestrak", "spacetrack"]:
            raise Exception
    except Exception:
        abort(500, "Error: Invalid data source")

    tle = get_tle(catalog, True, data_source, jd.to_datetime())
    return create_result_list(
        location,
        [jd],
        tle[0].tle_line1,
        tle[0].tle_line2,
        tle[0].date_collected,
        tle[1].sat_name,
        min_altitude,
        max_altitude,
        tle[1].sat_number,
        data_source,
    )


@app.route("/ephemeris/catalog-number-jdstep/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_catalog_number_jdstep():
    """Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's catalog number with the Two Line Element Data
    Set at the specfied Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.

    Parameters
    ----------
    catalog: 'str'
        Satellite catalog number of object (NORAD ID)
    latitude: 'float'
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: 'float'
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: 'float'
        Elevation in meters
    startjd: 'float'
        UT1 Universal Time Julian Date to start ephmeris calculation.
    stopjd: 'float'
        UT1 Universal Time Julian Date to stop ephmeris calculation.
    stepjd: 'float'
        UT1 Universal Time Julian Date timestep.
    min_altitude: 'float'
        Minimum satellite altitude in degrees
    max_altitude: 'float'
        Maximum satellite altitude in degrees
    data_source: 'str'
        Original source of TLE data (celestrak or spacetrack)

    Returns
    -------
    response: 'dictionary'
        JSON output with satellite information - see json_output() for format
    """
    catalog = request.args.get("catalog")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    elevation = request.args.get("elevation")
    startjd = request.args.get("startjd")
    stopjd = request.args.get("stopjd")
    stepjd = request.args.get("stepjd")
    min_altitude = request.args.get("min_altitude")
    max_altitude = request.args.get("max_altitude")
    data_source = request.args.get("data_source")

    # check for mandatory parameters
    if [
        x
        for x in (catalog, latitude, longitude, elevation, startjd, stopjd)
        if x is None
    ]:
        abort(400)

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
    try:
        location = EarthLocation(
            lat=float(latitude) * u.deg,
            lon=float(longitude) * u.deg,
            height=float(elevation) * u.m,
        )
    except Exception:
        abort(500, "Error: Invalid location parameters")

    try:
        min_altitude = float(min_altitude) if min_altitude is not None else None
        max_altitude = float(max_altitude) if max_altitude is not None else None
        if min_altitude is None:
            min_altitude = 0
        if max_altitude is None:
            max_altitude = 90
    except Exception:
        abort(500, "Error: Invalid parameter format")

    try:
        data_source = data_source.lower() if data_source is not None else None
        if data_source is None:
            data_source = "spacetrack"
        if data_source not in ["celestrak", "spacetrack"]:
            raise Exception
    except Exception:
        abort(500, "Error: Invalid data source")

    jd0 = float(startjd)
    jd1 = float(stopjd)

    jds = 0.00138889 if stepjd is None else float(stepjd)  # default to 2 min

    jd = jd_arange(jd0, jd1, jds)

    if len(jd) > 1000:
        app.logger.info("Too many results requested")
        abort(400)

    tle = get_tle(catalog, True, data_source, jd[0].to_datetime())
    return create_result_list(
        location,
        jd,
        tle[0].tle_line1,
        tle[0].tle_line2,
        tle[0].date_collected,
        tle[1].sat_name,
        min_altitude,
        max_altitude,
        tle[1].sat_number,
        data_source,
    )


@app.route("/ephemeris/tle/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_tle():
    """Returns satellite location and velocity information relative to the observer's
    coordinates for a given Two Line Element Data Set at the specified Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.

    Parameters
    ----------
    tle: 'str'
        Two line element set of object
    latitude: 'float'
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: 'float'
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: 'float'
        Elevation in meters
    julian_date: 'float'
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    min_altitude: 'float'
        Minimum satellite altitude in degrees
    max_altitude: 'float'
        Maximum satellite altitude in degrees

    Returns
    -------
    response: 'dictionary'
        JSON output with satellite information - see json_output() for format
    """
    tle = request.args.get("tle")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    elevation = request.args.get("elevation")
    julian_date = request.args.get("julian_date")
    min_altitude = request.args.get("min_altitude")
    max_altitude = request.args.get("max_altitude")

    # check for mandatory parameters
    if [x for x in (latitude, longitude, elevation, julian_date) if x is None]:
        abort(400)

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
    try:
        location = EarthLocation(
            lat=float(latitude) * u.deg,
            lon=float(longitude) * u.deg,
            height=float(elevation) * u.m,
        )
    except Exception:
        abort(500, "Error: Invalid location parameters")

    try:
        min_altitude = float(min_altitude) if min_altitude is not None else None
        max_altitude = float(max_altitude) if max_altitude is not None else None
        if min_altitude is None:
            min_altitude = 0
        if max_altitude is None:
            max_altitude = 90
    except Exception:
        abort(500, "Error: Invalid parameter format")

    # Converting string to list
    try:
        jd = Time(julian_date, format="jd", scale="ut1")
    except Exception:
        abort(500, "Error: Invalid Julian Date")

    tle = parse_tle(tle)
    return create_result_list(
        location,
        [jd],
        tle.tle_line1,
        tle.tle_line2,
        tle.date_collected,
        tle.name,
        min_altitude,
        max_altitude,
        tle.catalog,
        "user",
    )


@app.route("/ephemeris/tle-jdstep/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_ephemeris_by_tle_jdstep():
    """Returns satellite location and velocity information relative to the observer's
    coordinates for the given satellite's catalog number using the Two Line Element
    Data Set at a specified Julian Date.

    **Please note, for the most accurate results, a Julian Date close to the TLE epoch
    is necessary.

    Parameters
    ----------
    tle: 'str'
        Two line element set of object
    latitude: 'float'
        The observers latitude coordinate (positive value represents north,
        negative value represents south)
    longitude: 'float'
        The observers longitude coordinate (positive value represents east,
        negative value represents west)
    elevation: 'float'
        Elevation in meters
    startjd: 'float'
        UT1 Universal Time Julian Date to start ephmeris calculation.
    stopjd: 'float'
        UT1 Universal Time Julian Date to stop ephmeris calculation.
    stepjd: 'float'
        UT1 Universal Time Julian Date timestep.
    min_altitude: 'float'
        Minimum satellite altitude in degrees
    max_altitude: 'float'
        Maximum satellite altitude in degrees

    Returns
    -------
    response: 'dictionary'
        JSON output with satellite information - see json_output() for format
    """
    tle = request.args.get("tle")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    elevation = request.args.get("elevation")
    startjd = request.args.get("startjd")
    stopjd = request.args.get("stopjd")
    stepjd = request.args.get("stepjd")
    min_altitude = request.args.get("min_altitude")
    max_altitude = request.args.get("max_altitude")

    # check for mandatory parameters
    if [x for x in (latitude, longitude, elevation, startjd, stopjd) if x is None]:
        abort(400)

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
    try:
        location = EarthLocation(
            lat=float(latitude) * u.deg,
            lon=float(longitude) * u.deg,
            height=float(elevation) * u.m,
        )
    except Exception:
        abort(500, "Error: Invalid location parameters")

    try:
        min_altitude = float(min_altitude) if min_altitude is not None else None
        max_altitude = float(max_altitude) if max_altitude is not None else None
        if min_altitude is None:
            min_altitude = 0
        if max_altitude is None:
            max_altitude = 90
    except Exception:
        abort(500, "Error: Invalid parameter format")

    jd0 = float(startjd)
    jd1 = float(stopjd)

    jds = 0.00138889 if stepjd is None else float(stepjd)  # default to 2 min

    jd = jd_arange(jd0, jd1, jds)

    if len(jd) > 1000:
        app.logger.info("Too many results requested")
        abort(400)

    tle = parse_tle(tle)
    return create_result_list(
        location,
        jd,
        tle.tle_line1,
        tle.tle_line2,
        tle.date_collected,
        tle.name,
        min_altitude,
        max_altitude,
        tle.catalog,
        "user",
    )


### HELPER FUNCTIONS NOT EXPOSED TO API ###


def get_tle(identifier, use_catalog_number, data_source, date):
    tle_sat = (
        get_tle_by_catalog_number(identifier, data_source, date)
        if use_catalog_number
        else get_tle_by_name(identifier, data_source, date)
    )
    if not tle_sat:
        abort(500, "No TLE found")

    return tle_sat


def create_result_list(
    location,
    jd,
    tle_line_1,
    tle_line_2,
    date_collected,
    name,
    min_altitude,
    max_altitude,
    catalog_id="",
    data_source="",
):
    # propagation and create output
    result_list = []
    for d in jd:
        # Right ascension RA (deg), Declination Dec (deg), dRA/dt*cos(Dec) (deg/day),
        # dDec/dt (deg/day), Altitude (deg), Azimuth (deg), dAlt/dt (deg/day),
        # dAz/dt (deg/day), distance (km), range rate (km/s), phaseangle(deg),
        # illuminated (T/F)
        satellite_position = propagate_satellite(tle_line_1, tle_line_2, location, d)

        if (
            satellite_position.alt.degrees > min_altitude
            and satellite_position.alt.degrees < max_altitude
        ):
            result_list.append(
                json_output(
                    name,
                    catalog_id,
                    d.jd,
                    satellite_position.ra,
                    satellite_position.dec,
                    date_collected,
                    satellite_position.dracosdec,
                    satellite_position.ddec,
                    satellite_position.alt,
                    satellite_position.az,
                    satellite_position.distance,
                    satellite_position.ddistance,
                    satellite_position.phase_angle,
                    satellite_position.illuminated,
                    data_source,
                )
            )
    return result_list


def parse_tle(tle):
    # parse url encoded parameter to string to remove space encoding
    tle = tle.replace("%20", " ")

    # split string into three lines based on url encoded space character
    try:
        pattern = re.compile(r"\\n|\n")
        tle_data = pattern.split(tle)
    except Exception:
        abort(500, "Incorrect TLE format")

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
        abort(500, "Incorrect TLE format")

    catalog = tle_line_1[2:6]

    tle = namedtuple(
        "tle", ["tle_line1", "tle_line2", "date_collected", "name", "catalog"]
    )
    return tle(tle_line_1, tle_line_2, None, name, catalog)


def get_tle_by_name(target_name, data_source, date):
    """Query Two Line Element (orbital element) API and return TLE lines for propagation

    Paremeters:
    ------------
    target_name: 'str'
        Name of satellite as displayed in TLE file
    data_source: 'str'
        Original source of TLE data (celestrak or spacetrack)
    date: 'datetime'
        Date to query TLE data

    Returns
    -------
    tle_sat: 'TLE, Satellite'
        tuple with TLE and Satellite objects
    """
    # use the tle closest to the date given (at the same time or before)
    try:
        tle_sat = (
            db.session.query(models.TLE, models.Satellite)
            .filter_by(data_source=data_source)
            .join(models.Satellite, models.TLE.sat_id == models.Satellite.id)
            .filter_by(sat_name=target_name)
            .order_by(
                func.abs(
                    func.extract("epoch", models.TLE.date_collected)
                    - func.extract("epoch", date)
                )
            )
            .first()
        )
    except Exception as e:
        app.logger.error(e)
        return None

    return tle_sat


def get_tle_by_catalog_number(target_number, data_source, date):
    """Query Two Line Element (orbital element) API and return TLE lines for propagation

    Paremeters:
    ------------
    target_number: 'str'
        Catalog number of satellite as displayed in TLE file
    data_source: 'str'
        Original source of TLE data (celestrak or spacetrack)
    date: 'datetime'
        Date to query TLE data

    Returns
    -------
    tle_sat: 'TLE, Satellite'
        tuple with TLE and Satellite objects
    """
    # use the tle closest to the date given (at the same time or before)
    try:
        tle_sat = (
            db.session.query(models.TLE, models.Satellite)
            .filter_by(data_source=data_source)
            .join(models.Satellite, models.TLE.sat_id == models.Satellite.id)
            .filter_by(sat_number=target_number)
            .order_by(
                func.abs(
                    func.extract("epoch", models.TLE.date_collected)
                    - func.extract("epoch", date)
                )
            )
            .first()
        )
    except Exception as e:
        app.logger.error(e)
        return None

    return tle_sat


def propagate_satellite(tle_line_1, tle_line_2, location, jd, dtsec=1):
    """Use Skyfield (https://rhodesmill.org/skyfield/earth-satellites.html)
     to propagate satellite and observer states.

    Parameters
    ----------
    tle_line_1: 'str'
        TLE line 1
    tle_line_2: 'str'
         TLE line 2
    lat: 'float'
        The observer WGS84 latitude in degrees
    lon: 'float'
        The observers WGS84 longitude in degrees (positive value represents east,
        negative value represents west)
    elevation: 'float'
        The observer elevation above WGS84 ellipsoid in meters
    julian_date: 'float'
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    tleapi: 'str'
        base API for query

    Returns
    -------
    Right Ascension: 'float'
        The right ascension of the satellite relative to observer coordinates in ICRS
        reference frame in degrees. Range of response is [0,360)
    Declination: 'float'
        The declination of the satellite relative to observer coordinates in ICRS
        reference frame in degrees. Range of response is [-90,90]
    Altitude: 'float'
        The altitude of the satellite relative to observer coordinates in ICRS
        reference frame in degrees. Range of response is [0,90]
    Azimuth: 'float'
        The azimuth of the satellite relative to observer coordinates in ICRS reference
        frame in degrees. Range of response is [0,360)
    distance: 'float'
        Range from observer to object in km
    """
    # This is the skyfield implementation
    ts = load.timescale()
    satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)

    # Get current position and find topocentric ra and dec
    curr_pos = wgs84.latlon(
        location.lat.value, location.lon.value, location.height.value
    )
    # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
    # Use ts.ut1_jd instead of ts.from_astropy because from_astropy uses
    # astropy.Time.TT.jd instead of UT1
    if jd.jd == 0:
        t = ts.ut1_jd(satellite.model.jdsatepoch)
    else:
        t = ts.ut1_jd(jd.jd)

    difference = satellite - curr_pos
    topocentric = difference.at(t)
    topocentricn = topocentric.position.km / np.linalg.norm(topocentric.position.km)

    ra, dec, distance = topocentric.radec()
    alt, az, distance = topocentric.altaz()

    dtday = TimeDelta(1, format="sec")
    tplusdt = ts.ut1_jd((jd + dtday).jd)
    tminusdt = ts.ut1_jd((jd - dtday).jd)

    dtx2 = 2 * dtsec

    sat = satellite.at(t).position.km

    # satn = sat / np.linalg.norm(sat)
    # satpdt = satellite.at(tplusdt).position.km
    # satmdt = satellite.at(tminusdt).position.km
    # vsat = (satpdt - satmdt) / dtx2

    sattop = difference.at(t).position.km
    sattopr = np.linalg.norm(sattop)
    sattopn = sattop / sattopr
    sattoppdt = difference.at(tplusdt).position.km
    sattopmdt = difference.at(tminusdt).position.km

    ratoppdt, dectoppdt = icrf2radec(sattoppdt)
    ratopmdt, dectopmdt = icrf2radec(sattopmdt)

    vsattop = (sattoppdt - sattopmdt) / dtx2

    ddistance = np.dot(vsattop, sattopn)
    rxy = np.dot(sattop[0:2], sattop[0:2])
    dra = (sattop[1] * vsattop[0] - sattop[0] * vsattop[1]) / rxy
    ddec = vsattop[2] / np.sqrt(1 - sattopn[2] * sattopn[2])
    dracosdec = dra * np.cos(dec.radians)

    dra = (ratoppdt - ratopmdt) / dtx2
    ddec = (dectoppdt - dectopmdt) / dtx2
    dracosdec = dra * np.cos(dec.radians)

    # drav, ddecv = icrf2radec(vsattop / sattopr, unit_vector=True)
    # dracosdecv = drav * np.cos(dec.radians)

    eph = load("de430t.bsp")
    earth = eph["Earth"]
    sun = eph["Sun"]

    earthp = earth.at(t).position.km
    sunp = sun.at(t).position.km
    earthsun = sunp - earthp
    earthsunn = earthsun / np.linalg.norm(earthsun)
    satsun = sat - earthsun
    satsunn = satsun / np.linalg.norm(satsun)
    phase_angle = np.rad2deg(np.arccos(np.dot(satsunn, topocentricn)))

    # Is the satellite in Earth's Shadow?
    r_parallel = np.dot(sat, earthsunn) * earthsunn
    r_tangential = sat - r_parallel

    illuminated = True

    if np.linalg.norm(r_parallel) < 0:
        # rearthkm
        if np.linalg.norm(r_tangential) < 6370:
            # print(np.linalg.norm(r_tangential),np.linalg.norm(r))
            # yes the satellite is in Earth's shadow, no need to continue
            # (except for the moon of course)
            illuminated = False
    satellite_position = namedtuple(
        "satellite_position",
        [
            "ra",
            "dec",
            "dracosdec",
            "ddec",
            "alt",
            "az",
            "distance",
            "ddistance",
            "phase_angle",
            "illuminated",
        ],
    )
    return satellite_position(
        ra, dec, dracosdec, ddec, alt, az, distance, ddistance, phase_angle, illuminated
    )


def jd_arange(a, b, dr, decimals=11):
    """Better arange function that compensates for round-off errors.

    Parameters
    ----------
    a: 'float'
        first element in range
    b: 'float'
        last element in range
    dr: 'float'
        range increment
    decimals: 'integer'
        post comma digits to be rounded to

    Returns
    -------
    res: 'numpy array of floats'
        array of numbers between a and b with dr increments
    """
    res = [a]
    k = 1
    while res[-1] < b:
        tmp = np.round(a + k * dr, decimals)
        if tmp > b:
            break
        res.append(tmp)
        k += 1
    dates = np.asarray(res)

    try:
        results = Time(dates, format="jd", scale="ut1")
    except Exception:
        abort(500, "Error: Invalid Julian Date")

    return results


def tle_to_icrf_state(tle_line_1, tle_line_2, jd):
    # This is the skyfield implementation
    ts = load.timescale()
    satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)

    # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
    if jd == 0:
        t = ts.ut1_jd(satellite.model.jdsatepoch)
    else:
        t = ts.ut1_jd(jd.jd)

    r = satellite.at(t).position.km
    # print(satellite.at(t))
    v = satellite.at(t).velocity.km_per_s
    return np.concatenate(np.array([r, v]))


def json_output(
    name,
    catalog_id,
    time,
    ra,
    dec,
    date_collected,
    dracosdec,
    ddec,
    alt,
    az,
    # dalt, daz,
    r,
    dr,
    phaseangle,
    illuminated,
    data_source,
    precision_angles=11,
    precision_date=12,
    precision_range=12,
):
    """Convert API output to JSON format

    Parameters
    ----------
    name: 'str'
        Name of the target satellite
    time: 'float'
        Julian Date
    ra: Skyfield object / 'float'
        Right Ascension
    dec: Skyfield object / 'float'
        Declination
    alt: Skyfield object / 'float'
        Altitude
    az: Skyfield object / 'float'
        Azimuth
    r: Skyfield object / 'float'
        Range to target
    precision_angles: 'integer'
        number of digits for angles to be rounded to (default: micro arcsec)
    precision_date: 'integer'
        number of digits for Julian Date to be rounded to (default: micro sec)
    precision_range: 'integer'
        number of digits for angles to be rounded to (default: nano meters)

    Returns
    -------
    output: 'dictionary'
        JSON dictionary of the above quantities

    """
    # looking up the numpy round function once instead of multiple times
    # makes things a little faster
    my_round = np.round

    tle_date = (
        date_collected.strftime("%Y-%m-%d %H:%M:%S")
        if date_collected is not None
        else date_collected
    )

    output = {
        "NAME": name,
        "CATALOG_ID": catalog_id,
        "JULIAN_DATE": my_round(time, precision_date),
        "RIGHT_ASCENSION-DEG": my_round(ra._degrees, precision_angles),
        "DECLINATION-DEG": my_round(dec.degrees, precision_angles),
        "DRA_COSDEC-DEG_PER_SEC": my_round(dracosdec, precision_angles),
        "DDEC-DEG_PER_SEC": my_round(ddec, precision_angles),
        "ALTITUDE-DEG": my_round(alt.degrees, precision_angles),
        "AZIMUTH-DEG": my_round(az.degrees, precision_angles),
        "RANGE-KM": my_round(r.km, precision_range),
        "RANGE_RATE-KM_PER_SEC": my_round(dr, precision_range),
        "PHASE_ANGLE-DEG": my_round(phaseangle, precision_angles),
        "ILLUMINATED": illuminated,
        "TLE-DATE": tle_date,
        "DATA_SOURCE": data_source,
    }

    return output


def icrf2radec(pos, unit_vector=False, deg=True):
    """Convert ICRF xyz or xyz unit vector to Right Ascension and Declination.
    Geometric states on unit sphere, no light travel time/aberration correction.

    Parameters
    ----------
    pos ... real, dim=[n, 3], 3D vector of unit length (ICRF)
    unit_vector ... False: pos is unit vector, False: pos is not unit vector
    deg ... True: angles in degrees, False: angles in radians

    Returns
    -------
    ra ... Right Ascension [deg]
    dec ... Declination [deg]
    """
    norm = np.linalg.norm
    arctan2 = np.arctan2
    arcsin = np.arcsin
    rad2deg = np.rad2deg
    modulo = np.mod
    pix2 = 2.0 * np.pi

    r = 1
    if pos.ndim > 1:
        if not unit_vector:
            r = norm(pos, axis=1)
        xu = pos[:, 0] / r
        yu = pos[:, 1] / r
        zu = pos[:, 2] / r
    else:
        if not unit_vector:
            r = norm(pos)
        xu = pos[0] / r
        yu = pos[1] / r
        zu = pos[2] / r

    phi = arctan2(yu, xu)
    delta = arcsin(zu)

    if deg:
        ra = modulo(rad2deg(phi) + 360, 360)
        dec = rad2deg(delta)
    else:
        ra = modulo(phi + pix2, pix2)
        dec = delta

    return ra, dec


def get_forwarded_address(request):
    forwarded_header = request.headers.get("X-Forwarded-For")
    if forwarded_header:
        return request.headers.getlist("X-Forwarded-For")[0]
    return get_remote_address
