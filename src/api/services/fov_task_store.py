"""Shared Postgres-backed store for async FOV task status and results.

Each replica runs its own Redis sidecar as the Celery result backend, so a
task's state is only visible on the pod that executed it. When the status
request is load-balanced to a different pod, ``AsyncResult`` reports ``PENDING``
forever even though the task completed elsewhere.

This module persists the terminal status and the fully-formatted response
payload in the shared Postgres database (keyed by the job id returned to the
client) so the status endpoint can answer from any replica.

All functions degrade gracefully: a database error is logged and swallowed
rather than propagated into the request or the Celery task, so this store never
becomes a hard dependency for submission or execution.
"""

import logging
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Any

logger = logging.getLogger(__name__)


@contextmanager
def _session():
    """Yield a SQLAlchemy session bound to the shared Postgres engine.

    Mirrors the pattern used by the FOV Celery tasks so the same helper works
    from both the web process and a Celery worker. The session and app context
    are always torn down, even on error, so a failed commit never leaks a
    pooled connection.
    """
    from sqlalchemy.orm import Session as SASession

    from api import app
    from api.entrypoints.extensions import db

    with app.app_context():
        with SASession(db.engine) as session:
            yield session


def create_pending(task_id: str) -> None:
    """Record a newly submitted task as PENDING (no-op if a row exists)."""
    from api.adapters.database_orm import FovTaskResultDb

    try:
        with _session() as session:
            if session.get(FovTaskResultDb, task_id) is None:
                session.add(FovTaskResultDb(task_id=task_id, status="PENDING"))
                session.commit()
    except Exception as e:
        logger.error(f"fov_task_store.create_pending failed for {task_id}: {e}")


def store_success(task_id: str, result: dict[str, Any]) -> None:
    """Persist a completed task's formatted result payload."""
    from api.adapters.database_orm import FovTaskResultDb

    try:
        with _session() as session:
            row = session.get(FovTaskResultDb, task_id)
            if row is None:
                row = FovTaskResultDb(task_id=task_id)
                session.add(row)
            row.status = "SUCCESS"
            row.result = result
            row.error = None
            session.commit()
    except Exception as e:
        logger.error(f"fov_task_store.store_success failed for {task_id}: {e}")


def store_failure(task_id: str, error: str) -> None:
    """Persist a failed task's error message.

    Never downgrades a row that already recorded SUCCESS: a late error callback
    must not clobber a result that completed successfully.
    """
    from api.adapters.database_orm import FovTaskResultDb

    try:
        with _session() as session:
            row = session.get(FovTaskResultDb, task_id)
            if row is not None and row.status == "SUCCESS":
                return
            if row is None:
                row = FovTaskResultDb(task_id=task_id)
                session.add(row)
            row.status = "FAILURE"
            row.error = error
            session.commit()
    except Exception as e:
        logger.error(f"fov_task_store.store_failure failed for {task_id}: {e}")


def get_result(task_id: str) -> dict[str, Any] | None:
    """Return the stored status/result for a task.

    Returns a response-ready dict (status plus, for SUCCESS, the formatted FOV
    payload), or ``None`` if no row exists for this id.
    """
    from api.adapters.database_orm import FovTaskResultDb

    try:
        with _session() as session:
            row = session.get(FovTaskResultDb, task_id)
            if row is None:
                return None
            # Copy out while the session is still open; the objects are
            # detached once the context exits.
            status = row.status
            result = row.result
            error = row.error
    except Exception as e:
        logger.error(f"fov_task_store.get_result failed for {task_id}: {e}")
        return None

    if status == "SUCCESS" and isinstance(result, dict):
        response = dict(result)
        response["task_id"] = task_id
        return response
    if status == "FAILURE":
        return {
            "status": "FAILURE",
            "error": error or "Task failed with unknown error",
            "task_id": task_id,
            "message": "FOV calculation failed",
        }
    return {
        "status": "PENDING",
        "message": "Task is waiting to be processed",
        "task_id": task_id,
    }


def delete_expired(retention_hours: int) -> int:
    """Delete task rows older than ``retention_hours``. Returns rows removed.

    Postgres has no TTL, so without this the table grows unbounded (the old
    Redis result backend expired results automatically). The DELETE is keyed on
    the indexed ``created_at`` column and is idempotent, so it is safe to run
    concurrently from every worker and pod without a lock.
    """
    from api.adapters.database_orm import FovTaskResultDb

    cutoff = datetime.now(timezone.utc) - timedelta(hours=retention_hours)
    try:
        with _session() as session:
            deleted = (
                session.query(FovTaskResultDb)
                .filter(FovTaskResultDb.created_at < cutoff)
                .delete(synchronize_session=False)
            )
            session.commit()
            return int(deleted)
    except Exception as e:
        logger.error(f"fov_task_store.delete_expired failed: {e}")
        return 0


def scheduled_fov_cleanup_job() -> None:
    """APScheduler entry point: prune expired async FOV task rows.

    Depends only on Postgres (no Redis), so it keeps working during a cache
    outage. Retention is read from config so it can be tuned without touching
    the schedule.
    """
    try:
        from api.config import FOV_RESULT_RETENTION_HOURS

        deleted = delete_expired(FOV_RESULT_RETENTION_HOURS)
        if deleted:
            logger.info(f"FOV task cleanup removed {deleted} expired row(s)")
    except Exception as e:
        logger.error(f"Error in scheduled FOV cleanup: {e}", exc_info=True)


def register_fov_cleanup_job(interval_hours: int = 1) -> None:
    """Register the periodic FOV cleanup job with the shared APScheduler.

    Mirrors the cache-refresh registration: a fixed job id, interval trigger,
    and ``replace_existing`` so re-running startup in each gunicorn worker does
    not create duplicates.
    """
    from api.entrypoints.extensions import scheduler

    job_id = "fov_task_cleanup"
    if any(job.id == job_id for job in scheduler.get_jobs()):
        logger.info(f"FOV cleanup job '{job_id}' already exists, not adding again")
        return
    try:
        scheduler.add_job(
            func=scheduled_fov_cleanup_job,
            trigger="interval",
            id=job_id,
            hours=interval_hours,
            misfire_grace_time=900,  # 15 min grace time
            replace_existing=True,
        )
        logger.info(f"Added FOV task cleanup job '{job_id}' (every {interval_hours}h)")
    except Exception as e:
        logger.error(f"Failed to schedule FOV cleanup job: {e}")
