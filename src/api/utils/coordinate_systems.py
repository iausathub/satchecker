import functools
import os
from pathlib import Path

import numpy as np
from astropy.config import set_temp_cache
from skyfield.api import EarthSatellite, load, wgs84
from skyfield.nutationlib import iau2000b
from skyfield.timelib import Time

from api.common import error_messages
from api.common.exceptions import ValidationError
from api.utils.time_utils import calculate_lst, jd_to_gst

# Configure Astropy to use a secure cache directory within the application
cache_dir = (
    Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    / "data"
    / "astropy_cache"
)
cache_dir.mkdir(parents=True, exist_ok=True)
set_temp_cache(cache_dir)


# TODO: Verify if teme_to_ecef is correct
# The results of this function in combination with the other coordinate system updates
# for SGP4 give results similar to, but not identical to, the Skyfield results, so each
# new conversion needs to be individually verified
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


# TODO: Verify if ecef_to_enu is correct
# The results of this function in combination with the other coordinate system updates
# for SGP4 give results similar to, but not identical to, the Skyfield results, so each
# new conversion needs to be individually verified
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


# TODO: Verify if ecef_to_itrs is correct/necessary
# Not sure if the flattening of the Earth is necessary or not - if not this
# function can be removed
def ecef_to_itrs(r_ecef):
    """
    Converts coordinates from Earth-Centered, Earth-Fixed (ECEF) to International
    Terrestrial Reference System (ITRS). The conversion takes into account the
    flattening of the Earth.

    Args:
        r_ecef (np.ndarray): A numpy array representing the coordinates in the
        ECEF system.

    Returns:
        np.ndarray: A numpy array representing the coordinates in the ITRS system.
    """
    # Convert ECEF to ITRS
    r_itrs = np.zeros_like(r_ecef)
    r_itrs[0] = r_ecef[0] / (1 + 1 / 298.257223563)  # a / (1 + 1 / f)
    r_itrs[1] = r_ecef[1]
    r_itrs[2] = r_ecef[2]
    return r_itrs


# TODO: Verify if itrs_to_gcrs is correct
# The results of this function in combination with the other coordinate system updates
# for SGP4 give results similar to, but not identical to, the Skyfield results, so each
# new conversion needs to be individually verified
def itrs_to_gcrs(r_itrs, julian_date):
    """
    Converts coordinates from the International Terrestrial Reference System (ITRS)
    to the Geocentric Celestial Reference System (GCRS).

    The conversion takes into account the nutation and the Greenwich Sidereal Time
    (GST) at the given Julian date.

    Args:
        r_itrs (np.ndarray): A numpy array representing the coordinates in the ITRS
                             system.
        julian_date (float): The Julian date at which to perform the conversion.

    Returns:
        np.ndarray: A numpy array representing the coordinates in the GCRS system.
    """
    # Convert ITRS to GCRS
    r_gcrs = np.zeros_like(r_itrs)
    dpsi, deps = iau2000b(julian_date)
    nutation_arcsec = dpsi / 10000000  # Convert from arcseconds to degrees
    nutation = nutation_arcsec / 3600
    theta_gst = jd_to_gst(julian_date, nutation)
    r_gcrs[0] = r_itrs[0] * np.cos(theta_gst) - r_itrs[1] * np.sin(theta_gst)
    r_gcrs[1] = r_itrs[0] * np.sin(theta_gst) + r_itrs[1] * np.cos(theta_gst)
    r_gcrs[2] = r_itrs[2]
    return r_gcrs


# TODO: Verify if enu_to_az_el is correct
# The results of this function in combination with the other coordinate system updates
# for SGP4 give results similar to, but not identical to, the Skyfield results, so each
# new conversion needs to be individually verified
def enu_to_az_el(r_enu: np.ndarray) -> tuple[float, float]:
    """
    Convert ENU (East, North, Up) coordinates to azimuth and elevation.

    This function calculates the azimuth and elevation based on the ENU coordinates.

    Args:
        r_enu (np.ndarray): The ENU coordinates.

    Returns:
        tuple[float, float]: The azimuth and elevation in degrees.
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


# TODO: Verify if ecef_to_eci is correct
# The results of this function in combination with the other coordinate system updates
# for SGP4 give results similar to, but not identical to, the Skyfield results, so each
# new conversion needs to be individually verified
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


# TODO: Verify if az_el_to_ra_dec is correct
# The results of this function in combination with the other coordinate system updates
# for SGP4 give results similar to, but not identical to, the Skyfield results, so each
# new conversion needs to be individually verified
def az_el_to_ra_dec(
    az: float, el: float, lat: float, lon: float, jd: float
) -> tuple[float, float]:
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
        tuple[float, float]: The right ascension and declination in degrees.
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

    r = 1.0
    if pos.ndim > 1:
        if not unit_vector:
            r = norm(pos, axis=1)
        xu = pos[:, 0] / r
        yu = pos[:, 1] / r
        zu = pos[:, 2] / r
    else:
        if not unit_vector:
            r = float(norm(pos))
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


def radec2icrf(ra, dec, deg=True):
    """Convert Right Ascension and Declination to ICRF xyz unit vector.
    Geometric states on unit sphere, no light travel time/aberration correction.
    Parameters:
    -----------
    ra ... Right Ascension [deg]
    dec ... Declination [deg]
    deg ... True: angles in degrees, False: angles in radians
    Returns:
    --------
    x,y,z ... 3D vector of unit length (ICRF)
    """
    if deg:
        a = np.deg2rad(ra)
        d = np.deg2rad(dec)
    else:
        a = np.array(ra)
        d = np.array(dec)
    cosd = np.cos(d)
    x = cosd * np.cos(a)
    y = cosd * np.sin(a)
    z = np.sin(d)
    return np.array([x, y, z])


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
        np.ndarray: A 1D array containing the ICRF position (in km) and velocity
        (in km/s) of the satellite.
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


def is_illuminated(sat_gcrs: np.ndarray, julian_date: float) -> bool:
    """
    Determines if a satellite is illuminated by the sun.

    This function calculates the angle between the satellite and the sun to determine if
    the satellite is illuminated.

    Parameters:
        sat_gcrs (np.ndarray): The position of the satellite in the GCRS frame.
        julian_date (float): The Julian date to check if the satellite is illuminated.

    Returns:
        bool: True if the satellite is illuminated, False otherwise.
    """
    earthp, sunp = get_earth_sun_positions(julian_date)
    earthsun = sunp - earthp
    earthsun_norm = earthsun / np.linalg.norm(earthsun)

    # Is the satellite in Earth's Shadow?
    r_parallel_length = np.dot(sat_gcrs, earthsun_norm)
    r_parallel = r_parallel_length * earthsun_norm
    r_tangential = sat_gcrs - r_parallel

    illuminated = True

    if np.linalg.norm(r_tangential) < 6370:
        illuminated = False

        if r_parallel_length > 0:
            illuminated = True

    return illuminated


def is_illuminated_vectorized(
    sat_gcrs_list: list[np.ndarray], julian_dates: list[float]
) -> list[bool]:
    """
    Vectorized version of is_illuminated that processes multiple satellite
    positions at once.

    This function batches the Earth-Sun position calculations and vectorizes
    the computations.

    Parameters:
        sat_gcrs_list (list[np.ndarray]): List of satellite positions in the GCRS frame.
        julian_dates (list[float]): List of Julian dates corresponding to each
        satellite position.

    Returns:
        list[bool]: List of illumination states for each satellite position.
    """
    if not sat_gcrs_list:
        return []

    if len(sat_gcrs_list) != len(julian_dates):
        raise ValueError("sat_gcrs_list and julian_dates must have the same length")

    # Convert to numpy arrays for vectorized operations
    sat_gcrs_array = np.array(sat_gcrs_list)
    julian_dates_array = np.array(julian_dates)

    # Get unique Julian dates to avoid redundant Earth-Sun calculations
    unique_jds, inverse_indices = np.unique(julian_dates_array, return_inverse=True)

    # Pre-calculate Earth-Sun positions for all unique dates
    earth_sun_positions = {}
    for jd in unique_jds:
        earthp, sunp = get_earth_sun_positions(jd)
        earthsun = sunp - earthp
        earthsun_norm = earthsun / np.linalg.norm(earthsun)
        earth_sun_positions[jd] = earthsun_norm

    illuminated_results = np.ones(len(sat_gcrs_list), dtype=bool)

    for jd in unique_jds:
        # Find all satellites at this Julian date
        mask = julian_dates_array == jd
        sat_positions = sat_gcrs_array[mask]

        if len(sat_positions) == 0:
            continue

        earthsun_norm = earth_sun_positions[jd]

        # Vectorized calculations for all satellites at this time
        r_parallel_lengths = np.dot(sat_positions, earthsun_norm)
        r_parallel = r_parallel_lengths[:, np.newaxis] * earthsun_norm
        r_tangential = sat_positions - r_parallel
        r_tangential_norms = np.linalg.norm(r_tangential, axis=1)

        in_shadow = r_tangential_norms < 6370

        # illuminated = not in_shadow OR (in_shadow AND r_parallel_length > 0)
        illuminated_at_this_time = ~in_shadow | (in_shadow & (r_parallel_lengths > 0))

        illuminated_results[mask] = illuminated_at_this_time

    return illuminated_results.tolist()


@functools.cache
def load_earth_sun() -> tuple:
    """
    Loads the Earth and Sun ephemeris data from the DE430t.bsp file.

    This function uses the Skyfield library to load the ephemeris data for Earth and Sun
    from the DE430t.bsp file. The loaded data is cached to improve performance on
    subsequent calls.

    Returns:
        tuple: A tuple containing the Earth and Sun objects from the ephemeris data.
    """
    eph = load("de430t.bsp")
    earth = eph["Earth"]
    sun = eph["Sun"]
    return earth, sun


@functools.lru_cache(maxsize=128)
def get_earth_sun_positions(t: float | Time) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the positions of Earth and Sun at a given time.

    This function uses Skyfield to get the positions of Earth and Sun
    in kilometers at a specified time.
    The time can be provided either as a float representing Julian date or as a Skyfield
    Time object.
    The results are cached to improve performance on subsequent calls.

    Args:
        t (float | Time): The time at which to compute the positions. Can be a float
                          representing Julian date or a Skyfield Time object.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing two numpy arrays representing
                                       the positions of Earth and Sun in kilometers.
    """
    if not isinstance(t, Time):
        ts = load.timescale()
        time = ts.ut1_jd(t)
    else:
        time = t

    earth, sun = load_earth_sun()
    earthp = earth.at(time).position.km
    sunp = sun.at(time).position.km
    return earthp, sunp


def get_phase_angle(
    topocentric_gcrs_norm: np.ndarray, sat_gcrs: np.ndarray, julian_date: float
) -> float:
    """
    Computes the phase angle between a satellite and the Sun as seen from Earth.

    This function calculates the phase angle, which is the angle between the vector
    from the satelliteto the Sun and the vector from the satellite to the Earth.
    The phase angle is useful in determining the illumination of the satellite.

    Args:
        topocentric_gcrs_norm (np.ndarray): Normalized vector representing the
                                          topocentric position in GCRS coordinates.
        sat_gcrs (np.ndarray): Vector representing the satellite's position in
                             GCRS coordinates.
        julian_date (float): The Julian date at which to compute the phase angle.

    Returns:
        float: The phase angle in degrees
    """
    earthp, sunp = get_earth_sun_positions(julian_date)
    earthsun = sunp - earthp

    satsun = sat_gcrs - earthsun
    satsunn = satsun / np.linalg.norm(satsun)

    phase_angle = float(np.rad2deg(np.arccos(np.dot(satsunn, topocentric_gcrs_norm))))
    return phase_angle


def calculate_satellite_observer_relative(
    satellite_position_gcrs: np.ndarray,
    observer_latitude: float,
    observer_longitude: float,
    observer_elevation: float,
    julian_date: float,
) -> tuple[float, float, float]:
    """
    Calculate satellite altitude, azimuth, and range relative to observer
    without using Skyfield.

    Args:
        satellite_position_gcrs: Satellite position in GCRS coordinates (km)
        observer_latitude: Observer latitude in degrees
        observer_longitude: Observer longitude in degrees
        observer_elevation: Observer elevation in meters
        julian_date: Julian date

    Returns:
        tuple: (altitude_deg, azimuth_deg, range_km)
    """
    # WGS84 ellipsoid parameters for observer position calculation
    a = 6378.137  # Semi-major axis in km
    f = 1 / 298.257223563  # Flattening
    e2 = 2 * f - f * f  # First eccentricity squared

    # Convert to radians
    lat_rad = np.deg2rad(observer_latitude)
    lon_rad = np.deg2rad(observer_longitude)
    h = observer_elevation / 1000.0  # Convert to km

    # Calculate N (radius of curvature in the prime vertical)
    N = a / np.sqrt(1 - e2 * np.sin(lat_rad) ** 2)  # noqa: N806

    # Calculate observer position in ECEF
    observer_ecef = np.array(
        [
            (N + h) * np.cos(lat_rad) * np.cos(lon_rad),
            (N + h) * np.cos(lat_rad) * np.sin(lon_rad),
            (N * (1 - e2) + h) * np.sin(lat_rad),
        ]
    )

    # Convert satellite position from GCRS to ECEF using reverse of itrs_to_gcrs
    # This includes nutation corrections for better accuracy
    dpsi, deps = iau2000b(julian_date)
    nutation_arcsec = dpsi / 10000000  # Convert from arcseconds to degrees
    nutation = nutation_arcsec / 3600
    theta_gst = jd_to_gst(julian_date, nutation)

    # Reverse the itrs_to_gcrs transformation
    satellite_ecef = np.zeros_like(satellite_position_gcrs)
    satellite_ecef[0] = satellite_position_gcrs[0] * np.cos(
        theta_gst
    ) + satellite_position_gcrs[1] * np.sin(theta_gst)
    satellite_ecef[1] = -satellite_position_gcrs[0] * np.sin(
        theta_gst
    ) + satellite_position_gcrs[1] * np.cos(theta_gst)
    satellite_ecef[2] = satellite_position_gcrs[2]

    # Calculate relative position (satellite - observer)
    relative_position_ecef = satellite_ecef - observer_ecef

    # Use the existing ecef_to_enu function
    relative_position_enu = ecef_to_enu(
        relative_position_ecef, observer_latitude, observer_longitude
    )

    # Use the existing enu_to_az_el function
    azimuth_deg, altitude_deg = enu_to_az_el(relative_position_enu)

    # Calculate range
    range_km = np.linalg.norm(relative_position_enu)

    return altitude_deg, azimuth_deg, range_km
