"""
Celery tasks for FOV (Field of View) calculations.

This module provides asynchronous FOV processing capabilities to handle
long-running satellite propagation calculations without blocking the API.

Parallelism is achieved via Celery chord: each batch runs as a separate task
on its own worker, and a callback aggregates results.
"""

import logging
from typing import Any

from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.celery_app import celery
from api.entrypoints.v1.routes import api_source, api_version
from api.utils.output_utils import fov_data_to_json
from api.utils.propagation_strategies import process_satellite_batch

logger = logging.getLogger(__name__)


@celery.task(name="fov.process_satellite_batch")
def process_satellite_batch_task(
    serialized_batch_tles: list[dict[str, Any]],
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
    batch_tles = SqlAlchemyTLERepository.deserialize_tles(serialized_batch_tles)
    args = (
        batch_tles,
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
    tle_time: float,
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
        "total_time": round(tle_time + propagation_time, 3),
        "tle_time": round(tle_time, 3),
        "propagation_time": round(propagation_time, 3),
        "satellites_processed": satellites_processed,
        "points_in_fov": points_in_fov,
        "jd_times": jd_times,
    }

    return all_results, points_in_fov, group_by, performance_metrics


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
