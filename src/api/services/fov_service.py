# mypy: disable-error-code=unreachable
import logging
import time as python_time
from datetime import datetime
from typing import Any, Optional

import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from skyfield.api import EarthSatellite, load, wgs84

from api.adapters.repositories.ephemeris_repository import AbstractEphemerisRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository

# from api.domain.models.interpolator_splines import InterpolatorSplines
from api.services.cache_service import (
    create_fov_cache_key,
    set_cached_data,
)
from api.utils import coordinate_systems, output_utils
from api.utils.propagation_strategies import (
    FOVParallelPropagationStrategy,
    KroghPropagationStrategy,
    satellite_position_fov,
    # FOVPropagationStrategy,
)
from api.utils.time_utils import astropy_time_to_datetime_utc, ensure_datetime

logger = logging.getLogger(__name__)


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
        api_source: Source of the API call
        api_version: Version of the API

    Returns:
        dict: Formatted results either grouped by satellite or chronologically
    """
    start_time = python_time.time()
    logger.info(f"Starting FOV calculation at: {datetime.now().isoformat()}")
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
    skip_cache = True

    cached_data = None  # get_cached_data(cache_key)

    if cached_data:  # pragma: no cover
        logger.info(  # type: ignore[unreachable]
            f"Cached data found with {len(cached_data.get('results', []))} results and "
            f"{cached_data.get('points_in_fov', 0)} points in FOV"
        )
        # Log structure details for debugging
        for key in cached_data:
            if isinstance(cached_data[key], (list, dict)):
                logger.debug(
                    f"Cached {key}: {type(cached_data[key])} "
                    f"with length {len(cached_data[key])}"
                )
            else:
                logger.debug(
                    f"Cached {key}: {type(cached_data[key])} = {cached_data[key]}"
                )  # noqa: E501
    else:
        logger.info("No cached data found")
    logger.info(f"Cached data: {cached_data}")

    # TODO: Re-enable caching - this block is intentionally unreachable for now
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
    # Get all current TLEs
    tle_start = python_time.time()
    time_param = mid_obs_time_jd if mid_obs_time_jd is not None else start_time_jd
    logger.info(f"Fetching TLEs for epoch: {astropy_time_to_datetime_utc(time_param)}")

    try:
        tles, count, _ = tle_repo.get_all_tles_at_epoch(
            astropy_time_to_datetime_utc(time_param),
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

    # Pre-compute time arrays and constants
    time_step = 1 / 86400  # 1 second
    duration_jd = duration / 86400

    prop_start = python_time.time()
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

    all_results = []
    points_in_fov = 0
    satellites_processed = 0

    # Get ephemeris for all satellites in the time range
    tles_to_propagate = tles
    """
    satellites_with_ephemeris = ephemeris_repo.get_satellites_with_ephemeris(
        ensure_datetime(jd_times[0]),
        ensure_datetime(jd_times[-1]),
    )
    logger.info(f"Satellites with ephemeris: {len(satellites_with_ephemeris)}")

    satellite_numbers_with_ephemeris = set(satellites_with_ephemeris)

    for tle in tles:
        if tle.satellite.sat_number not in satellite_numbers_with_ephemeris:
            tles_to_propagate.append(tle)

    # TODO: Change to getting all interpolator splines at the epoch instead
    # of getting each ephemeris

    # Process Starlink satellites with Krogh propagation (sequential for now)
    if satellites_with_ephemeris:
        logger.info(
            f"Processing {len(satellites_with_ephemeris)} Starlink satellites "
            f"with Krogh propagation"
        )

        krogh_strategy = KroghPropagationStrategy()
        for i, satellite_number in enumerate(satellites_with_ephemeris):
            try:
                # Load ephemeris data for this Starlink satellite
                logger.info(f"Satellite number: {satellite_number}")
                ephemeris = ephemeris_repo.get_closest_by_satellite_number(
                    str(satellite_number),
                    ensure_datetime(jd_times[0]),
                )
                logger.info(f"Ephemeris: {ephemeris}")

                # Skip if no ephemeris data found
                if ephemeris is None:
                    logger.warning(
                        f"No ephemeris data found for Starlink satellite "
                        f"{satellite_number}"
                    )
                    satellites_processed += 1
                    continue

                try:
                    krogh_strategy.load_ephemeris(ephemeris, ephemeris_repo)
                except Exception as e:
                    logger.error(
                        f"Error loading ephemeris for satellite {satellite_number}: {e}"
                    )
                    satellites_processed += 1
                    continue

                try:
                    # create a new InterpolatorSplines object to save to the database
                    # Convert Julian dates to datetime objects
                    splines_dict = krogh_strategy.interpolated_splines

                    time_range_start_dt = Time(
                        splines_dict["time_range"][0], format="jd"
                    ).datetime
                    time_range_end_dt = Time(
                        splines_dict["time_range"][1], format="jd"
                    ).datetime

                    interpolator_splines = InterpolatorSplines(
                        sat_id=krogh_strategy.ephemeris_data.satellite,
                        ephemeris_id=ephemeris.id,
                        time_range_start=time_range_start_dt,
                        time_range_end=time_range_end_dt,
                        generated_at=krogh_strategy.ephemeris_data.generated_at,
                        data_source=krogh_strategy.ephemeris_data.data_source,
                        method="krogh_chunked",
                        chunk_size=14,
                        overlap=8,
                        n_sigma_points=13,
                        date_collected=krogh_strategy.ephemeris_data.date_collected,
                        interpolated_splines=krogh_strategy.interpolated_splines,
                    )

                    ephemeris_repo.add_interpolator_splines(interpolator_splines)
                except Exception as e:
                    logger.error(
                        f"Error adding interpolator splines for satellite "
                        f"Error loading ephemeris for satellite "
                        f"{satellite_number}: {e}"
                    )
                    satellites_processed += 1
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
                except Exception as e:
                    logger.error(
                        f"Error propagating positions for satellite "
                        f"{satellite_number}: {e}"
                    )
                    satellites_processed += 1
                    continue

                # Check if positions are in FOV
                for pos in positions:
                    if pos.ra is not None and pos.dec is not None:
                        # Calculate angular distance from FOV center
                        angular_distance = np.sqrt(
                            (pos.ra - ra) ** 2 + (pos.dec - dec) ** 2
                        )
                        if angular_distance <= fov_radius:
                            # Create new satellite_position_fov with updated values
                            updated_pos = satellite_position_fov(
                                ra=pos.ra,
                                dec=pos.dec,
                                altitude=pos.altitude,
                                azimuth=pos.azimuth,
                                range_km=pos.range_km,
                                julian_date=pos.julian_date,
                                name=tle.satellite.sat_name,
                                norad_id=tle.satellite.sat_number,
                                propagation_epoch=output_utils.format_date(
                                    ephemeris.generated_at
                                ),
                                propagation_source="ephemeris",
                            )
                            result = updated_pos._asdict()

                            all_results.append(result)
                            points_in_fov += 1

                satellites_processed += 1

                # Progress logging
                if (i + 1) % 100 == 0:
                    logger.info(
                        f"Completed {i + 1}/{len(satellites_with_ephemeris)} satellites"
                    )

            except Exception as e:
                logger.error(
                    f"Error processing Starlink satellite {satellite_number}: {e}"
                )
                satellites_processed += 1
                continue
    """
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

    # Log performance metrics
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

    # Before returning results, log any None values
    for idx, result in enumerate(all_results):
        for key, value in result.items():
            if value is None:
                logger.warning(
                    f"Found None value in result {idx}, field {key} before returning"
                )

    # Process ephemeris data for satellites that were initially processed with TLE data
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
                    if angular_distance <= fov_radius:
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
                            propagation_epoch=output_utils.format_date(
                                ephemeris.generated_at
                            ),
                            propagation_source="ephemeris",
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
            logger.error(f"Error propagating positions for satellite {norad_id}: {e}")
            continue

    # Calculate final points_in_fov count after all processing
    points_in_fov = len(all_results)

    performance_metrics = {
        "total_time": round(total_time, 3),
        "tle_time": round(tle_time, 3),
        "propagation_time": round(prop_time, 3),
        "satellites_processed": satellites_processed,
        "points_in_fov": points_in_fov,
        "jd_times": jd_times.tolist(),
    }

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

    return json_result


def get_satellites_above_horizon(
    tle_repo: AbstractTLERepository,
    location: EarthLocation,
    julian_dates: list[Time],
    min_altitude: float,
    min_range: float,
    max_range: float,
    illuminated_only: bool = False,
    constellation: Optional[str] = None,
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
