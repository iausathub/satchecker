import functools
from typing import Tuple  # noqa: I001

import numpy as np
from api.common import error_messages
from api.common.exceptions import ValidationError
from api.utils.time_utils import calculate_lst
from skyfield.api import EarthSatellite, load, wgs84


def teme_to_ecef(r_teme: list[float], theta_gst: float) -> np.ndarray:
    """
    Convert TEME (True Equator, Mean Equinox) coordinates to ECEF (Earth-Centered,
    Earth-Fixed) coordinates.

    This function applies a rotation matrix to transform the coordinates from the
    TEME frame to the ECEF frame.

    Args:
        r_teme (list[float]): The TEME coordinates.
        theta_gst (float): The Greenwich Sidereal Time angle.

    Returns:
        np.ndarray: The ECEF coordinates.
    """
    # Rotation matrix from TEME to ECEF
    R = np.array(  # noqa: N806
        [
            [np.cos(theta_gst), np.sin(theta_gst), 0],
            [-np.sin(theta_gst), np.cos(theta_gst), 0],
            [0, 0, 1],
        ]
    )

    # Convert TEME to ECEF
    r_ecef = R @ r_teme

    return r_ecef


def ecef_to_enu(r_ecef: list[float], lat: float, lon: float) -> np.ndarray:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) coordinates to ENU (East, North, Up)
    coordinates.

    This function applies a rotation matrix to transform the coordinates from the
    ECEF frame to the ENU frame.

    Args:
        r_ecef (list[float]): The ECEF coordinates.
        lat (float): The latitude of the location.
        lon (float): The longitude of the location.

    Returns:
        np.ndarray: The ENU coordinates.
    """
    # Convert to radians
    lat = np.deg2rad(lat)
    lon = np.deg2rad(lon)

    # Rotation matrix from ECEF to ENU
    R = np.array(  # noqa: N806
        [
            [-np.sin(lon), np.cos(lon), 0],
            [-np.sin(lat) * np.cos(lon), -np.sin(lat) * np.sin(lon), np.cos(lat)],
            [np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)],
        ]
    )

    # Convert ECEF to ENU
    r_enu = R @ r_ecef

    return r_enu


def enu_to_az_el(r_enu: np.ndarray) -> Tuple[float, float]:
    """
    Convert ENU (East, North, Up) coordinates to azimuth and elevation.

    This function calculates the azimuth and elevation based on the ENU coordinates.

    Args:
        r_enu (np.ndarray): The ENU coordinates.

    Returns:
        Tuple[float, float]: The azimuth and elevation in degrees.
    """
    # Calculate horizontal distance
    p = np.hypot(r_enu[0], r_enu[1])

    # Calculate azimuth
    az = np.arctan2(r_enu[0], r_enu[1])

    # Calculate elevation
    el = np.arctan2(r_enu[2], p)

    # Convert azimuth from [-pi, pi] to [0, 2*pi]
    if az < 0:
        az += 2 * np.pi

    return np.rad2deg(az), np.rad2deg(el)


def ecef_to_eci(r_ecef: list[float], theta_gst: float) -> np.ndarray:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) coordinates to ECI (Earth-Centered
    Inertial) coordinates.

    This function applies a rotation matrix to transform the coordinates from the ECEF
    frame to the ECI frame.

    Args:
        r_ecef (list[float]): The ECEF coordinates.
        theta_gst (float): The Greenwich Sidereal Time angle in degrees.

    Returns:
        np.ndarray: The ECI coordinates.
    """
    # Convert GST from degrees to radians
    theta_gst_rad = np.deg2rad(theta_gst)

    # Rotation matrix
    R = np.array(  # noqa: N806
        [
            [np.cos(theta_gst_rad), np.sin(theta_gst_rad), 0],
            [-np.sin(theta_gst_rad), np.cos(theta_gst_rad), 0],
            [0, 0, 1],
        ]
    )

    # Convert from ECEF to ECI
    r_eci = R @ r_ecef

    return r_eci


def az_el_to_ra_dec(
    az: float, el: float, lat: float, lon: float, jd: float
) -> Tuple[float, float]:
    """
    Convert azimuth and elevation to right ascension and declination.

    This function calculates the right ascension and declination based on the azimuth,
    elevation, latitude, longitude, and Julian Day.

    Args:
        az (float): The azimuth in degrees.
        el (float): The elevation in degrees.
        lat (float): The latitude in degrees.
        lon (float): The longitude in degrees.
        jd (float): The Julian Day.

    Returns:
        Tuple[float, float]: The right ascension and declination in degrees.
    """
    lst = calculate_lst(lon, jd)
    # Convert to radians
    az = np.deg2rad(az)
    el = np.deg2rad(el)
    lat = np.deg2rad(lat)

    # Calculate declination
    dec = np.arcsin(np.sin(el) * np.sin(lat) + np.cos(el) * np.cos(lat) * np.cos(az))

    # Calculate hour angle
    ha = np.arccos(
        (np.sin(el) - np.sin(lat) * np.sin(dec)) / (np.cos(lat) * np.cos(dec))
    )

    # Convert hour angle to right ascension
    ra = lst - ha

    # Convert to degrees
    ra = np.rad2deg(ra) % 360
    dec = np.rad2deg(dec)

    return ra, dec


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

    tle_line_1 = tle_line_1.strip().replace("%20", " ")
    tle_line_2 = tle_line_2.strip().replace("%20", " ")

    if (len(tle_line_1) != 69) or (len(tle_line_2) != 69):
        raise ValidationError(500, error_messages.INVALID_TLE)

    # This is the skyfield implementation
    ts = load.timescale()
    satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)

    # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
    if jd == 0:
        t = ts.ut1_jd(satellite.model.jdsatepoch)
    else:
        t = ts.ut1_jd(jd.jd)

    r = satellite.at(t).position.km
    v = satellite.at(t).velocity.km_per_s

    return np.concatenate(np.array([r, v]))


def is_illuminated(sat_gcrs: np.array, earthsun_norm: np.array) -> bool:
    """
    Determines if a satellite is illuminated by the sun.

    This function calculates the angle between the satellite and the sun to determine if
    the satellite is illuminated.

    Parameters:
        sat_gcrs (np.array): The position of the satellite in the GCRS frame.
        earthsun_norm (np.array): The normalized vector pointing from the Earth to the
        Sun.

    Returns:
        bool: True if the satellite is illuminated, False otherwise.
    """
    # Is the satellite in Earth's Shadow?
    r_parallel = np.dot(sat_gcrs, earthsun_norm) * earthsun_norm
    r_tangential = sat_gcrs - r_parallel
    illuminated = True

    if np.linalg.norm(r_parallel) < 0:
        # rearthkm
        if np.linalg.norm(r_tangential) < 6370:
            # print(np.linalg.norm(r_tangential),np.linalg.norm(r))
            # yes the satellite is in Earth's shadow, no need to continue
            # (except for the moon of course)
            illuminated = False

    return illuminated
