from flask import abort
from sqlalchemy import and_
from sqlalchemy.exc import DataError

from .. import error_messages
from ..extensions import db
from . import models


def get_ids_for_satelltite_name(satellite_name):
    norad_ids_and_dates = (
        db.session.query(
            models.Satellite.sat_number,
            models.Satellite.date_added,
        )
        .filter(models.Satellite.sat_name == satellite_name)
        .order_by(models.Satellite.date_added.desc())
        .all()
    )

    return norad_ids_and_dates


def get_names_for_satellite_id(satellite_id):
    satellite_names_and_dates = (
        db.session.query(models.Satellite.sat_name, models.Satellite.date_added)
        .filter(models.Satellite.sat_number == satellite_id)
        .order_by(models.Satellite.date_added.desc())
        .all()
    )

    return satellite_names_and_dates


def get_tles(satellite_id, id_type, start_date, end_date):

    # Define the date filter
    date_filter = []
    if start_date is not None:
        date_filter.append(models.TLE.date_collected >= start_date)
    if end_date is not None:
        date_filter.append(models.TLE.date_collected <= end_date)

    # if there is no start date or end date for the date range, return all data
    if not date_filter:
        date_filter.append(True)

    # Define the satellite filter
    satellite_filter = []
    if id_type == "catalog":
        satellite_filter.append(models.Satellite.sat_number == satellite_id)
    elif id_type == "name":
        satellite_filter.append(models.Satellite.sat_name == satellite_id)

    try:
        tle_data = (
            db.session.query(models.TLE)
            .join(models.Satellite, models.TLE.sat_id == models.Satellite.id)
            .filter(and_(*satellite_filter))
            .filter(and_(*date_filter))
            .order_by(models.TLE.date_collected.desc())
            .all()
        )
        return tle_data

    except Exception as e:
        if isinstance(e, DataError):
            abort(500, error_messages.NO_TLE_FOUND)
        return None
