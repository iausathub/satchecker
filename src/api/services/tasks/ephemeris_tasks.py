import logging
from typing import Any

from astropy.coordinates import EarthLocation
from astropy.time import Time
from flask import current_app, has_app_context

from api.celery_app import celery
from api.utils.orbital_data_utils import deserialize_orbital_data
from api.utils.output_utils import position_data_to_json
from api.utils.propagation_strategies import (
    PropagationInfo,
    SGP4PropagationStrategy,
    SkyfieldPropagationStrategy,
    TestPropagationStrategy,
)

logger = logging.getLogger(__name__)


@celery.task
def process_results(
    data_points: list[tuple[float, ...]],
    min_altitude: float,
    max_altitude: float,
    date_collected: str,
    tle_epoch_date: str,
    name: str,
    intl_designator: str,
    catalog_id: str,
    data_source: str,
    api_source: str,
    api_version: str,
) -> dict[str, Any]:
    """
    Process the results of the satellite propagation.

    This function filters the satellite position data based on the altitude range and
    adds the remaining metadata to the results.

    Args:
        data_points (list[tuple[float, float]]): The satellite position results.
        min_altitude (float): The minimum altitude.
        max_altitude (float): The maximum altitude.
        date_collected (str): The date the data was collected.
        tle_epoch_date (str): The date the TLE was created.
        name (str): The name of the satellite.
        catalog_id (str): The catalog ID of the satellite.
        data_source (str): The data source.

    Returns:
        dict[str, Any]: Either the processed results dictionary or an
        info message dictionary.
    """
    if has_app_context():
        current_app.logger.info("process results started")
    # Filter out results that are not within the altitude range
    results = [
        result for result in data_points if min_altitude <= result[4] <= max_altitude
    ]

    if not results:
        return {
            "info": "No position information found with this criteria",
            "api_source": api_source,
            "version": api_version,
        }

    # Add remaining metadata to results
    data_set: dict[str, Any] = position_data_to_json(
        name,
        intl_designator,
        catalog_id,
        date_collected,
        tle_epoch_date,
        data_source,
        results,
        api_source,
        api_version,
    )
    if has_app_context():
        current_app.logger.info("process results complete")
    return data_set


@celery.task
def generate_position_data(
    location: EarthLocation,
    dates: list[Time],
    serialized_orbital_data: dict[str, Any],
    min_altitude: float,
    max_altitude: float,
    api_source: str,
    api_version: str,
    propagation_strategy: str = "skyfield",
) -> dict[str, Any] | list[dict[str, Any]]:
    """
    Create a list of results for a given satellite and date range.

    This function propagates the satellite for each date in the given range, processes
    the results, and returns a list of results.

    Args:
        location (EarthLocation): The location of the observer.
        dates (list[Time]): The dates for which to propagate the satellite.
        serialized_orbital_data (dict): Serialized TLE or orbital elements data.
        min_altitude (float): The minimum altitude for the results.
        max_altitude (float): The maximum altitude for the results.

    Returns:
        dict[str, Any] | list[dict[str, Any]]: Either a dictionary with results
        or a list of results for the given satellite and date range.
    """
    orbital_data = deserialize_orbital_data(serialized_orbital_data)
    satellite = orbital_data.satellite

    # Create a chord that will propagate the satellite for
    # each date and then process the results
    if propagation_strategy == "sgp4":
        if "tle_line1" not in serialized_orbital_data:
            raise ValueError(
                "SGP4 propagation requires TLE data; orbital elements are not supported"
            )
        method = propagate_satellite_sgp4
    elif propagation_strategy == "skyfield":
        method = propagate_satellite_skyfield
    else:
        raise ValueError(f"Invalid propagation strategy: {propagation_strategy}")

    # Convert all dates to JD values
    jd_dates = [date.jd for date in dates]

    result = method.apply(
        args=[
            serialized_orbital_data,
            location.lat.value,
            location.lon.value,
            location.height.value,
            jd_dates,
        ]
    )

    processed_results = process_results.apply(
        args=[
            result.get(),
            min_altitude,
            max_altitude,
            orbital_data.date_collected,
            orbital_data.epoch,
            satellite.sat_name,
            satellite.object_id,
            satellite.sat_number,
            orbital_data.data_source,
            api_source,
            api_version,
        ]
    )
    result_dict: dict[str, Any] = processed_results.get()
    if not result_dict:
        return [{"info": "No position information found with this criteria"}]

    return result_dict


@celery.task
def propagate_satellite_skyfield(serialized_orbital_data, lat, long, height, jd):
    """
    Propagates satellite and observer states using the Skyfield library.

    Args:
        serialized_orbital_data (dict): Serialized TLE or orbital elements data.
        lat (float): The latitude of the observer's location, in degrees.
        long (float): The longitude of the observer's location, in degrees.
        height (float): The height of the observer's location, in meters above the
        WGS84 ellipsoid.
        jd (float | list[float]): The Julian Date(s) at which to propagate
        the satellite.

    Returns:
        list[tuple]: A list of tuples containing the propagated state of the
        satellite and the observer.
    """
    orbital_data = deserialize_orbital_data(serialized_orbital_data)
    propagation_info = PropagationInfo(
        SkyfieldPropagationStrategy(),
        jd,
        lat,
        long,
        height,
        orbital_data=orbital_data,
    )
    return propagation_info.propagate()


@celery.task
def propagate_satellite_sgp4(
    serialized_orbital_data, lat, long, height, jd
):  # pragma: no cover
    """
    Propagates satellite and observer states using the SGP4 model.

    Args:
        serialized_orbital_data (dict): Serialized TLE data.
        lat (float): The latitude of the observer's location, in degrees.
        long (float): The longitude of the observer's location, in degrees.
        height (float): The height of the observer's location, in meters above the
        WGS84 ellipsoid.
        jd (float | list[float]): The Julian Date(s) at which to propagate
        the satellite.

    Returns:
        list[tuple]: A list of tuples containing the propagated state of the satellite
        and the observer.
    """
    if "tle_line1" not in serialized_orbital_data:
        raise ValueError(
            "SGP4 propagation requires TLE data; orbital elements are not supported"
        )
    orbital_data = deserialize_orbital_data(serialized_orbital_data)
    propagation_info = PropagationInfo(
        SGP4PropagationStrategy(),
        jd,
        lat,
        long,
        height,
        orbital_data=orbital_data,
    )
    return propagation_info.propagate()


@celery.task
def propagate_satellite_new(
    tle_line_1, tle_line_2, lat, long, height, jd
):  # pragma: no cover
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
    from api.services.validation_service import parse_tle

    orbital_data = parse_tle(f"{tle_line_1}\n{tle_line_2}")
    propagation_info = PropagationInfo(
        TestPropagationStrategy(),
        jd,
        lat,
        long,
        height,
        orbital_data=orbital_data,
    )
    return propagation_info.propagate()
