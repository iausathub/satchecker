import re
from collections import namedtuple

from flask import abort
from sqlalchemy import func

from ..extensions import db
from ..utils import json_output, propagate_satellite
from . import models

NO_TLE_FOUND = "Error: No TLE found"


def propagate_and_create_json_results(
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

            result_list.append(satellite_position._asdict())

    api_source = "IAU CPS SatChecker"
    version = "0.4"
    json_output(
        name, catalog_id, date_collected, data_source, result_list, api_source, version
    )

    if not result_list:
        return {"info": "No position information found with this criteria"}
    return result_list


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
    except Exception:
        # app.logger.error(e)
        return None

    return tle_sat


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
        print(e)
        return None

    return tle_sat


def get_tle(identifier, use_catalog_number, data_source, date):
    tle_sat = (
        get_tle_by_catalog_number(identifier, data_source, date)
        if use_catalog_number
        else get_tle_by_name(identifier, data_source, date)
    )
    if not tle_sat:
        abort(500, NO_TLE_FOUND)

    return tle_sat


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
