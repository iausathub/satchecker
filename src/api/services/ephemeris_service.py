from typing import Any

from astropy.coordinates import EarthLocation
from astropy.time import Time, TimeDelta

from api.adapters.repositories.orbital_elements_repository import (
    AbstractOrbitalElementsRepository,
)
from api.adapters.repositories.satellite_repository import AbstractSatelliteRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.common import error_messages
from api.common.exceptions import DataError
from api.domain.models.orbital_elements import OrbitalElements
from api.domain.models.tle import TLE
from api.services.tasks.ephemeris_tasks import generate_position_data
from api.utils.orbital_data_utils import ORBITAL_ELEMENTS_CUTOFF, serialize_orbital_data


def _get_closest_orbital_data(
    tle_repo: AbstractTLERepository,
    orbital_elements_repo: AbstractOrbitalElementsRepository,
    identifier: str,
    identifier_type: str,
    request_time: Time,
    data_source: str,
) -> TLE | OrbitalElements | None:
    """Return the closest TLE or orbital elements record for the request epoch."""
    epoch = request_time.to_datetime()
    use_tles = request_time < ORBITAL_ELEMENTS_CUTOFF

    if identifier_type == "name":
        if use_tles:
            return tle_repo.get_closest_by_satellite_name(
                identifier, epoch, data_source
            )
        return orbital_elements_repo.get_closest_by_satellite_name(
            identifier, epoch, data_source
        )

    if use_tles:
        return tle_repo.get_closest_by_satellite_number(identifier, epoch, data_source)
    return orbital_elements_repo.get_closest_by_satellite_number(
        identifier, epoch, data_source
    )


def generate_ephemeris_data(
    sat_repo: AbstractSatelliteRepository,
    tle_repo: AbstractTLERepository,
    orbital_elements_repo: AbstractOrbitalElementsRepository,
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
) -> dict[str, Any] | list[dict[str, Any]]:
    orbital_data = _get_closest_orbital_data(
        tle_repo,
        orbital_elements_repo,
        identifier,
        identifier_type,
        dates[0],
        data_source,
    )

    if orbital_data is None:
        raise DataError(422, error_messages.NO_TLE_FOUND)

    orbital_data_epoch_time = Time(orbital_data.epoch, scale="utc")
    if abs(dates[0] - orbital_data_epoch_time) > TimeDelta(30, format="jd"):
        raise DataError(422, error_messages.TLE_DATE_OUT_OF_RANGE)

    result_list_task = generate_position_data.apply(
        args=[
            location,
            dates,
            serialize_orbital_data(orbital_data),
            min_altitude,
            max_altitude,
            api_source,
            api_version,
            propagation_method,
        ]
    )
    result_list: dict[str, Any] | list[dict[str, Any]] = result_list_task.get()
    return result_list


def generate_ephemeris_data_user(
    tle: TLE,
    location: EarthLocation,
    dates: list[Time],
    min_altitude: float,
    max_altitude: float,
    api_source: str,
    api_version: str,
) -> dict[str, Any] | list[dict[str, Any]]:
    result_list_task = generate_position_data.apply(
        args=[
            location,
            dates,
            serialize_orbital_data(tle),
            min_altitude,
            max_altitude,
            api_source,
            api_version,
        ]
    )
    result_list: dict[str, Any] | list[dict[str, Any]] = result_list_task.get()
    return result_list
