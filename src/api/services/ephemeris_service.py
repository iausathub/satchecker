from typing import Any, Union

from astropy.coordinates import EarthLocation
from astropy.time import Time, TimeDelta

from api.adapters.repositories.ephemeris_repository import SqlAlchemyEphemerisRepository
from api.adapters.repositories.satellite_repository import AbstractSatelliteRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.common import error_messages
from api.common.exceptions import DataError
from api.domain.models.tle import TLE
from api.services.tasks.ephemeris_tasks import generate_position_data


def generate_ephemeris_data(
    sat_repo: AbstractSatelliteRepository,
    tle_repo: AbstractTLERepository,
    ephemeris_repo: SqlAlchemyEphemerisRepository,
    identifier: str,
    identifier_type: str,
    location: EarthLocation,
    dates: list[Time],
    min_altitude: float,
    max_altitude: float,
    api_source: str,
    api_version: str,
    data_source: str = "",
    propagation_method: str = "skyfield",
) -> Union[dict[str, Any], list[dict[str, Any]]]:

    #  get TLE from repository
    tle = (
        tle_repo.get_closest_by_satellite_name(
            identifier, dates[0].to_datetime(), data_source
        )
        if identifier_type == "name"
        else tle_repo.get_closest_by_satellite_number(
            identifier, dates[0].to_datetime(), data_source
        )
    )

    if tle is None:
        raise DataError(500, error_messages.NO_TLE_FOUND)

    # Check if the requested date is within 30 days of the TLE epoch
    tle_epoch_time = Time(tle.epoch, scale="utc")
    if abs(dates[0] - tle_epoch_time) > TimeDelta(30, format="jd"):  # 30 days
        raise DataError(500, error_messages.TLE_DATE_OUT_OF_RANGE)

    # get the list of position data for each date/time in the requested range
    result_list_task = generate_position_data.apply(
        args=[
            location,
            dates,
            tle.tle_line1,
            tle.tle_line2,
            tle.date_collected,
            tle.epoch,
            tle.satellite.sat_name,
            tle.satellite.object_id,
            min_altitude,
            max_altitude,
            api_source,
            api_version,
            tle.satellite.sat_number,
            tle.data_source,
            propagation_method,
            ephemeris_repo,
        ]
    )
    result_list: Union[dict[str, Any], list[dict[str, Any]]] = result_list_task.get()
    return result_list


def generate_ephemeris_data_user(
    tle: TLE,
    location: EarthLocation,
    dates: list[Time],
    min_altitude: float,
    max_altitude: float,
    api_source: str,
    api_version: str,
    ephemeris_repo: SqlAlchemyEphemerisRepository,
) -> Union[dict[str, Any], list[dict[str, Any]]]:

    result_list_task = generate_position_data.apply(
        args=[
            location,
            dates,
            tle.tle_line1,
            tle.tle_line2,
            tle.date_collected,
            tle.epoch,
            tle.satellite.sat_name,
            tle.satellite.object_id,
            min_altitude,
            max_altitude,
            api_source,
            api_version,
            tle.satellite.sat_number,
            tle.data_source,
            ephemeris_repo,
        ]
    )
    result_list: Union[dict[str, Any], list[dict[str, Any]]] = result_list_task.get()
    return result_list
