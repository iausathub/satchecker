import logging
from typing import Tuple

from astropy.coordinates import EarthLocation
from astropy.time import Time
from celery import chord
from flask import current_app, has_app_context

from api import celery
from api.common.position_data_point import position_data_point

# from core import celery, utils
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
    data_points: list[Tuple[float, float]],
    min_altitude: float,
    max_altitude: float,
    date_collected: str,
    name: str,
    catalog_id: str,
    data_source: str,
    api_source: str,
    api_version: str,
) -> list[position_data_point]:
    """
    Process the results of the satellite propagation.

    This function filters the satellite position data based on the altitude range and
    adds the remaining metadata to the results.

    Args:
        data_points (list[Tuple[float, float]]): The satellite position results.
        min_altitude (float): The minimum altitude.
        max_altitude (float): The maximum altitude.
        date_collected (str): The date the data was collected.
        name (str): The name of the satellite.
        catalog_id (str): The catalog ID of the satellite.
        data_source (str): The data source.

    Returns:
        list[position_data_point]: The processed results.
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
    data_set = position_data_to_json(
        name, catalog_id, date_collected, data_source, results, api_source, api_version
    )
    if has_app_context():
        current_app.logger.info("process results complete")
    return data_set


@celery.task
def generate_position_data(
    location: EarthLocation,
    dates: list[Time],
    tle_line_1: str,
    tle_line_2: str,
    date_collected: str,
    name: str,
    min_altitude: float,
    max_altitude: float,
    api_source: str,
    api_version: str,
    catalog_id: str = "",
    data_source: str = "",
    propagation_strategy: str = "skyfield",
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
    # Create a chord that will propagate the satellite for
    # each date and then process the results
    if propagation_strategy == "sgp4":
        method = propagate_satellite_sgp4
    elif propagation_strategy == "skyfield":
        method = propagate_satellite_skyfield
    else:
        raise ValueError(f"Invalid propagation strategy: {propagation_strategy}")

    tasks = chord(
        (
            method.s(
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
            min_altitude,
            max_altitude,
            date_collected,
            name,
            catalog_id,
            data_source,
            api_source,
            api_version,
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


@celery.task
def propagate_satellite_sgp4(
    tle_line_1, tle_line_2, lat, long, height, jd
):  # pragma: no cover
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
    propagation_info = PropagationInfo(
        TestPropagationStrategy(), tle_line_1, tle_line_2, jd, lat, long, height
    )
    return propagation_info.propagate()
