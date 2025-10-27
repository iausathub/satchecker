"""
Celery tasks for FOV (Field of View) calculations.

This module provides asynchronous FOV processing capabilities to handle
long-running satellite propagation calculations without blocking the API.
"""

import logging
from typing import Any

import astropy.units as u
import numpy as np
from astropy.coordinates import EarthLocation

from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.celery_app import celery
from api.entrypoints.v1.routes import api_source, api_version
from api.utils.output_utils import fov_data_to_json
from api.utils.propagation_strategies import FOVParallelPropagationStrategy

logger = logging.getLogger(__name__)


@celery.task(bind=True, name="fov.calculate_satellite_passes")
def calculate_satellite_passes_async(
    self,
    ra: float,
    dec: float,
    fov_radius: float,
    serialized_tles: list[dict[str, Any]],
    jd_times: list[float],
    location_lat: float,
    location_lon: float,
    location_height: float,
    include_tles: bool,
    batch_size: int,
    illuminated_only: bool,
    group_by: str,
    tle_time: float,
) -> tuple[list[dict[str, Any]], int, None]:
    """
    Asynchronously calculate satellite passes within a specified field of view (FOV).

    This Celery task performs parallel satellite propagation to determine which
    satellites pass through a given FOV during specified time periods and include
    progress updates when the task is checked with the task status endpoint.

    Args:
        self: Celery task instance (bound=True)
        ra (float): Right ascension of FOV center in degrees
        dec (float): Declination of FOV center in degrees
        fov_radius (float): Radius of the field of view in degrees
        serialized_tles (list[dict[str, Any]]): Serialized TLE data for satellites
        jd_times (list[float]): Julian day times for propagation calculations
        location_lat (float): Observer latitude in degrees
        location_lon (float): Observer longitude in degrees
        location_height (float): Observer height above sea level in meters
        include_tles (bool): Whether to include TLE data in results
        batch_size (int): Number of satellites to process per batch
        illuminated_only (bool): Filter for only illuminated satellites
        group_by (str): Method for grouping results (e.g., 'satellite', 'time')
        tle_time (float): Time spent on TLE processing for performance metrics

    Returns:
        tuple[list[dict[str, Any]], int, None]: A tuple containing:
            - List of satellite pass results with position and timing data
            - Number of points found within the FOV
            - Grouping method (group_by parameter)
            - Performance metrics including processing times and statistics

    Raises:
        Exception: If propagation fails or encounters errors during processing

    Note:
        This task provides real-time progress updates via Celery's task state mechanism.
        Progress can be monitored using the task ID returned when the task is submitted.
    """
    # Deserialize TLEs from the serialized format
    all_tles = SqlAlchemyTLERepository.deserialize_tles(serialized_tles)

    location = EarthLocation(
        lat=location_lat * u.deg, lon=location_lon * u.deg, height=location_height * u.m
    )
    all_results = []
    points_in_fov = 0
    satellites_processed = 0

    prop_strategy = FOVParallelPropagationStrategy()

    try:
        self.update_state(
            state="PROGRESS",
            meta={
                "status": "Starting FOV calculation",
                "progress": 0,
                "total_satellites": len(all_tles),
            },
        )

        logger.info("Starting parallel propagation with batch size 250")

        # Allow multithreaded propagation to update task state
        def progress_callback(
            progress_percent, completed_batches, total_batches, satellites_processed
        ):
            self.update_state(
                state="PROGRESS",
                meta={
                    "status": f"Processing batch {completed_batches}/{total_batches}",
                    "progress": progress_percent,
                    "satellites_processed": satellites_processed,
                    "total_satellites": len(all_tles),
                },
            )

        results, execution_time, satellites_processed = prop_strategy.propagate(
            all_tles=all_tles,
            jd_times=np.array(jd_times),
            location=location,
            fov_center=(ra, dec),
            fov_radius=fov_radius,
            batch_size=250,
            include_tles=include_tles,
            illuminated_only=illuminated_only,
            progress_callback=progress_callback,
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

        logger.info(
            f"Task completed: {points_in_fov} points in FOV, "
            f"{satellites_processed} satellites processed"
        )

    except Exception as e:
        logger.error(f"Error in parallel FOV processing: {str(e)}", exc_info=True)
        logger.error(f"Failed after processing {satellites_processed} satellites")
        satellites_processed = 0  # Set a default value in case of error
        raise

    performance_metrics = {
        "total_time": round(tle_time + execution_time, 3),
        "tle_time": round(tle_time, 3),
        "propagation_time": round(execution_time, 3),
        "satellites_processed": satellites_processed,
        "points_in_fov": points_in_fov,
        "jd_times": jd_times,
    }

    # Return the results
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
        task = calculate_satellite_passes_async.AsyncResult(task_id)

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

            if isinstance(result, list):
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
