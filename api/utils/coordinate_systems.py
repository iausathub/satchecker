from typing import Tuple

import numpy as np
from utils.time_utils import calculate_lst


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
