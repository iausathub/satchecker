import logging
import time as python_time
from datetime import datetime
from typing import Any

import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from skyfield.api import EarthSatellite, load, wgs84

from api.adapters.repositories.tle_repository import (
    AbstractTLERepository,
    SqlAlchemyTLERepository,
)
from api.domain.models.tle import TLE
from api.services.cache_service import (
    create_fov_cache_key,
    get_cached_data,
    set_cached_data,
)
from api.services.tasks.fov_tasks import calculate_satellite_passes_async
from api.utils import coordinate_systems, output_utils
from api.utils.propagation_strategies import FOVParallelPropagationStrategy
from api.utils.time_utils import astropy_time_to_datetime_utc

logger = logging.getLogger(__name__)


def get_satellite_passes_in_fov_async(
    tle_repo: AbstractTLERepository,
    location: EarthLocation,
    mid_obs_time_jd: Time,
    start_time_jd: Time,
    duration: float,
    ra: float,
    dec: float,
    fov_radius: float,
    group_by: str,
    include_tles: bool,
    skip_cache: bool,
    constellation: str,
    data_source: str,
    illuminated_only: bool,
    api_source: str,
    api_version: str,
) -> dict[str, Any]:

    start_time = python_time.time()

    _log_fov_parameters(
        True,
        ra,
        dec,
        fov_radius,
        duration,
        location,
        mid_obs_time_jd,
        start_time_jd,
        group_by,
        include_tles,
        skip_cache,
    )

    # Create cache key and check cache
    cache_key = create_fov_cache_key(
        location,
        mid_obs_time_jd,
        start_time_jd,
        duration,
        ra,
        dec,
        fov_radius,
        False if include_tles is None else include_tles,
        constellation,
        data_source,
    )

    # TODO: resolve caching issue
    cached_data = _check_cache_for_results(
        cache_key, start_time, api_source, api_version, group_by
    )
    if cached_data:
        return cached_data

    time_param = mid_obs_time_jd if mid_obs_time_jd is not None else start_time_jd
    # Get all current TLEs
    tles, count, tle_time = _get_tle_data(
        tle_repo, time_param, constellation, data_source
    )

    jd_times = _create_jd_list(mid_obs_time_jd, start_time_jd, duration)

    # Serialize TLEs for Celery task
    serialized_tles = SqlAlchemyTLERepository.batch_serialize_tles(tles)

    result_list_task = calculate_satellite_passes_async.apply_async(
        args=[
            ra,
            dec,
            fov_radius,
            serialized_tles,
            jd_times.tolist(),
            location.lat.value,
            location.lon.value,
            location.height.value,
            include_tles,
            250,
            illuminated_only,
            group_by,
            tle_time,
        ]
    )

    # Return task ID instead of waiting for result
    return {
        "task_id": result_list_task.id,
        "status": "PENDING",
        "message": (
            "FOV calculation started. Use the task_id to check status and "
            "retrieve results."
        ),
        "api_source": api_source,
        "api_version": api_version,
    }


def get_satellite_passes_in_fov(
    tle_repo: AbstractTLERepository,
    location: EarthLocation,
    mid_obs_time_jd: Time,
    start_time_jd: Time,
    duration: float,
    ra: float,
    dec: float,
    fov_radius: float,
    group_by: str,
    include_tles: bool,
    skip_cache: bool,
    constellation: str,
    data_source: str,
    illuminated_only: bool,
    api_source: str,
    api_version: str,
) -> dict[str, Any]:
    """
    Get all satellite passes in the field of view.

    Args:
        tle_repo: Repository for TLE data
        location: Observer's location
        mid_obs_time_jd: Middle observation time (as Time object)
        start_time_jd: Start time (as Time object)
        duration: Duration in seconds
        ra: Right ascension of FOV center in degrees
        dec: Declination of FOV center in degrees
        fov_radius: Radius of FOV in degrees
        group_by: Grouping strategy ('satellite' or 'time')
        include_tles: Whether to include TLE data in results
        skip_cache: Whether to skip cache and force recalculation
        constellation: Constellation of the satellites to include in the response
        data_source: Data source for TLEs
        illuminated_only: Whether to include only illuminated satellites
        api_source: Source of the API call
        api_version: Version of the API

    Returns:
        dict: Formatted results either grouped by satellite or chronologically
    """
    start_time = python_time.time()

    _log_fov_parameters(
        False,
        ra,
        dec,
        fov_radius,
        duration,
        location,
        mid_obs_time_jd,
        start_time_jd,
        group_by,
        include_tles,
        skip_cache,
    )

    # Create cache key and check cache
    cache_key = create_fov_cache_key(
        location,
        mid_obs_time_jd,
        start_time_jd,
        duration,
        ra,
        dec,
        fov_radius,
        False if include_tles is None else include_tles,
        constellation,
        data_source,
    )

    # TODO: resolve caching issue
    cached_data = _check_cache_for_results(
        cache_key, start_time, api_source, api_version, group_by
    )
    if cached_data:
        return cached_data

    time_param = mid_obs_time_jd if mid_obs_time_jd is not None else start_time_jd

    # Get all current TLEs
    tles, count, tle_time = _get_tle_data(
        tle_repo, time_param, constellation, data_source
    )

    prop_start = python_time.time()

    jd_times = _create_jd_list(mid_obs_time_jd, start_time_jd, duration)

    all_results = []
    points_in_fov = 0
    satellites_processed = 0

    # Create propagation strategy
    prop_strategy = FOVParallelPropagationStrategy()

    try:
        logger.info("Starting parallel propagation with batch size 250")
        results, execution_time, satellites_processed = prop_strategy.propagate(
            all_tles=tles,
            jd_times=jd_times,
            location=location,
            fov_center=(ra, dec),
            fov_radius=fov_radius,
            batch_size=250,
            include_tles=include_tles,
            illuminated_only=illuminated_only,
        )

        # Add all valid results to the final output
        if results:
            all_results.extend(results)
            points_in_fov = len(results)
            logger.info(
                f"Propagation completed successfully with {points_in_fov} points in FOV"
            )
        else:
            logger.warning("Propagation completed but returned no results")

    except Exception as e:
        logger.error(f"Error in parallel FOV processing: {str(e)}", exc_info=True)
        logger.error(f"Failed after processing {satellites_processed} satellites")
        satellites_processed = 0  # Set a default value in case of error
        raise

    end_time = python_time.time()
    total_time = end_time - start_time
    prop_time = end_time - prop_start

    performance_metrics = _calculate_performance_metrics(
        total_time,
        tle_time,
        prop_time,
        satellites_processed,
        points_in_fov,
        jd_times,
        count,
        execution_time,
    )

    # Before returning results, log any None values
    for idx, result in enumerate(all_results):
        for key, value in result.items():
            if value is None:
                logger.warning(
                    f"Found None value in result {idx}, field {key} before returning"
                )

    try:
        json_result: dict[str, Any] = output_utils.fov_data_to_json(
            all_results,
            points_in_fov,
            performance_metrics,
            api_source,
            api_version,
            group_by,
        )
        logger.info("Successfully formatted results to JSON")
    except Exception as e:
        logger.error(f"Failed to format results to JSON: {str(e)}", exc_info=True)
        raise

    # Cache only the raw results and points_in_fov
    _cache_results(cache_key, all_results, points_in_fov, performance_metrics)

    return json_result


def get_satellites_above_horizon(
    tle_repo: AbstractTLERepository,
    location: EarthLocation,
    julian_dates: list[Time],
    min_altitude: float,
    min_range: float,
    max_range: float,
    illuminated_only: bool = False,
    constellation: str | None = None,
    api_source: str = "",
    api_version: str = "",
) -> dict[str, Any]:
    """
    Get all satellites above the horizon at a specific time.

    Args:
        tle_repo: Repository for TLE data
        location: Observer's location
        time_jd: Time to check (as Time object)
        min_altitude: Minimum altitude in degrees (default: 0.0 = horizon)
        min_range: Minimum range in kilometers
        max_range: Maximum range in kilometers
        illuminated_only: Whether to only return illuminated satellites
        constellation: Constellation of the satellites to include in the response
        api_source: Source of the API call
        api_version: Version of the API

    Returns:
        dict: Formatted results containing satellite positions and metadata
    """
    start_time = python_time.time()
    print(f"\nStarting horizon check at: {datetime.now().isoformat()}")
    print(f"Minimum altitude: {min_altitude}°")
    print(f"Time: {julian_dates}")
    print(f"Location: {location}")

    time_jd = julian_dates[0]

    # Get all current TLEs
    tle_start = python_time.time()
    tles, count, _ = tle_repo.get_all_tles_at_epoch(
        astropy_time_to_datetime_utc(time_jd), 1, 10000, "zip", constellation
    )
    tle_time = python_time.time() - tle_start

    # Set up time and observer
    ts = load.timescale()
    t = ts.ut1_jd([time_jd.jd])  # Single time point
    curr_pos = wgs84.latlon(
        location.lat.value, location.lon.value, location.height.value
    )

    all_results = []
    satellites_processed = 0
    visible_satellites = 0

    for tle in tles:
        try:
            satellite = EarthSatellite(tle.tle_line1, tle.tle_line2, ts=ts)
            difference = satellite - curr_pos
            topocentric = difference.at(t)

            # Get altitude and azimuth
            alt, az, distance = topocentric.altaz()

            # Check if above minimum altitude and within range
            if (
                float(alt._degrees[0]) >= min_altitude
                and min_range <= distance.km[0] <= max_range
            ):
                # Get position in RA/Dec
                topocentricn = topocentric.position.km / np.linalg.norm(
                    topocentric.position.km, axis=0
                )
                ra_sat, dec_sat = coordinate_systems.icrf2radec(topocentricn[:, 0])
                if illuminated_only:
                    sat_gcrs = satellite.at(t).position.km
                    illuminated = coordinate_systems.is_illuminated(
                        sat_gcrs[:, 0], time_jd.jd
                    )
                    if not illuminated:
                        continue
                position = {
                    "ra": ra_sat,
                    "dec": dec_sat,
                    "altitude": float(alt._degrees[0]),
                    "azimuth": float(az._degrees[0]),
                    "name": tle.satellite.sat_name,
                    "norad_id": tle.satellite.sat_number,
                    "julian_date": time_jd.jd,
                    "range_km": float(distance.km[0]),
                    "tle_epoch": output_utils.format_date(tle.epoch),
                }
                all_results.append(position)
                visible_satellites += 1

            satellites_processed += 1

            if satellites_processed % 100 == 0:
                elapsed = python_time.time() - start_time
                print(
                    f"Processed {satellites_processed}/{count} satellites in {elapsed:.2f} seconds"  # noqa: E501
                )
                print(f"Found {visible_satellites} visible satellites so far")

        except Exception as e:
            print(f"Error processing Satellite {tle.satellite.sat_name}: {e}")
            satellites_processed += 1
            continue

    end_time = python_time.time()
    total_time = end_time - start_time

    performance_metrics = {
        "total_time": round(total_time, 3),
        "tle_time": round(tle_time, 3),
        "satellites_processed": satellites_processed,
        "visible_satellites": visible_satellites,
    }

    result: dict[str, Any] = output_utils.fov_data_to_json(
        all_results,
        visible_satellites,
        performance_metrics,
        api_source,
        api_version,
        "time",
    )
    return result


def _get_tle_data(
    tle_repo: AbstractTLERepository, time_jd: Time, constellation: str, data_source: str
) -> tuple[list[TLE], int, float]:
    tle_start = python_time.time()

    logger.info(f"Fetching TLEs for epoch: {astropy_time_to_datetime_utc(time_jd)}")

    try:
        tles, count, _ = tle_repo.get_all_tles_at_epoch(
            astropy_time_to_datetime_utc(time_jd),
            1,
            10000,
            "zip",
            constellation,
            data_source,
        )
        logger.info(f"Successfully retrieved {count} TLEs")
    except Exception as e:
        logger.error(f"Failed to retrieve TLEs: {str(e)}", exc_info=True)
        raise

    tle_time = python_time.time() - tle_start
    logger.info(f"Retrieved {count} TLEs in {tle_time:.2f} seconds")

    return tles, count, tle_time


def _check_cache_for_results(
    cache_key: str, start_time: float, api_source: str, api_version: str, group_by: str
) -> dict[str, Any] | None:
    """
    Check cache for FOV calculation results and return formatted data if found.

    Args:
        cache_key: Unique key for the cache entry
        start_time: Start time for performance calculation
        api_source: Source of the API call
        api_version: Version of the API
        group_by: Grouping strategy for results

    Returns:
        dict[str, Any] | None: Formatted cached results if found, None otherwise
    """
    skip_cache = True

    cached_data = get_cached_data(cache_key)

    if cached_data and not skip_cache:  # pragma: no cover
        cache_time = python_time.time() - start_time
        logger.info(
            f"Cache hit: Found {len(cached_data['results'])} results with "
            f"{cached_data['points_in_fov']} points in FOV"
        )
        # Log any None values in the cached results
        for idx, result in enumerate(cached_data.get("results", [])):
            for key, value in result.items():
                if value is None:
                    logger.warning(
                        f"Found None value in cached result {idx}, field {key}"
                    )
        # Return cached results using the same formatting function
        return output_utils.fov_data_to_json(
            cached_data["results"],
            cached_data["points_in_fov"],
            {
                "total_time": round(cache_time, 3),
                "points_in_fov": cached_data["points_in_fov"],
                "from_cache": True,
            },
            api_source,
            api_version,
            group_by,
        )

    logger.info("Cache miss - calculating FOV results")
    return None


def _cache_results(
    cache_key: str,
    all_results: list[dict[str, Any]],
    points_in_fov: int,
    performance_metrics: dict[str, Any],
) -> None:
    """
    Cache FOV calculation results for future use.

    Args:
        cache_key: Unique key for the cache entry
        all_results: List of satellite pass results
        points_in_fov: Number of points found in field of view
        performance_metrics: Performance metrics dictionary
    """
    cache_data = {
        "results": all_results,
        "points_in_fov": points_in_fov,
    }
    logger.info(
        f"Caching {len(all_results)} results with {points_in_fov} points in FOV"
    )
    try:
        set_cached_data(cache_key, cache_data)
        logger.info("Successfully cached results")
    except Exception as e:
        logger.error(f"Failed to cache results: {str(e)}", exc_info=True)
        # Don't raise here as caching is not critical


def _create_jd_list(
    mid_obs_time_jd: Time,
    start_time_jd: Time,
    duration: float,
) -> np.ndarray:
    """
    Create a list of Julian day times for FOV calculations.

    Args:
        mid_obs_time_jd: Middle observation time (as Time object)
        start_time_jd: Start time (as Time object)
        duration: Duration in seconds

    Returns:
        np.ndarray: Array of Julian day times for propagation calculations
    """
    # Pre-compute time arrays and constants
    time_step = 1 / 86400  # 1 second
    duration_jd = duration / 86400

    if mid_obs_time_jd is not None:
        jd_times = np.arange(
            mid_obs_time_jd.jd - duration_jd / 2,
            mid_obs_time_jd.jd + duration_jd / 2,
            time_step,
        )
    elif start_time_jd is not None:
        jd_times = np.arange(
            start_time_jd.jd,
            start_time_jd.jd + duration_jd,
            time_step,
        )
    logger.info(f"Checking {len(jd_times)} time points")
    return jd_times


def _log_fov_parameters(
    async_mode: bool,
    ra: float,
    dec: float,
    fov_radius: float,
    duration: float,
    location: EarthLocation,
    mid_obs_time_jd: Time,
    start_time_jd: Time,
    group_by: str,
    include_tles: bool,
    skip_cache: bool,
):
    logger.info(f"Starting FOV calculation at: {datetime.now().isoformat()}")

    logger.info(f"FOV calculation mode: {'async' if async_mode else 'sync'}")

    logger.info(f"FOV Parameters: RA={ra}°, Dec={dec}°, Radius={fov_radius}°")
    logger.info(f"Duration: {duration} seconds")
    logger.info(
        f"Location: lat={location.lat.value}°, "
        f"lon={location.lon.value}°, "
        f"height={location.height.value}m"
    )
    logger.info(
        f"Time parameters: mid_obs_time={mid_obs_time_jd}, start_time={start_time_jd}"
    )
    logger.info(
        f"Group by: {group_by}, Include TLEs: {include_tles}, Skip cache: {skip_cache}"
    )


def _calculate_performance_metrics(
    total_time: float,
    tle_time: float,
    prop_time: float,
    satellites_processed: int,
    points_in_fov: int,
    jd_times: list[float],
    count: int,
    execution_time: float,
) -> dict[str, Any]:
    """
    Calculate and log performance metrics for FOV calculations.

    Args:
        total_time: Total execution time in seconds
        tle_time: Time spent retrieving TLE data in seconds
        prop_time: Time spent on propagation calculations in seconds
        satellites_processed: Number of satellites processed
        points_in_fov: Number of points found in field of view
        jd_times: List of Julian day times used in calculations
        count: Total number of satellites available
        execution_time: Time spent on propagation execution

    Returns:
        dict[str, Any]: Performance metrics dictionary
    """
    # Log performance metrics
    total_time = tle_time + prop_time + execution_time
    logger.info("\nPerformance Metrics:")
    logger.info(f"Total execution time: {total_time:.2f} seconds")
    logger.info(
        f"TLE retrieval time: {tle_time:.2f} seconds "
        f"({(tle_time/total_time)*100:.1f}%)"
    )
    logger.info(
        f"Propagation time: {prop_time:.2f} seconds "
        f"({(prop_time/total_time)*100:.1f}%)"
    )
    logger.info("\nResults Summary:")
    logger.info(f"Satellites processed: {satellites_processed}/{count}")
    logger.info(f"Points in FOV: {points_in_fov}")
    logger.info(f"End time: {datetime.now().isoformat()}")

    performance_metrics = {
        "total_time": round(total_time, 3),
        "tle_time": round(tle_time, 3),
        "propagation_time": round(execution_time, 3),
        "satellites_processed": satellites_processed,
        "points_in_fov": points_in_fov,
        "jd_times": jd_times.tolist(),
    }

    return performance_metrics
