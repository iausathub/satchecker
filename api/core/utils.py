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
    forwarded_header = request.headers.get("X-Forwarded-For")
    if forwarded_header:
        return request.headers.getlist("X-Forwarded-For")[0]
    return get_remote_address


def get_db_login():
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
    np.array: A 1D array containing the ICRF position (in km) and velocity (in km/s) of
    the satellite.
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
    satellite_gcrs,
    observer_gcrs,
    precision_angles=8,
    precision_date=8,
    precision_range=6,
    precision_velocity=12,
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
        date_collected.strftime("%Y-%m-%d %H:%M:%S %Z")
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
        "RANGE_RATE-KM_PER_SEC": my_round(dr, precision_velocity),
        "PHASE_ANGLE-DEG": my_round(phaseangle, precision_angles),
        "ILLUMINATED": illuminated,
        "TLE_DATE": tle_date,
        "DATA_SOURCE": data_source,
        "SATELLITE_GCRS-KM": satellite_gcrs.tolist(),
        "OBSERVER_GCRS-KM": observer_gcrs.tolist(),
    }

    return output


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
    """
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
            else "spacetrack"
        )
        if parameters["data_source"] not in ["celestrak", "spacetrack"]:
            abort(500, "Invalid data source")

    return parameters


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
