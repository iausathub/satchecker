import datetime
import functools
import logging
import time
from collections import namedtuple
from typing import Tuple

import numpy as np
from astropy import units as u
from astropy.coordinates import (
    AltAz,
    EarthLocation,
    SkyCoord,
)
from astropy.time import Time, TimeDelta
from celery import chord
from flask import current_app
from sgp4.api import Satrec
from skyfield.api import EarthSatellite, load, wgs84
from skyfield.framelib import itrs as sk_itrs
from skyfield.nutationlib import iau2000b
from skyfield.sgp4lib import TEME as sk_TEME  # noqa: N811
from sqlalchemy import and_, func

from core import celery, utils
from core.database import models
from core.extensions import db

logger = logging.getLogger(__name__)


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


def jd_to_gst(jd: float, nutation: float) -> float:
    """
    Convert Julian Day (JD) to Greenwich Apparent Sidereal Time (GAST).

    This function calculates the GAST based on the JD and nutation.

    Args:
        jd (float): The Julian Day.
        nutation (float): The nutation in degrees.

    Returns:
        float: The GAST in radians.
    """
    # Approximate Delta T (in days)
    delta_t_days = 32.184 / (24 * 60 * 60)

    # Convert JD(UT) to JD(TT)
    jd_tt = jd + delta_t_days
    # Julian centuries since J2000.0
    t = (jd_tt - 2451545.0) / 36525.0

    # Greenwich Mean Sidereal Time (GMST) at 0h UT
    theta_gmst = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * t**2
        - t**3 / 38710000.0
    )

    # Wrap GMST to [0, 360) range
    theta_gmst = theta_gmst % 360

    # Convert nutation from arcseconds to degrees
    # nutation = nutation / 3600

    # Calculate Greenwich Apparent Sidereal Time (GAST)
    theta_gast = theta_gmst + nutation

    # Wrap GAST to [0, 360) range
    theta_gast = theta_gast % 360

    # Convert to radians
    theta_gast = np.deg2rad(theta_gast)

    return theta_gast


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


def calculate_lst(longitude: float, jd: float) -> float:
    """
    Calculate Local Sidereal Time (LST) based on longitude and Julian Day (JD).

    This function calculates the Greenwich Sidereal Time (GST) and then adjusts it
    based on the given longitude to calculate the LST.

    Args:
        longitude (float): The longitude in degrees.
        jd (float): The Julian Day.

    Returns:
        float: The LST in radians.
    """
    # Calculate the Julian centuries since J2000.0
    T = (jd - 2451545.0) / 36525.0  # noqa: N806

    # Calculate the GST in degrees
    gst = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * T**2
        - T**3 / 38710000.0
    )

    # Convert GST to range 0-360
    gst = gst % 360

    longitude = longitude * np.pi / 180.0  # Convert longitude to radians
    # Convert longitude to degrees
    longitude_deg = longitude * 180.0 / np.pi

    # Calculate LST in degrees
    lst_deg = gst + longitude_deg

    # Convert LST to range 0-360
    lst_deg = lst_deg % 360

    # Convert LST from degrees to radians
    lst = np.radians(lst_deg)

    return lst


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


@celery.task
def compare():
    # Two-line element set (TLE) for ISS
    tle_line_1 = "1 25544U 98067A   24087.50963912  .00035317  00000+0  63250-3 0  9993"
    tle_line_2 = "2 25544  51.6411   0.3077 0004676   8.9972 162.1343 15.49609731445878"

    # Observer's location
    lat = 33.0
    long = -117.0
    height = 0.0
    date = 2460402.32304

    # Create EarthLocation object for observer's location
    location = EarthLocation(lat=33.0 * u.deg, lon=-117.0 * u.deg, height=0.0 * u.m)
    location_itrs = location.itrs.cartesian.xyz.value / 1000.0

    # Load timescale and create time object
    ts = load.timescale()
    t = ts.ut1_jd(date)

    # Compute the x, y coordinates of the CIP (Celestial Intermediate Pole)
    dpsi, deps = iau2000b(date)

    # Compute the nutation in longitude
    nutation_arcsec = dpsi / 10000000  # Convert from arcseconds to degrees
    nutation = nutation_arcsec / 3600

    # Propagate satellite position
    satellite_position = propagate_satellite_skyfield(
        tle_line_1, tle_line_2, lat, long, height, date
    )

    # Calculate Greenwich Sidereal Time (GST)
    theta_gst = jd_to_gst(date, nutation)

    # Create satellite object from TLE
    satellite = Satrec.twoline2rv(tle_line_1, tle_line_2)

    # Calculate satellite position and velocity
    error, r, v = satellite.sgp4(date, 0)

    # Create EarthSatellite object
    satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)

    # Log satellite position
    current_app.logger.error(f"r: {r} ")  # ~20m is the issue
    current_app.logger.error(f"satellite - skyfield: {satellite.at(t).position.km} ")

    # Convert location from ITRS to AU
    AU_KM = 149597870.700  # noqa: N806
    location_itrs_au = location_itrs / AU_KM

    # new_r calculation makes the TEME vector match the one from skyfield,
    # but using this one results in even less correct results
    # Rotate location
    # ITRS to XYZ
    RT = np.rollaxis(sk_itrs.rotation_at(t), 1)  # noqa: N806
    r1 = np.dot(
        RT, location_itrs_au
    )  # np.einsum('ij...,j...->i...',RT, location_itrs_au)

    # Rotate satellite position from TEME to XYZ
    R = np.rollaxis(sk_TEME.rotation_at(t), 1)  # noqa: N806
    current_app.logger.error(f": {np} ")
    r2 = np.einsum("ij...,j...->i...", R, r)
    current_app.logger.error(f"R.T: {R.T} ")
    current_app.logger.error(f"R inverse: {np.linalg.inv(R)} ")
    current_app.logger.error(f"diff: {R.T - np.linalg.inv(R)} ")

    # Add rotated location and satellite position
    new_r = np.dot(R.T, r1 + r2)
    current_app.logger.error(f"new_r: {new_r} ")

    # Convert satellite position from TEME to ECEF
    r_ecef = teme_to_ecef(new_r, theta_gst)

    # Calculate difference between satellite position and observer's location
    difference = r_ecef - location_itrs
    current_app.logger.error(f"difference: {difference} ")

    # Convert difference from ECEF to ENU
    r_enu = ecef_to_enu(difference, lat, long)

    # Convert ENU coordinates to azimuth and elevation
    az, el = enu_to_az_el(r_enu)

    # Repeat the above steps for the original satellite position
    r_ecef = teme_to_ecef(r, theta_gst)
    difference = r_ecef - location_itrs
    current_app.logger.error(f"difference: {difference} ")
    r_enu = ecef_to_enu(difference, lat, long)
    az2, el2 = enu_to_az_el(r_enu)

    # Convert azimuth and elevation to right ascension and declination
    ra, dec = az_el_to_ra_dec(az, el, lat, long, date)
    ra2, dec2 = az_el_to_ra_dec(az2, el2, lat, long, date)

    # Log results
    current_app.logger.error(f"new ra: {ra} new dec: {dec}")
    current_app.logger.error(f"sgp only ra: {ra2} sgp dec: {dec2}")

    current_app.logger.error(f"new az: {az} new alt: {el}")
    current_app.logger.error(f"sgp only az: {az2} sgp alt: {el2}")
    current_app.logger.error(
        f"old az: {satellite_position.az} old alt: {satellite_position.alt}"
    )

    return "done"


@celery.task
def test_fov():

    # for each satellite in the database, propagate the satellite to
    # the current date/time using the most recent TLE
    # Define the target date
    target_date = datetime.datetime.now()
    started = time.time()
    try:
        subquery = (
            db.session.query(
                models.TLE.sat_id,
                func.min(
                    func.abs(
                        func.extract("epoch", models.TLE.date_collected)
                        - func.extract("epoch", target_date)
                    )
                ).label("min_difference"),
            )
            .group_by(models.TLE.sat_id)
            .subquery()
        )

        query = (
            db.session.query(models.TLE, models.Satellite)
            .filter_by(data_source="celestrak")
            .join(
                subquery,
                and_(
                    models.TLE.sat_id == subquery.c.sat_id,
                    func.abs(
                        func.extract("epoch", models.TLE.date_collected)
                        - func.extract("epoch", target_date)
                    )
                    == subquery.c.min_difference,
                ),
            )  # noqa: E501
            .join(models.Satellite, models.TLE.sat_id == models.Satellite.id)
        )

        results = query.all()
    except Exception:
        return None

    positions = []

    data = []
    jd = 2460402.61351  # Julian Date

    # get alt/az of center of FOV
    fov = [177.07062666895, 56.29124903308]  # ra/dec of center of FOV
    # in arcminutes
    radius = 30
    c1 = SkyCoord(ra=fov[0], dec=fov[1], unit="deg")
    # Define the time and location of the observer

    observer_location = EarthLocation(
        lat=33 * u.deg, lon=-117 * u.deg, height=0 * u.m
    )  # Replace with actual location
    observer_time = Time("2024-04-02T2:43:27", scale="utc")  # Replace with actual time
    location_itrs = observer_location.itrs.cartesian.xyz.value / 1000
    target_altaz = c1.transform_to(
        AltAz(obstime=observer_time, location=observer_location)
    )

    for tle, sat in results:
        position = propagate_satellite_sgp4(
            tle.tle_line1, tle.tle_line2, 33, -117, location_itrs, jd
        )

        if (
            position.alt > 0
            and position.alt < target_altaz.alt.deg + 2
            and position.alt > target_altaz.alt.deg - 2
        ):
            data.append((tle, sat.sat_name))

    for d in data:
        position = propagate_satellite_skyfield(
            d[0].tle_line1, d[0].tle_line2, 33, -117, 0, jd
        )
        c2 = SkyCoord(ra=position.ra, dec=position.dec, unit="deg")
        sep = c2.separation(c1).arcmin
        if sep <= radius:
            positions.append((position.ra, position.dec))
            current_app.logger.error(f"tle1: {d[0].tle_line1}")
            current_app.logger.error(f"sep: {sep}")
            current_app.logger.error(f"az: {position.az} alt: {position.alt}")

    elapsed = time.time() - started
    current_app.logger.error(f"Elapsed time: {elapsed}")
    current_app.logger.error(f"Objects: {len(positions)}")
    current_app.logger.error(f"Total checked: {len(data)}")
    current_app.logger.error(f"Total results: {len(results)}")
    current_app.logger.error(f"Center: {c1.ra.deg} {c1.dec.deg}")

    for p in positions:
        current_app.logger.error(f"ra: {p[0]} dec: {p[1]}")

    return positions


@celery.task
def process_results(
    tles: list[Tuple[float, float]],
    min_altitude: float,
    max_altitude: float,
    date_collected: str,
    name: str,
    catalog_id: str,
    data_source: str,
) -> list[utils.data_point]:
    """
    Process the results of the TLE data.

    This function filters the TLE data based on the altitude range and adds the
    remaining metadata to the results.

    Args:
        tles (list[Tuple[float, float]]): The TLE data.
        min_altitude (float): The minimum altitude.
        max_altitude (float): The maximum altitude.
        date_collected (str): The date the data was collected.
        name (str): The name of the satellite.
        catalog_id (str): The catalog ID of the satellite.
        data_source (str): The data source.

    Returns:
        list[utils.data_point]: The processed results.
    """
    current_app.logger.error("process results started")
    # Filter out results that are not within the altitude range
    results = [result for result in tles if min_altitude <= result[1] <= max_altitude]

    # Add remaining metadata to results
    data_set = []
    for result in results:
        data_set.append(
            utils.data_point(
                "0",
                "0",
                "0",
                "0",
                result[1],
                result[0],
                "0",
                "0",
                "0",
                "0",
                "0",
                date_collected,
                name,
                catalog_id,
                data_source,
            )
        )
    current_app.logger.error("process results complete")
    return data_set


@celery.task
def create_result_list(
    location: EarthLocation,
    dates: list[Time],
    tle_line_1: str,
    tle_line_2: str,
    date_collected: str,
    name: str,
    min_altitude: float,
    max_altitude: float,
    catalog_id: str = "",
    data_source: str = "",
) -> list[dict]:
    """
    Create a list of results for a given satellite and date range.

    This function propagates the satellite for each date in the given range, processes
    the results, and returns a list of results.

    Args:
        location (EarthLocation): The location of the observer.
        dates (list[Time]): The dates for which to propagate the satellite.
        tle_line_1 (str): The first line of the TLE data for the satellite.
        tle_line_2 (str): The second line of the TLE data for the satellite.
        date_collected (str): The date the TLE data was collected.
        name (str): The name of the satellite.
        min_altitude (float): The minimum altitude for the results.
        max_altitude (float): The maximum altitude for the results.
        catalog_id (str, optional): The catalog ID of the satellite. Defaults to "".
        data_source (str, optional): The data source of the TLE data. Defaults to "".

    Returns:
        list[dict]: A list of results for the given satellite and date range.
    """
    location_itrs = location.itrs.cartesian.xyz.value / 1000
    # Create a chord that will propagate the satellite for
    # each date and then process the results
    tasks = chord(
        (
            propagate_satellite_sgp4.s(
                tle_line_1,
                tle_line_2,
                location.lat.value,
                location.lon.value,
                location_itrs.tolist(),
                date.jd,
            )
            for date in dates
        ),
        process_results.s(
            min_altitude, max_altitude, date_collected, name, catalog_id, data_source
        ),
    )()
    results = tasks.get()
    return results


@functools.lru_cache(maxsize=128)
def calculate_current_position(lat, long, height):
    curr_pos = wgs84.latlon(lat, long, height)
    return curr_pos


ts = load.timescale()
eph = load("de430t.bsp")
earth = eph["Earth"]
sun = eph["Sun"]


@celery.task
def propagate_satellite_skyfield(tle_line_1, tle_line_2, lat, long, height, jd):
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
    eph = load("de430t.bsp")
    earth = eph["Earth"]
    sun = eph["Sun"]
    satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)
    # Get current position and find topocentric ra and dec
    curr_pos = calculate_current_position(lat, long, height)
    # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
    # Use ts.ut1_jd instead of ts.from_astropy because from_astropy uses
    # astropy.Time.TT.jd instead of UT1
    jd = Time(jd, format="jd", scale="ut1")
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

    # haven't had the need to change this but leaving it here for clarity purposes
    dtsec = 1
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

    earthp = earth.at(t).position.km
    sunp = sun.at(t).position.km
    # earthp, sunp = calculate_earth_sun(t)
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
            "jd",
        ],
    )
    return satellite_position(
        ra._degrees,
        dec.degrees,
        dracosdec,
        ddec,
        alt.degrees,
        az.degrees,
        distance.km,
        ddistance,
        phase_angle,
        illuminated,
        jd.jd,
    )


# Only returns azimuth and altitude for quick calulations
@celery.task
def propagate_satellite_sgp4(tle_line_1, tle_line_2, lat, long, location_itrs, jd):
    # new function
    # Compute the x, y coordinates of the CIP (Celestial Intermediate Pole)
    dpsi, deps = iau2000b(jd)

    # Compute the nutation in longitude
    nutation_arcsec = dpsi / 10000000  # Convert from arcseconds to degrees
    nutation = nutation_arcsec / 3600

    location_itrs = np.array(location_itrs)
    theta_gst = jd_to_gst(jd, nutation)

    satellite = Satrec.twoline2rv(tle_line_1, tle_line_2)
    error, r, v = satellite.sgp4(jd, 0)

    r_ecef = teme_to_ecef(r, theta_gst)
    difference = r_ecef - location_itrs
    r_enu = ecef_to_enu(difference, lat, long)
    az, el = enu_to_az_el(r_enu)
    ra, dec = az_el_to_ra_dec(az, el, lat, long, jd)

    return az, el, ra, dec


@celery.task
def propagate_satellite_new(tle_line_1, tle_line_2, lat, long, height, jd):
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
    eph = load("de430t.bsp")
    earth = eph["Earth"]
    sun = eph["Sun"]
    satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)
    # Get current position and find topocentric ra and dec
    curr_pos = calculate_current_position(lat, long, height)
    # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
    # Use ts.ut1_jd instead of ts.from_astropy because from_astropy uses
    # astropy.Time.TT.jd instead of UT1
    jd = Time(jd, format="jd", scale="ut1")
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

    # haven't had the need to change this but leaving it here for clarity purposes
    dtsec = 1
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

    earthp = earth.at(t).position.km
    sunp = sun.at(t).position.km
    # earthp, sunp = calculate_earth_sun(t)
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
            "jd",
        ],
    )
    return satellite_position(
        ra._degrees,
        dec.degrees,
        dracosdec,
        ddec,
        alt.degrees,
        az.degrees,
        distance.km,
        ddistance,
        phase_angle,
        illuminated,
        jd.jd,
    )


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
