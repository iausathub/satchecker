import logging
from collections import namedtuple

import numpy as np
from astropy.time import Time, TimeDelta
from celery import chord
from skyfield.api import EarthSatellite, load, wgs84

from core import celery, utils

logger = logging.getLogger(__name__)


@celery.task
def process_results(
    results, min_altitude, max_altitude, date_collected, name, catalog_id, data_source
):
    # Filter out results that are not within the altitude range
    results = [
        result for result in results if min_altitude <= result[4] <= max_altitude
    ]

    # Add remaining metadata to results
    data_set = []
    for result in results:
        data_set.append(
            utils.data_point(
                result[0],
                result[1],
                result[2],
                result[3],
                result[4],
                result[5],
                result[6],
                result[7],
                result[8],
                result[9],
                result[10],
                date_collected,
                name,
                catalog_id,
                data_source,
            )
        )
    return data_set


@celery.task
def create_result_list(
    location,
    dates,
    tle_line_1,
    tle_line_2,
    date_collected,
    name,
    min_altitude,
    max_altitude,
    catalog_id="",
    data_source="",
):
    # Create a chord that will propagate the satellite for
    # each date and then process the results
    tasks = chord(
        (
            propagate_satellite.s(
                tle_line_1,
                tle_line_2,
                location.lat.value,
                location.lon.value,
                location.height.value,
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


@celery.task
def propagate_satellite(tle_line_1, tle_line_2, lat, long, height, jd):
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
    curr_pos = wgs84.latlon(lat, long, height)
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
