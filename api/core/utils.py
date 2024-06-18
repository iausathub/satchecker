import functools
import json
import os
from collections import namedtuple

import astropy.units as u
import boto3
import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time, TimeDelta
from flask import abort
from flask_limiter.util import get_remote_address
from skyfield.api import EarthSatellite, load, wgs84

INVALID_JD = "Error: Invalid Julian Date"
INVALID_PARAMETER = "Error: Invalid parameter format"
NO_TLE_FOUND = "Error: No TLE found"


def get_forwarded_address(request):
    """
    Retrieves the original IP address from the 'X-Forwarded-For' header of a
    HTTP request.

    This is needed due to the way the app is deployed with Docker. If the
    'X-Forwarded-For' header is not present, it falls back to the remote
    address of the request.

    Args:
        request (werkzeug.local.LocalProxy): The HTTP request object.

    Returns:
        str: The original client IP address, or the remote address of the request if the
             'X-Forwarded-For' header is not present.
    """
    forwarded_header = request.headers.get("X-Forwarded-For")
    if forwarded_header:
        return request.headers.getlist("X-Forwarded-For")[0]
    return get_remote_address


def get_db_login():
    """
    Retrieves database login credentials from environment variables or AWS Secrets
    Manager.

    This function first checks if the 'LOCAL_DB' environment variable is set to '1'.
     If it is, it returns a predefined set of local database credentials.

    If 'LOCAL_DB' is not set to '1', it then checks if the 'DB_HOST' environment
    variable is set. If it is, it returns the database credentials from the
    'DB_USERNAME', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', and 'DB_NAME'
    environment variables.

    If neither 'LOCAL_DB' nor 'DB_HOST' are set, it attempts to retrieve the database
    credentials from AWS Secrets Manager. If it fails to retrieve the credentials
    from Secrets Manager, it falls back to the predefined local database credentials.

    Returns:
        list: A list containing the username, password, host, port, and database name,
        in that order.
    """
    if os.environ.get("LOCAL_DB") == "1":
        username, password, host, port, dbname = (
            "postgres",
            "postgres",
            "localhost",
            "5432",
            "satchecker_test",
        )
        return [username, password, host, port, dbname]

    if os.environ.get("DB_HOST") is not None:
        username, password, host, port, dbname = (
            os.environ.get("DB_USERNAME"),
            os.environ.get("DB_PASSWORD"),
            os.environ.get("DB_HOST"),
            os.environ.get("DB_PORT"),
            os.environ.get("DB_NAME"),
        )
        return [username, password, host, port, dbname]

    secret_name = "satchecker-prod-db-cred"  # noqa: S105
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    get_secret_value_response = None
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        username, password, host, port, dbname = (
            "postgres",
            "postgres",
            "localhost",
            "5432",
            "satchecker_test",
        )
        return [username, password, host, port, dbname]

    if get_secret_value_response is None:
        raise RuntimeError("No secret value response")

    secrets = json.loads(get_secret_value_response["SecretString"])
    # Decrypts secret using the associated KMS key.
    username = secrets["username"]
    password = secrets["password"]
    host = secrets["host"]
    port = secrets["port"]
    dbname = secrets["dbname"]

    return [username, password, host, port, dbname]


data_point = namedtuple(
    "data_point",
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
        "jd",
        "date_collected",
        "name",
        "catalog_id",
        "data_source",
    ],
)


def tle_to_icrf_state(tle_line_1, tle_line_2, jd):
    """
    Converts Two-Line Element (TLE) set to International Celestial Reference Frame
    (ICRF) state.

    This function uses the Skyfield library to convert a TLE set into a state vector in
    the ICRF. The state vector includes the position and velocity of the satellite.

    Parameters:
        tle_line_1 (str): The first line of the TLE set.
        tle_line_2 (str): The second line of the TLE set.
        jd (float or astropy.time.core.Time): The Julian date at which to calculate the
            state. If 0, the function will use the epoch specified in the TLE set.

    Returns:
        np.array: A 1D array containing the ICRF position (in km) and velocity (in km/s)
            of the satellite.
    """
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


def icrf2radec(pos, unit_vector=False, deg=True):
    """
    Convert ICRF xyz or xyz unit vector to Right Ascension and Declination.
    Geometric states on unit sphere, no light travel time/aberration correction.

    Parameters
    ----------
    pos : numpy.ndarray
        A 3D vector of unit length in the ICRF frame. If `unit_vector` is False,
        `pos` is assumed to be a position vector and will be normalized. If `unit_vector`
        is True, `pos` is assumed to already be a unit vector. The shape should be [n, 3].
    unit_vector : bool, optional
        If True, `pos` is assumed to be a unit vector. If False, `pos` is assumed to be a
        position vector and will be normalized. Default is False.
    deg : bool, optional
        If True, the angles are returned in degrees. If False, the angles are returned in
        radians. Default is True.

    Returns
    -------
    ra : numpy.ndarray
        The Right Ascension of the position, in degrees if `deg` is True, or in radians if
        `deg` is False. If `pos` was a 2D array, this will be a 1D array of the same length.
    dec : numpy.ndarray
        The Declination of the position, in degrees if `deg` is True, or in radians if `deg`
        is False. If `pos` was a 2D array, this will be a 1D array of the same length.
    """  # noqa: E501

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


def json_output(
    name,
    catalog_id,
    date_collected,
    data_source,
    results,
    api_source,
    version,
    precision_angles=8,
    precision_date=8,
    precision_range=6,
    precision_velocity=12,
):
    """
    Convert API output to JSON format

    Parameters
    ----------
    name: str
        Name of the target satellite
    catalog_id: str
        Catalog ID of the satellite
    date_collected: datetime
        Date when the data was collected
    data_source: str
        Source of the data
    results: list
        List of results from the API
    api_source: str
        Source of the API
    version: str
        Version of the API
    precision_angles: int, optional
        Number of digits for angles to be rounded to (default: 8)
    precision_date: int, optional
        Number of digits for Julian Date to be rounded to (default: 8)
    precision_range: int, optional
        Number of digits for range to be rounded to (default: 6)
    precision_velocity: int, optional
        Number of digits for velocity to be rounded to (default: 12)

    Returns
    -------
    dict
        JSON dictionary of the above quantities
    """
    # looking up the numpy round function once instead of multiple times
    # makes things a little faster
    my_round = np.round

    tle_date = (
        date_collected.strftime("%Y-%m-%d %H:%M:%S %Z")
        if date_collected is not None
        else date_collected
    )

    fields = [
        "name",
        "catalog_id",
        "satellite_gcrs_km",
        "right_ascension_deg",
        "declination_deg",
        "tle_date",
        "dra_cosdec_deg_per_sec",
        "ddec_deg_per_sec",
        "altitude_deg",
        "azimuth_deg",
        "range_km",
        "range_rate_km_per_sec",
        "phase_angle_deg",
        "illuminated",
        "data_source",
        "observer_gcrs_km",
    ]
    data = []
    for result in results:
        (
            ra,
            dec,
            dracosdec,
            ddec,
            alt,
            az,
            r,
            dr,
            phaseangle,
            illuminated,
            satellite_gcrs,
            observer_gcrs,
            time,
        ) = result  # noqa: E501
        data.append(
            [
                name,
                int(catalog_id),
                my_round(time, precision_date),
                satellite_gcrs,
                my_round(ra, precision_angles),
                my_round(dec, precision_angles),
                tle_date,
                my_round(dracosdec, precision_angles),
                my_round(ddec, precision_angles),
                my_round(alt, precision_angles),
                my_round(az, precision_angles),
                my_round(r, precision_range),
                my_round(dr, precision_velocity),
                my_round(phaseangle, precision_angles),
                illuminated,
                data_source,
                observer_gcrs,
            ]
        )

    return {
        "count": len(results),
        "fields": fields,
        "data": data,
        "source": api_source,
        "version": version,
    }


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
        abort(500, INVALID_JD)

    return results


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


def validate_parameters(parameters, required_parameters):
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
    for param in required_parameters:
        if param not in parameters.keys() or parameters[param] is None:
            abort(400, f"Missing parameter: {param}")

    # Cast the latitude, longitude, and jd to floats (request parses as a string)
    try:
        parameters["location"] = EarthLocation(
            lat=float(parameters["latitude"]) * u.deg,
            lon=float(parameters["longitude"]) * u.deg,
            height=float(parameters["elevation"]) * u.m,
        )
    except Exception:
        abort(500, "Invalid location")

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
        abort(500, INVALID_PARAMETER)

    if "data_source" in parameters.keys():
        parameters["data_source"] = (
            parameters["data_source"].lower()
            if parameters["data_source"] is not None
            else "any"
        )
        if parameters["data_source"] not in ["celestrak", "spacetrack", "any"]:
            abort(500, "Invalid data source")

    return parameters


def propagate_satellite(tle_line_1, tle_line_2, location, jd, dtsec=1):
    """
    Propagates satellite and observer states using the Skyfield library.

    Parameters
    ----------
    tle_line_1: str
        The first line of the Two-Line Element set representing the satellite.
    tle_line_2: str
        The second line of the Two-Line Element set representing the satellite.
    location: Topos
        The observer's location, represented as a Topos object.
    jd: Time
        The Julian Date at which to propagate the satellite. If the Julian Date is 0,
        the function uses the epoch from the TLE.
    dtsec: int, optional
        The time step for the propagation, in seconds. Default is 1.

    Returns
    -------
    satellite_position: namedtuple
        A namedtuple with the following fields:

        - ra: The right ascension of the satellite relative to the observer, in degrees.

        - dec: The declination of the satellite relative to the observer, in degrees.

        - dracosdec: The rate of change of right ascension, in degrees per second.

        - ddec: The rate of change of declination, in degrees per second.

        - alt: The altitude of the satellite relative to the observer, in degrees.

        - az: The azimuth of the satellite relative to the observer, in degrees.

        - distance: The distance from the observer to the satellite, in kilometers.

        - ddistance: The rate of change of the distance, in kilometers per second.

        - phase_angle: The phase angle of the satellite, in degrees.

        - illuminated: A boolean indicating whether the satellite is illuminated by the Sun.

        - satellite_gcrs: The position of the satellite in the Geocentric Celestial Reference System, in kilometers.

        - observer_gcrs: The position of the observer in the Geocentric Celestial Reference System, in kilometers.

    """  # noqa: E501

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

    sat_gcrs = satellite.at(t).position.km

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
    satsun = sat_gcrs - earthsun
    satsunn = satsun / np.linalg.norm(satsun)
    phase_angle = np.rad2deg(np.arccos(np.dot(satsunn, topocentricn)))

    # Is the satellite in Earth's Shadow?
    r_parallel = np.dot(sat_gcrs, earthsunn) * earthsunn
    r_tangential = sat_gcrs - r_parallel

    illuminated = True

    obs_gcrs = curr_pos.at(t).position.km

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
            "satellite_gcrs",
            "observer_gcrs",
        ],
    )
    return satellite_position(
        ra,
        dec,
        dracosdec,
        ddec,
        alt,
        az,
        distance,
        ddistance,
        phase_angle,
        illuminated,
        sat_gcrs,
        obs_gcrs,
    )


@functools.lru_cache(maxsize=128)
def calculate_current_position(lat, long, height):
    """
    Calculates the current position in the WGS84 reference frame.

    This function uses the WGS84 model to calculate the current position based on the
    given latitude, longitude, and height.
    The result is cached for faster subsequent calls with the same arguments.

    Args:
        lat (float): The latitude in degrees.
        long (float): The longitude in degrees.
        height (float): The height in meters above the WGS84 ellipsoid.

    Returns:
        Topos: A Topos object representing the current position.
    """
    curr_pos = wgs84.latlon(lat, long, height)
    return curr_pos
