import datetime
import logging
import time
from typing import Tuple

import numpy as np
from astropy import units as u
from astropy.coordinates import (
    AltAz,
    EarthLocation,
    SkyCoord,
)
from astropy.time import Time
from celery import chord
from core import celery, utils
from core.database import models
from core.extensions import db
from core.propagation_strategies import (
    PropagationInfo,
    SGP4PropagationStrategy,
    SkyfieldPropagationStrategy,
    TestPropagationStrategy,
)
from flask import current_app
from sgp4.api import Satrec
from skyfield.api import EarthSatellite, load
from skyfield.framelib import itrs as sk_itrs
from skyfield.nutationlib import iau2000b
from skyfield.sgp4lib import TEME as sk_TEME  # noqa: N811
from sqlalchemy import and_, func
from utils.coordinate_systems import (
    az_el_to_ra_dec,
    ecef_to_enu,
    enu_to_az_el,
    teme_to_ecef,
)
from utils.time_utils import jd_to_gst

logger = logging.getLogger(__name__)


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
    # location_itrs = observer_location.itrs.cartesian.xyz.value / 1000
    target_altaz = c1.transform_to(
        AltAz(obstime=observer_time, location=observer_location)
    )

    for tle, sat in results:
        position = propagate_satellite_sgp4(
            tle.tle_line1, tle.tle_line2, 33, -117, 0, jd
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
    current_app.logger.info("process results started")
    # Filter out results that are not within the altitude range
    results = [result for result in tles if min_altitude <= result[4] <= max_altitude]
    api_source = "IAU CPS SatChecker"
    version = "0.4"

    if not results:
        return {
            "info": "No position information found with this criteria",
            "api_source": api_source,
            "version": version,
        }

    # Add remaining metadata to results
    data_set = utils.json_output(
        name, catalog_id, date_collected, data_source, results, api_source, version
    )

    current_app.logger.info("process results complete")
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
    # location_itrs = location.itrs.cartesian.xyz.value / 1000
    # Create a chord that will propagate the satellite for
    # each date and then process the results
    tasks = chord(
        (
            propagate_satellite_skyfield.s(
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
    if not results:
        return {"info": "No position information found with this criteria"}
    return results


@celery.task
def propagate_satellite_skyfield(tle_line_1, tle_line_2, lat, long, height, jd):
    """
    Propagates satellite and observer states using the Skyfield library.

    Args:
        tle_line_1 (str): The first line of the Two-Line Element set representing the satellite.
        tle_line_2 (str): The second line of the Two-Line Element set representing the satellite.
        lat (float): The latitude of the observer's location, in degrees.
        long (float): The longitude of the observer's location, in degrees.
        height (float): The height of the observer's location, in meters above the WGS84 ellipsoid.
        jd (Time): The Julian Date at which to propagate the satellite.

    Returns:
        dict: A dictionary containing the propagated state of the satellite and the
        observer.
    """  # noqa: E501
    propagation_info = PropagationInfo(
        SkyfieldPropagationStrategy(), tle_line_1, tle_line_2, jd, lat, long, height
    )
    return propagation_info.propagate()


# Only returns azimuth and altitude for quick calulations
@celery.task
def propagate_satellite_sgp4(tle_line_1, tle_line_2, lat, long, height, jd):
    """
    Propagates satellite and observer states using the SGP4 propagation library.

    Args:
        tle_line_1 (str): The first line of the Two-Line Element set representing the satellite.
        tle_line_2 (str): The second line of the Two-Line Element set representing the satellite.
        lat (float): The latitude of the observer's location, in degrees.
        long (float): The longitude of the observer's location, in degrees.
        height (float): The height of the observer's location, in meters above the WGS84 ellipsoid.
        jd (Time): The Julian Date at which to propagate the satellite.

    Returns:
        dict: A dictionary containing the propagated state of the satellite and the
        observer.
    """  # noqa: E501
    propagation_info = PropagationInfo(
        SGP4PropagationStrategy(), tle_line_1, tle_line_2, jd, lat, long, height
    )
    return propagation_info.propagate()


@celery.task
def propagate_satellite_new(tle_line_1, tle_line_2, lat, long, height, jd):
    """
    Propagates satellite and observer states using a test propagation strategy.

    Args:
        tle_line_1 (str): The first line of the Two-Line Element set representing the satellite.
        tle_line_2 (str): The second line of the Two-Line Element set representing the satellite.
        lat (float): The latitude of the observer's location, in degrees.
        long (float): The longitude of the observer's location, in degrees.
        height (float): The height of the observer's location, in meters above the WGS84 ellipsoid.
        jd (Time): The Julian Date at which to propagate the satellite.

    Returns:
        dict: A dictionary containing the propagated state of the satellite and the
        observer.
    """  # noqa: E501
    propagation_info = PropagationInfo(
        TestPropagationStrategy(), tle_line_1, tle_line_2, jd, lat, long, height
    )
    return propagation_info.propagate()
