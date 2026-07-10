"""
Celery tasks for FOV (Field of View) calculations.

This module provides asynchronous FOV processing capabilities to handle
long-running satellite propagation calculations without blocking the API.

Parallelism is achieved via Celery chord: each batch runs as a separate task
on its own worker, and a callback aggregates results. After aggregation, a
refinement task replaces TLE-based positions with Krogh-interpolated positions
for any satellites whose ephemeris data is available.
"""

import logging
import time as python_time
from typing import Any

import numpy as np

from api.celery_app import celery
from api.entrypoints.v1.routes import api_source, api_version
from api.utils.orbital_data_utils import deserialize_orbital_data_batch
from api.utils.output_utils import fov_data_to_json
from api.utils.propagation_strategies import (
    KroghPropagationStrategy,
    process_satellite_batch,
    satellite_position_fov,
)

logger = logging.getLogger(__name__)


@celery.task(name="fov.process_satellite_batch")
def process_satellite_batch_task(
    serialized_batch_orbital_data: list[dict[str, Any]],
    jd_times: list[float],
    location_lat: float,
    location_lon: float,
    location_height: float,
    fov_center: tuple[float, float],
    fov_radius: float,
    include_tles: bool,
    illuminated_only: bool,
) -> tuple[list[dict[str, Any]], int, float]:
    """
    Process a single batch of satellites for FOV calculation.

    Each batch runs on its own Celery worker.
    Returns (batch_results, satellites_processed, execution_time).
    """
    batch_orbital_data = deserialize_orbital_data_batch(serialized_batch_orbital_data)
    args = (
        batch_orbital_data,
        jd_times,
        location_lat,
        location_lon,
        location_height,
        fov_center,
        fov_radius,
        include_tles,
        illuminated_only,
    )
    return process_satellite_batch(args)


@celery.task(name="fov.aggregate_fov_results")
def aggregate_fov_results_task(
    group_results: list[tuple[list[dict[str, Any]], int, float]],
    group_by: str,
    orbital_data_time: float,
    jd_times: list[float],
) -> tuple[list[dict[str, Any]], int, str, dict[str, object]]:
    """
    Aggregate batch results from chord group into final FOV response format.

    propagation_time is the sum of batch execution times (CPU time across
    workers; when batches run in parallel, wall clock < propagation_time).
    """
    all_results = []
    satellites_processed = 0
    propagation_time = 0.0
    for batch_results, batch_sats, batch_time in group_results:
        all_results.extend(batch_results)
        satellites_processed += batch_sats
        propagation_time += batch_time

    points_in_fov = len(all_results)

    performance_metrics = {
        "total_time": round(orbital_data_time + propagation_time, 3),
        "data_retrieval_time": round(orbital_data_time, 3),
        "calculation_time": round(propagation_time, 3),
        "satellites_processed": satellites_processed,
        "points_in_fov": points_in_fov,
        "jd_times": jd_times,
    }

    return all_results, points_in_fov, group_by, performance_metrics


@celery.task(name="fov.refine_with_ephemeris")
def refine_with_ephemeris_task(
    aggregate_result: tuple,
    jd_times: list[float],
    location_lat: float,
    location_lon: float,
    location_height: float,
    ra: float,
    dec: float,
    fov_radius: float,
) -> tuple[list[dict[str, Any]], int, str, dict[str, object]]:
    """
    Refine FOV results by replacing TLE-propagated positions with
    Krogh-interpolated positions for satellites with available ephemeris data.

    Receives the aggregated TLE results and uses the set of NORAD IDs found in
    the FOV as a filter — only those satellites are queried for ephemeris data.
    For each satellite with ephemeris, Krogh propagation replaces the original
    TLE-based entries in the result set.

    Returns the same (all_results, points_in_fov, group_by, performance_metrics)
    format as aggregate_fov_results_task so get_fov_task_status needs no changes.
    """
    # Defer Flask-context imports to avoid circular imports at module load time
    from sqlalchemy.orm import Session as SASession

    from api import app
    from api.adapters.repositories.ephemeris_repository import (
        SqlAlchemyEphemerisRepository,
    )
    from api.entrypoints.extensions import db
    from api.utils import output_utils
    from api.utils.time_utils import ensure_datetime

    all_results, points_in_fov, group_by, performance_metrics = aggregate_result

    if not all_results:
        return aggregate_result

    refine_start = python_time.time()

    with app.app_context():
        # Mask password in log
        try:
            masked_url = db.engine.url.render_as_string(hide_password=True)
        except Exception:
            masked_url = "<unavailable>"
        logger.info(f"refine_with_ephemeris_task: connecting to DB: {masked_url}")

        session = SASession(db.engine)
        ephemeris_repo = SqlAlchemyEphemerisRepository(session)

        # Before returning results, log any None values
        for idx, result in enumerate(all_results):
            for key, value in result.items():
                if value is None:
                    logger.warning(
                        f"Found None value in result {idx}, "
                        f"field {key} before returning"
                    )

        # Process ephemeris data for satellites that were initially processed
        # with TLE data. Only process each unique norad_id once and replace
        # original TLE results
        unique_norad_ids = set()
        for result in all_results:
            if result.get("norad_id") is not None:
                unique_norad_ids.add(result["norad_id"])

        # Batch lookup all ephemeris data at once
        satellite_numbers = [str(norad_id) for norad_id in unique_norad_ids]
        epoch = ensure_datetime(jd_times[0])
        logger.info(
            f"Querying ephemeris for {len(satellite_numbers)} satellites "
            f"at epoch {epoch} (jd={jd_times[0]}), "
            f"norad_ids={satellite_numbers}"
        )
        ephemeris_dict = ephemeris_repo.get_closest_by_satellite_numbers(
            satellite_numbers,
            epoch,
        )

        logger.info(
            f"Found ephemeris data for {len(ephemeris_dict)} out of "
            f"{len(unique_norad_ids)} satellites — "
            f"keys={list(ephemeris_dict.keys())}"
        )

        for norad_id in satellite_numbers:
            krogh_strategy = KroghPropagationStrategy()

            ephemeris = ephemeris_dict.get(int(norad_id))

            # Skip if no ephemeris data found
            if ephemeris is None:
                key_types = [type(k).__name__ for k in ephemeris_dict.keys()]
                logger.info(
                    f"No ephemeris in dict for satellite {norad_id} "
                    f"(int key={int(norad_id)}, dict key types={key_types})"
                )
                continue

            logger.info(
                f"Satellite {norad_id}: found ephemeris id={ephemeris.id}, "
                f"generated_at={ephemeris.generated_at}"
            )

            try:
                krogh_strategy.load_ephemeris(ephemeris, ephemeris_repo)
                logger.info(f"Satellite {norad_id}: load_ephemeris succeeded")
            except Exception as e:
                logger.error(f"Error loading ephemeris for satellite {norad_id}: {e}")
                continue

            try:
                # Propagate positions
                positions = krogh_strategy.propagate(
                    jd_times,
                    None,
                    location_lat,
                    location_lon,
                    location_height,
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

                tle_entries_for_sat = [
                    r for r in all_results if r.get("norad_id") == int(norad_id)
                ]
                logger.info(
                    f"Satellite {norad_id}: {len(replacement_results)} Krogh "
                    f"positions in FOV, replacing "
                    f"{len(tle_entries_for_sat)} TLE entries"
                )

                if not replacement_results:
                    # Krogh propagation succeeded but placed the satellite
                    # outside the FOV — keep the TLE-based entries as fallback
                    # rather than silently dropping the satellite from results
                    logger.warning(
                        f"Satellite {norad_id}: Krogh found 0 positions in FOV "
                        f"— retaining {len(tle_entries_for_sat)} TLE entries"
                    )
                    continue

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

        session.close()

    refine_time = python_time.time() - refine_start

    updated_metrics = {
        **performance_metrics,
        "total_time": round(performance_metrics.get("total_time", 0) + refine_time, 3),
        "ephemeris_refinement_time": round(refine_time, 3),
        "points_in_fov": points_in_fov,
    }

    return all_results, points_in_fov, group_by, updated_metrics


def get_fov_task_status(task_id: str) -> dict[str, Any]:
    """
    Get the status of a FOV calculation task.

    Args:
        task_id: The Celery task ID

    Returns:
        dict: Task status and result if available
    """
    try:
        task = celery.AsyncResult(task_id)

        # Check if task exists
        if task.state == "PENDING":
            return {
                "status": "PENDING",
                "message": "Task is waiting to be processed",
                "task_id": task_id,
            }
        elif task.state == "PROGRESS":
            return {
                "status": "PROGRESS",
                "message": task.info.get("status", "Processing..."),
                "progress": task.info.get("progress", 0),
                "task_id": task_id,
            }
        elif task.state == "SUCCESS":
            # Format the result properly for the API response
            result = task.result

            if isinstance(result, (list, tuple)) and len(result) >= 4:  # noqa: PLR2004
                all_results = result[0]
                points_in_fov = result[1]
                group_by = result[2]
                performance_metrics = result[3]

                # If result is a list of satellite passes, format it properly
                formatted_result = fov_data_to_json(
                    all_results,
                    points_in_fov,
                    performance_metrics,
                    api_source,
                    api_version,
                    group_by,
                )

                # Add task metadata to the formatted result
                formatted_result.update(
                    {
                        "task_id": task_id,
                        "status": "SUCCESS",
                        "message": "FOV calculation completed successfully",
                    }
                )
                return formatted_result
            else:
                return {
                    "status": "SUCCESS",
                    "result": result,
                    "task_id": task_id,
                    "message": "FOV calculation completed successfully",
                }
        elif task.state == "FAILURE":
            error_info = task.info
            error_message = (
                str(error_info) if error_info else "Task failed with unknown error"
            )
            return {
                "status": "FAILURE",
                "error": error_message,
                "task_id": task_id,
                "message": "FOV calculation failed",
            }
        else:
            return {
                "status": task.state,
                "message": f"Unknown task state: {task.state}",
                "task_id": task_id,
            }
    except Exception as e:
        logger.error(f"Error checking task status for {task_id}: {str(e)}")
        return {
            "status": "ERROR",
            "error": f"Failed to check task status: {str(e)}",
            "task_id": task_id,
            "message": "Error occurred while checking task status",
        }
