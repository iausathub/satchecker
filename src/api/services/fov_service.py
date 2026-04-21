# mypy: disable-error-code=unreachable
import logging
import time as python_time
from datetime import datetime, timedelta
from typing import Any

import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from celery import chord, group
from skyfield.api import EarthSatellite, wgs84

from api.adapters.repositories.ephemeris_repository import AbstractEphemerisRepository
from api.adapters.repositories.tdm_repository import AbstractTdmPredictionRepository
from api.adapters.repositories.tle_repository import (
    AbstractTLERepository,
    SqlAlchemyTLERepository,
)
from api.domain.models.tdm_prediction_point import TdmPredictionPoint
from api.domain.models.tle import TLE
from api.services.cache_service import (
    create_fov_cache_key,
    get_cached_data,
    set_cached_data,
)
from api.services.tasks.fov_tasks import (
    aggregate_fov_results_task,
    process_satellite_batch_task,
    refine_with_ephemeris_task,
)
from api.utils import coordinate_systems, output_utils
from api.utils.propagation_strategies import (
    FOVParallelPropagationStrategy,
    KroghPropagationStrategy,
    satellite_position_fov,
    # FOVPropagationStrategy,
)
from api.utils.skyfield_loader import load
from api.utils.time_utils import astropy_time_to_datetime_utc, ensure_datetime

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
    tle_only: bool,
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
        cache_key,
        start_time,
        api_source,
        api_version,
        group_by,
        ra=ra,
        dec=dec,
        fov_radius=fov_radius,
        duration=duration,
        location=location,
    )
    if cached_data:
        return cached_data

    time_param = mid_obs_time_jd if mid_obs_time_jd is not None else start_time_jd
    # Get all current TLEs
    tles, count, tle_time = _get_tle_data(
        tle_repo, time_param, constellation, data_source
    )

    jd_times = _create_jd_list(mid_obs_time_jd, start_time_jd, duration)
    jd_times_list = jd_times.tolist()

    if not tles:
        # No TLEs: return empty result immediately, no task needed
        performance_metrics = {
            "total_time": round(tle_time, 3),
            "tle_time": round(tle_time, 3),
            "propagation_time": 0,
            "satellites_processed": 0,
            "points_in_fov": 0,
            "jd_times": jd_times_list,
        }
        empty_result = output_utils.fov_data_to_json(
            [], 0, performance_metrics, api_source, api_version, group_by
        )
        return {
            **empty_result,
            "task_id": None,
            "status": "SUCCESS",
            "message": "No TLEs available for the requested criteria",
        }

    batch_size = 1000
    # Build batches and create chord for multi-CPU parallelism
    common_args = {
        "jd_times": jd_times_list,
        "location_lat": float(location.lat.value),
        "location_lon": float(location.lon.value),
        "location_height": float(location.height.value),
        "fov_center": (float(ra), float(dec)),
        "fov_radius": float(fov_radius),
        "include_tles": include_tles,
        "illuminated_only": illuminated_only,
    }

    batch_tasks = []
    for i in range(0, len(tles), batch_size):
        batch = tles[i : i + batch_size]
        serialized_batch = SqlAlchemyTLERepository.batch_serialize_tles(batch)
        batch_tasks.append(
            process_satellite_batch_task.s(serialized_batch, **common_args)
        )

    callback = aggregate_fov_results_task.s(
        group_by=group_by,
        tle_time=tle_time,
        jd_times=jd_times_list,
    )
    if not tle_only:
        callback = callback | refine_with_ephemeris_task.s(
            jd_times=jd_times_list,
            location_lat=float(location.lat.value),
            location_lon=float(location.lon.value),
            location_height=float(location.height.value),
            ra=float(ra),
            dec=float(dec),
            fov_radius=float(fov_radius),
        )

    chord_primitive = chord(group(batch_tasks), callback)
    chord_result = chord_primitive.apply_async()
    task_id = chord_result.id

    return {
        "task_id": task_id,
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
    ephemeris_repo: AbstractEphemerisRepository,
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
    tle_only: bool,
    api_source: str,
    api_version: str,
) -> dict[str, Any]:
    """
    Get all satellite passes in the field of view.

    Args:
        tle_repo: Repository for TLE data
        ephemeris_repo: Repository for ephemeris data
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
        tle_only: Whether to include only TLE data in the response
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
        cache_key,
        start_time,
        api_source,
        api_version,
        group_by,
        ra=ra,
        dec=dec,
        fov_radius=fov_radius,
        duration=duration,
        location=location,
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

    tles_to_propagate = tles

    # Process non-Starlink satellites with parallel propagation
    if tles_to_propagate:
        logger.info(
            f"Processing {len(tles_to_propagate)} non-Starlink satellites "
            f"with parallel propagation"
        )
        prop_strategy = FOVParallelPropagationStrategy()
        try:
            results, execution_time, non_starlink_processed = prop_strategy.propagate(
                all_tles=tles_to_propagate,
                jd_times=jd_times,
                location=location,
                fov_center=(ra, dec),
                fov_radius=fov_radius,
                batch_size=250,
                include_tles=include_tles,
            )

            # Add all valid results to the final output
            if results:
                all_results.extend(results)
                points_in_fov += len(results)
                satellites_processed += non_starlink_processed
                logger.info(
                    f"Found {len(results)} points in FOV for non-Starlink satellites"
                )

        except Exception as e:
            logger.error(f"Error in parallel FOV processing: {str(e)}", exc_info=True)

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
        prop_time,
    )

    # Before returning results, log any None values
    for idx, result in enumerate(all_results):
        for key, value in result.items():
            if value is None:
                logger.warning(
                    f"Found None value in result {idx}, field {key} before returning"
                )

    if not tle_only:
        # Process ephemeris data for satellites that were initially processed with TLE
        # data
        # Only process each unique norad_id once and replace original TLE results
        unique_norad_ids = set()
        for result in all_results:
            if result.get("norad_id") is not None:
                unique_norad_ids.add(result["norad_id"])

        # Batch lookup all ephemeris data at once
        satellite_numbers = [str(norad_id) for norad_id in unique_norad_ids]
        ephemeris_dict = ephemeris_repo.get_closest_by_satellite_numbers(
            satellite_numbers,
            ensure_datetime(jd_times[0]),
        )

        logger.info(
            f"Found ephemeris data for {len(ephemeris_dict)} out of "
            f"{len(unique_norad_ids)} satellites"
        )

        for norad_id in satellite_numbers:
            krogh_strategy = KroghPropagationStrategy()

            ephemeris = ephemeris_dict.get(int(norad_id))

            # Skip if no ephemeris data found
            if ephemeris is None:
                logger.warning(f"No ephemeris data found for satellite {norad_id}")
                continue

            try:
                krogh_strategy.load_ephemeris(ephemeris, ephemeris_repo)
            except Exception as e:
                logger.error(f"Error loading ephemeris for satellite {norad_id}: {e}")
                continue

            try:
                # Propagate positions
                positions = krogh_strategy.propagate(
                    jd_times,
                    "",
                    "",
                    location.lat.value,
                    location.lon.value,
                    location.height.value,
                )
                logger.info(
                    f"Propagated {len(positions)} positions for satellite {norad_id}"
                )

                # Check if positions are in FOV
                replacement_results = []
                for pos in positions:

                    if pos.ra is not None and pos.dec is not None:
                        # Calculate angular distance from FOV center
                        angular_distance = np.sqrt(
                            (pos.ra - ra) ** 2 + (pos.dec - dec) ** 2
                        )
                        if angular_distance <= fov_radius * 1.2:  # add 20% margin
                            # Create new satellite_position_fov with updated values
                            updated_pos = satellite_position_fov(
                                ra=pos.ra,
                                dec=pos.dec,
                                covariance=pos.covariance.tolist(),
                                angle=angular_distance,
                                altitude=pos.altitude,
                                azimuth=pos.azimuth,
                                range_km=pos.range_km,
                                julian_date=pos.julian_date,
                                name=ephemeris.satellite.sat_name,
                                norad_id=int(norad_id),
                                orbital_data_epoch=output_utils.format_date(
                                    ephemeris.generated_at
                                ),
                                orbital_data_source="ephemeris",
                            )

                            replacement_results.append(updated_pos._asdict())

                # Replace all TLE results for this norad_id
                # with ephemeris results
                all_results = [
                    result
                    for result in all_results
                    if result.get("norad_id") != int(norad_id)
                ]
                all_results.extend(replacement_results)
            except Exception as e:
                logger.error(
                    f"Error propagating positions for satellite {norad_id}: {e}"
                )
                continue

    # Calculate final points_in_fov count after all processing
    points_in_fov = len(all_results)

    try:
        json_result: dict[str, Any] = output_utils.fov_data_to_json(
            all_results,
            points_in_fov,
            performance_metrics,
            api_source,
            api_version,
            group_by,
        )
        logger.debug("Successfully formatted results to JSON")
    except Exception as e:
        logger.error(f"Failed to format results to JSON: {str(e)}", exc_info=True)
        raise

    # Cache only the raw results and points_in_fov
    _cache_results(cache_key, all_results, points_in_fov, performance_metrics)

    logger.info(
        f"FOV completed: RA={ra}° Dec={dec}° radius={fov_radius}° duration={duration}s "
        f"lat={location.lat.value}° lon={location.lon.value}° "
        f"height={location.height.value}m {satellites_processed} satellites, "
        f"{points_in_fov} points in FOV, {total_time:.2f}s (calculated)"
    )
    return json_result


def get_satellite_passes_in_fov_tdm(
    tdm_repo: AbstractTdmPredictionRepository,
    site: str,
    location: EarthLocation,
    mid_obs_time_jd: Time,
    start_time_jd: Time,
    duration: float,
    ra: float,
    dec: float,
    fov_radius: float,
    group_by: str,
    constellation: str,
    api_source: str,
    api_version: str,
) -> dict[str, Any]:
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
        False,
        True,
    )

    base_time = mid_obs_time_jd if mid_obs_time_jd is not None else start_time_jd
    base_datetime = astropy_time_to_datetime_utc(base_time)
    time_param_datetime = base_datetime - timedelta(seconds=duration / 2)
    time_param = Time(time_param_datetime)

    # Get all current TLEs
    tdm_prediction_points, count, tdm_prediction_time = _get_tdm_prediction_points(
        tdm_repo, time_param, duration, site, constellation
    )

    calc_start = python_time.time()

    jd_times = _create_jd_list(mid_obs_time_jd, start_time_jd, duration)

    all_results = []
    points_in_fov = 0
    prediction_points_processed = 0
    try:
        # for each tdm prediction point, check if it is in the FOV during
        # the duration of the observation
        # if it is, add it to the results

        ra_points = np.array([pt.right_ascension for pt in tdm_prediction_points])
        dec_points = np.array([pt.declination for pt in tdm_prediction_points])
        timestamps = np.array([pt.timestamp for pt in tdm_prediction_points])

        in_fov = coordinate_systems.is_in_fov(
            ra_points, dec_points, ra, dec, fov_radius
        )
        end_obs_time = time_param_datetime + timedelta(seconds=duration)
        in_time = (timestamps >= time_param_datetime) & (timestamps <= end_obs_time)

        fov_mask = in_fov & in_time

        matched = [p for p, m in zip(tdm_prediction_points, fov_mask, strict=True) if m]

        points_in_fov += len(matched)
        prediction_points_processed += len(tdm_prediction_points)

    except Exception as e:
        logger.error(
            f"Error in FOV processing with TDM predictions: {str(e)}",
            exc_info=True,
        )
        logger.error(
            f"Failed after processing {prediction_points_processed} prediction points"
        )
        prediction_points_processed = 0  # Set a default value in case of error
        raise

    end_time = python_time.time()
    total_time = end_time - start_time
    execution_time = end_time - calc_start

    performance_metrics = _calculate_performance_metrics(
        total_time,
        tdm_prediction_time,
        execution_time,
        prediction_points_processed,
        points_in_fov,
        jd_times,
        count,
        execution_time,
    )

    # convert tdm prediction points to dicts with info about points in fov
    all_results = [
        {
            "date_time": pt.timestamp,
            "ra": pt.right_ascension,
            "dec": pt.declination,
            "apparent_magnitude": pt.apparent_magnitude,
            "norad_id": pt.satellite_number,
            "name": pt.satellite_name,
        }
        for pt in matched
    ]

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
        "data_retrieval_time": round(tle_time, 3),
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

    logger.debug(f"Fetching TLEs for epoch: {astropy_time_to_datetime_utc(time_jd)}")

    try:
        tles, count, _ = tle_repo.get_all_tles_at_epoch(
            astropy_time_to_datetime_utc(time_jd),
            1,
            10000,
            "zip",
            constellation,
            data_source,
        )
        logger.debug(f"Successfully retrieved {count} TLEs")
    except Exception as e:
        logger.error(f"Failed to retrieve TLEs: {str(e)}", exc_info=True)
        raise

    tle_time = python_time.time() - tle_start
    logger.debug(f"Retrieved {count} TLEs in {tle_time:.2f} seconds")

    return tles, count, tle_time


def _get_tdm_prediction_points(
    tdm_repo: AbstractTdmPredictionRepository,
    time_jd: Time,
    duration: float,
    site: str,
    constellation: str,
) -> tuple[list[TdmPredictionPoint], int, float]:
    tdm_prediction_start = python_time.time()

    epoch = astropy_time_to_datetime_utc(time_jd)
    logger.info(
        f"Fetching TDM prediction points for epoch: {epoch}, "
        f"duration: {duration}s, site: {site!r}, constellation: {constellation!r}"
    )

    try:
        tdm_predictions, count, _ = tdm_repo.get_all_tdm_predictions_at_epoch(
            astropy_time_to_datetime_utc(time_jd),
            duration,
            site,
            constellation,
        )
        logger.info(
            f"get_all_tdm_predictions_at_epoch returned {len(tdm_predictions)} "
            f"predictions (total_count={count})"
        )

        prediction_ids = [p.id for p in tdm_predictions if p.id is not None]
        if prediction_ids:
            logger.info(
                f"Fetching prediction points for {len(prediction_ids)} "
                f"TDM prediction ids: {prediction_ids[:20]}"
            )
        else:
            logger.info("No TDM prediction ids — skipping point query")

        tdm_prediction_points = tdm_repo.get_tdm_prediction_points(prediction_ids)
        logger.info(
            f"get_tdm_prediction_points returned {len(tdm_prediction_points)} points"
        )

    except Exception as e:
        logger.error(
            f"Failed to retrieve TDM prediction points: {str(e)}",
            exc_info=True,
        )
        raise

    tdm_prediction_time = python_time.time() - tdm_prediction_start

    return tdm_prediction_points, count, tdm_prediction_time


def _check_cache_for_results(
    cache_key: str,
    start_time: float,
    api_source: str,
    api_version: str,
    group_by: str,
    *,
    ra: float | None = None,
    dec: float | None = None,
    fov_radius: float | None = None,
    duration: float | None = None,
    location: EarthLocation | None = None,
) -> dict[str, Any] | None:
    """
    Check cache for FOV calculation results and return formatted data if found.

    Args:
        cache_key: Unique key for the cache entry
        start_time: Start time for performance calculation
        api_source: Source of the API call
        api_version: Version of the API
        group_by: Grouping strategy for results
        ra: RA in degrees (for logging)
        dec: Dec in degrees (for logging)
        fov_radius: FOV radius in degrees (for logging)
        duration: Duration in seconds (for logging)
        location: Observer location (for logging)

    Returns:
        dict[str, Any] | None: Formatted cached results if found, None otherwise
    """
    skip_cache = True

    cached_data = get_cached_data(cache_key)

    if cached_data and not skip_cache:  # pragma: no cover
        cache_time = python_time.time() - start_time
        points_in_fov = cached_data["points_in_fov"]
        if (
            location is not None
            and ra is not None
            and dec is not None
            and fov_radius is not None
            and duration is not None
        ):
            logger.info(
                f"FOV completed: RA={ra}° Dec={dec}° radius={fov_radius}° "
                f"duration={duration}s "
                f"lat={location.lat.value}° lon={location.lon.value}° "
                f"height={location.height.value}m {points_in_fov} points in FOV, "
                f"{cache_time:.2f}s (cache hit)"
            )
        else:
            logger.info(
                f"FOV completed: {points_in_fov} points in FOV, "
                f"{cache_time:.2f}s (cache hit)"
            )
        logger.debug(
            f"Cache hit: Found {len(cached_data['results'])} results with "
            f"{points_in_fov} points in FOV"
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

    logger.debug("Cache miss - calculating FOV results")
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
    logger.debug(
        f"Caching {len(all_results)} results with {points_in_fov} points in FOV"
    )
    try:
        set_cached_data(cache_key, cache_data)
        logger.debug("Successfully cached results")
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
    logger.debug(f"Checking {len(jd_times)} time points")
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
    logger.debug(f"Starting FOV calculation at: {datetime.now().isoformat()}")

    logger.debug(f"FOV calculation mode: {'async' if async_mode else 'sync'}")

    logger.debug(f"FOV Parameters: RA={ra}°, Dec={dec}°, Radius={fov_radius}°")
    logger.debug(f"Duration: {duration} seconds")
    logger.debug(
        f"Location: lat={location.lat.value}°, "
        f"lon={location.lon.value}°, "
        f"height={location.height.value}m"
    )
    logger.debug(
        f"Time parameters: mid_obs_time={mid_obs_time_jd}, start_time={start_time_jd}"
    )
    logger.debug(
        f"Group by: {group_by}, Include TLEs: {include_tles}, Skip cache: {skip_cache}"
    )


def _calculate_performance_metrics(
    total_time: float,
    retrieval_time: float,
    calc_time: float,
    satellites_processed: int,  # TODO change to objects processed or allow for both
    points_in_fov: int,
    jd_times: np.ndarray,
    count: int,
    execution_time: float,
) -> dict[str, Any]:
    """
    Calculate and log performance metrics for FOV calculations.

    Args:
        total_time: Total execution time in seconds
        retrieval_time: Time spent retrieving orbital data in seconds
        calc_time: Time spent on propagation (or other FOV)
        calculations in seconds
        satellites_processed: Number of satellites processed
        points_in_fov: Number of points found in field of view
        jd_times: List of Julian day times used in calculations
        count: Total number of satellites available
        execution_time: Time spent on propagation execution

    Returns:
        dict[str, Any]: Performance metrics dictionary
    """
    # Log performance metrics
    logger.debug("\nPerformance Metrics:")
    logger.debug(f"Total execution time: {total_time:.2f} seconds")
    logger.debug(
        f"Data retrieval time: {retrieval_time:.2f} seconds "
        f"({(retrieval_time/total_time)*100:.1f}%)"
    )
    logger.debug(
        f"Calculation time: {calc_time:.2f} seconds "
        f"({(calc_time/total_time)*100:.1f}%)"
    )
    logger.debug("\nResults Summary:")
    logger.debug(f"Satellites processed: {satellites_processed}/{count}")
    logger.debug(f"Points in FOV: {points_in_fov}")
    logger.debug(f"End time: {datetime.now().isoformat()}")

    performance_metrics = {
        "total_time": round(total_time, 3),
        "data_retrieval_time": round(retrieval_time, 3),
        "calculation_time": round(execution_time, 3),
        "satellites_processed": satellites_processed,
        "points_in_fov": points_in_fov,
        "jd_times": jd_times.tolist(),
    }

    return performance_metrics
