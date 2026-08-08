import json
import logging
import threading
import time
from datetime import datetime, timezone
from typing import Any

from astropy.coordinates import EarthLocation
from astropy.time import Time
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import LockError
from redis.exceptions import TimeoutError as RedisTimeoutError

from api.entrypoints.extensions import db, redis_client, scheduler

# Use the application's centralized logging configuration
logger = logging.getLogger(__name__)

# Errors that indicate Redis is simply unreachable (e.g. the sidecar isn't
# ready yet after a pod restart). These are transient and self-heal once the
# connection pool reconnects, so they're logged quietly and without a traceback
# to avoid spamming logs during startup windows.
REDIS_UNAVAILABLE_ERRORS = (RedisConnectionError, RedisTimeoutError)

DEFAULT_CACHE_TTL = 3600  # 1 hour in seconds
RECENT_TLES_CACHE_KEY = "recent_tles"
RECENT_TDM_PREDICTIONS_CACHE_KEY = "recent_tdm_predictions"
RECENT_ORBITAL_ELEMENTS_CACHE_KEY = "recent_orbital_elements"

# Pod-local lock so only one gunicorn worker per pod runs the (heavy) cache
# refresh. Each pod has its own Redis sidecar, so this lock naturally scopes to
# the workers in the same pod - every pod still warms its own cache once.
CACHE_REFRESH_LOCK_KEY = "cache_refresh_lock"
CACHE_REFRESH_LOCK_TTL = 300  # seconds; auto-expires if a holder crashes


def _acquire_refresh_lock(ttl: int = CACHE_REFRESH_LOCK_TTL) -> tuple[Any, bool]:
    """Try to acquire the pod-local cache-refresh lock.

    Uses redis-py's built-in ``Lock`` (SET NX + a unique token, released with an
    atomic compare-and-delete)

    Returns a ``(lock, redis_reachable)`` tuple:
      * ``(lock, True)``  - we acquired the lock; pass ``lock`` to
        :func:`_release_refresh_lock` when done.
      * ``(None, True)``  - Redis is up but another worker holds the lock; skip
        the refresh (that worker is warming this pod's shared cache).
      * ``(None, False)`` - Redis is unreachable; the caller decides whether to
        retry (this is the pod-restart / sidecar-not-ready case).
    """
    if not redis_client:
        return None, False
    lock = redis_client.lock(CACHE_REFRESH_LOCK_KEY, timeout=ttl)
    try:
        acquired = lock.acquire(blocking=False)
        return (lock, True) if acquired else (None, True)
    except REDIS_UNAVAILABLE_ERRORS:
        return None, False
    except Exception as e:
        logger.debug(f"Could not acquire cache refresh lock: {e}")
        return None, False


def _release_refresh_lock(lock: Any) -> None:
    """Release the pod-local cache-refresh lock if we still own it."""
    if lock is None:
        return
    try:
        lock.release()
    except LockError:
        # The lock already expired or was taken over by another worker; there's
        # nothing of ours left to release.
        pass
    except Exception as e:
        logger.debug(f"Could not release cache refresh lock: {e}")


def _redis_is_ready() -> bool:
    """Return True if Redis is reachable (responds to a ping)."""
    if not redis_client:
        return False
    try:
        return bool(redis_client.ping())
    except Exception:
        return False


def _warm_cache_once(app) -> bool:
    """Warm the pod's cache once, guarded by the pod-local lock.

    Returns True if the cache is warm afterward - either because we refreshed it
    or because another worker in this pod already holds the lock and is doing so.
    Returns False if Redis was unreachable or the refresh failed.

    Args:
        app: The Flask application object to push an app context with.
    """
    lock, redis_reachable = _acquire_refresh_lock()
    if lock is None:
        # (None, True)  -> another worker is warming the shared cache: done.
        # (None, False) -> Redis unreachable: not warm.
        return redis_reachable
    try:
        with app.app_context():
            tle_ok = refresh_tle_cache()
            orbital_elements_ok = refresh_orbital_elements_cache()
        return bool(tle_ok and orbital_elements_ok)
    finally:
        _release_refresh_lock(lock)


def create_fov_cache_key(
    location: EarthLocation,
    mid_obs_time_jd: Time,
    start_time_jd: Time,
    duration: float,
    ra: float,
    dec: float,
    fov_radius: float,
    include_orbital_data: bool = False,
    constellation: str | None = None,
    data_source: str | None = None,
) -> str:
    """Create a unique cache key for the FOV calculation."""
    key_parts = [
        "fov",
        f"lat_{location.lat.value:.6f}",
        f"lon_{location.lon.value:.6f}",
        f"height_{location.height.value:.6f}",
        f"mid_time_{mid_obs_time_jd.jd if mid_obs_time_jd else 'None'}",
        f"start_time_{start_time_jd.jd if start_time_jd else 'None'}",
        f"duration_{duration}",
        f"ra_{ra}",
        f"dec_{dec}",
        f"radius_{fov_radius}",
        f"include_orbital_data_{include_orbital_data}",
        f"constellation_{constellation}",
        f"data_source_{data_source}",
    ]
    return ":".join(key_parts)


def get_cached_data(key: str, default: Any = None) -> Any:
    """Get data from cache
    Args:
        key: The cache key to retrieve the data for.
        default: The default value to return if the data is not found in the cache.
    Returns:
        The deserialized data from the cache or the default value if the data is not
        found in the cache.
    """
    if not redis_client:
        return default

    try:
        data = redis_client.get(key)
        if not data:
            return default
        # Cast to str to ensure mypy knows this is a string for json.loads
        return json.loads(str(data))
    except REDIS_UNAVAILABLE_ERRORS as e:
        # Redis is temporarily unreachable (e.g. still starting up after a pod
        # restart); fall back to the default without noisy logging.
        logger.debug(f"Redis unavailable for cache retrieval of key {key}: {e}")
        return default
    except Exception as e:
        logger.warning(f"Cache retrieval error for key {key}: {e}")
        return default


def set_cached_data(key: str, data: Any, ttl: int = DEFAULT_CACHE_TTL) -> bool:
    """Set data in cache with default or custom TTL.
    Args:
        key: The cache key to set the data for.
        data: The unserialized data to set in the cache.
        ttl: The time-to-live for the cache entry.
    Returns:
        True if the data was set successfully, False otherwise.
    """
    if not redis_client:
        return False

    try:
        serialized = json.dumps(data)
        serialized_size = len(serialized)

        # Log data structure details for debugging
        if isinstance(data, dict):
            if "results" in data:
                results_count = len(data["results"]) if data["results"] else 0
                logger.debug(
                    f"Caching {results_count} results in data structure "
                    f"for key {key}"
                )
            if "tles" in data:
                tles_count = len(data["tles"]) if data["tles"] else 0
                logger.debug(
                    f"Caching {tles_count} TLEs in data structure for key {key}"
                )
            if "orbital_elements" in data:
                orbital_elements_count = (
                    len(data["orbital_elements"]) if data["orbital_elements"] else 0
                )
                logger.debug(
                    f"Caching {orbital_elements_count} orbital elements in "
                    f"data structure for key {key}"
                )

        if serialized_size > 500 * 1024 * 1024:
            logger.warning(
                f"Data for key {key} is too large to cache "
                f"({serialized_size} bytes), skipping"
            )
            return False

        logger.debug(f"Attempting to cache data for key {key}: {serialized_size} bytes")
        redis_client.setex(key, ttl, serialized)

        # Immediately verify the data was cached successfully
        verification_data = redis_client.get(key)
        if verification_data:
            verified_data = json.loads(str(verification_data))
            if isinstance(verified_data, dict):
                if "results" in verified_data:
                    verified_count = (
                        len(verified_data["results"]) if verified_data["results"] else 0
                    )
                    logger.debug(
                        f"Verification: Retrieved {verified_count} results "
                        f"from cache for key {key}"
                    )
                if "tles" in verified_data:
                    verified_tles = (
                        len(verified_data["tles"]) if verified_data["tles"] else 0
                    )
                    logger.debug(
                        f"Verification: Retrieved {verified_tles} TLEs "
                        f"from cache for key {key}"
                    )
                if "orbital_elements" in verified_data:
                    verified_orbital_elements = (
                        len(verified_data["orbital_elements"])
                        if verified_data["orbital_elements"]
                        else 0
                    )
                    logger.debug(
                        f"Verification: Retrieved {verified_orbital_elements} "
                        f"orbital elements from cache for key {key}"
                    )

            logger.debug(f"Successfully cached and verified data for key {key}")
        else:
            logger.warning(
                "Cache verification failed - data not found immediately "
                f"after setex for key {key}"
            )
            return False

        return True
    except REDIS_UNAVAILABLE_ERRORS as e:
        # Redis is temporarily unreachable (e.g. still starting up after a pod
        # restart); skip caching without noisy logging or a traceback.
        logger.debug(f"Redis unavailable for cache set of key {key}: {e}")
        return False
    except Exception as e:
        logger.warning(f"Cache set error for key {key}: {e}", exc_info=True)
        return False


def refresh_tle_cache(session=None):
    """
    Refresh the TLE cache with current data from the database.
    Can be used both for initialization and scheduled updates.

    Args:
        session: Optional database session to use. If None, db.session will be used,
                which requires a Flask application context.
    """
    from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository

    try:
        logger.info(f"Refreshing TLE cache at {datetime.now(timezone.utc)}")

        # Create a new db session if one wasn't provided
        if session is None:
            from flask import current_app

            if not current_app:
                logger.error("No Flask app context available and no session provided")
                return False

            session = db.session

        tle_repo = SqlAlchemyTLERepository(session)

        # Current time as the epoch date
        epoch_date = datetime.now(timezone.utc)

        # Perform full TLE retrieval
        logger.info("Retrieving TLEs from database...")
        tles, count, _ = tle_repo._get_all_tles_at_epoch(epoch_date, 1, 100000, "json")
        logger.info(f"Retrieved {count} TLEs from database")

        # Serialize TLEs for JSON storage
        logger.info(f"Serializing {len(tles)} TLEs for caching")
        try:
            # Use the batch serialization for all TLEs
            serialized_tles = SqlAlchemyTLERepository.batch_serialize_tles(tles)
            logger.info(f"Successfully serialized {len(serialized_tles)} TLEs")
        except Exception as e:
            logger.error(f"Batch serialization failed: {e}", exc_info=True)
            return False

        # Cache the result
        cache_data = {
            "tles": serialized_tles,  # Use serialized TLEs
            "total_count": count,
            "cached_at": epoch_date.isoformat(),
        }

        # Set TTL to 3 hours
        ttl = 3 * 3600
        logger.info(f"Setting cache with TTL of {ttl} seconds")
        cache_result = set_cached_data(RECENT_TLES_CACHE_KEY, cache_data, ttl=ttl)

        if cache_result:
            logger.info(f"TLE cache refreshed with {len(serialized_tles)} entries")
        else:
            logger.warning("TLE data retrieved but caching failed")

        return cache_result

    except Exception as e:
        logger.error(f"Error refreshing TLE cache: {e}", exc_info=True)
        # Roll back any pending transactions
        if session and session.is_active:
            session.rollback()
        return False


def refresh_orbital_elements_cache(session=None):
    """
    Refresh the orbital elements cache with current data from the database.
    Can be used both for initialization and scheduled updates.

    Args:
        session: Optional database session to use. If None, db.session will be used,
                which requires a Flask application context.
    """
    from api.adapters.repositories.orbital_elements_repository import (
        SqlAlchemyOrbitalElementsRepository,
    )

    try:
        logger.info(
            f"Refreshing orbital elements cache at {datetime.now(timezone.utc)}"
        )

        # Create a new db session if one wasn't provided
        if session is None:
            from flask import current_app

            if not current_app:
                logger.error("No Flask app context available and no session provided")
                return False

            session = db.session

        orbital_elements_repo = SqlAlchemyOrbitalElementsRepository(session)

        # Current time as the epoch date
        epoch_date = datetime.now(timezone.utc)

        # Perform full orbital elements retrieval
        logger.info("Retrieving TLEs from database...")
        orbital_elements, count, _ = (
            orbital_elements_repo._get_all_orbital_elements_at_epoch(
                epoch_date, 1, 100000, "json"
            )
        )
        logger.info(f"Retrieved {count} TLEs from database")

        # Serialize orbital elements for JSON storage
        logger.info(f"Serializing {len(orbital_elements)} orbital elements for caching")
        try:
            # Use the batch serialization for all orbital elements
            serialized_orbital_elements = (
                SqlAlchemyOrbitalElementsRepository.batch_serialize_orbital_elements(
                    orbital_elements
                )
            )
            logger.info(
                f"Successfully serialized {len(serialized_orbital_elements)} "
                f"orbital elements"
            )
        except Exception as e:
            logger.error(f"Batch serialization failed: {e}", exc_info=True)
            return False

        # Cache the result
        cache_data = {
            "orbital_elements": serialized_orbital_elements,  # serialized
            "total_count": count,
            "cached_at": epoch_date.isoformat(),
        }

        # Set TTL to 3 hours
        ttl = 3 * 3600
        logger.info(f"Setting cache with TTL of {ttl} seconds")
        cache_result = set_cached_data(
            RECENT_ORBITAL_ELEMENTS_CACHE_KEY, cache_data, ttl=ttl
        )

        if cache_result:
            logger.info(
                f"Orbital elements cache refreshed with "
                f"{len(serialized_orbital_elements)} entries"
            )
        else:
            logger.warning("TLE data retrieved but caching failed")

        return cache_result

    except Exception as e:
        logger.error(f"Error refreshing TLE cache: {e}", exc_info=True)
        # Roll back any pending transactions
        if session and session.is_active:
            session.rollback()
        return False


# Define a global function for the scheduler to use
def scheduled_cache_refresh_job():
    """Global function for the scheduler job to refresh the cache"""
    try:
        # This job fires in every gunicorn worker's scheduler; the pod-local
        # lock ensures only one worker per pod actually runs the refresh. If the
        # lock isn't acquired (another worker has it, or Redis is unreachable),
        # skip - the holder warms the shared cache, or the next interval retries.
        lock, _ = _acquire_refresh_lock()
        if not lock:
            logger.debug("Scheduled cache refresh skipped; lock not acquired")
            return

        # Access the Flask app directly through the scheduler
        app = scheduler.app

        logger.info(
            f"Scheduled TLE cache refresh triggered at {datetime.now(timezone.utc)}"
        )

        # Execute refresh_tle_cache within the app context
        try:
            with app.app_context():
                logger.info("Running scheduled refresh with app context")
                refresh_tle_cache()
                refresh_orbital_elements_cache()
        finally:
            _release_refresh_lock(lock)
    except Exception as e:
        logger.error(f"Error in scheduled cachedata refresh: {e}", exc_info=True)


# Global flag to track if the initial refresh has been done
_initial_cache_refresh_done = False

# Guards against spawning more than one background warmup thread per worker.
_cache_warmup_thread_started = False
_cache_warmup_lock = threading.Lock()


def _start_background_cache_warmup(app, interval: int = 5, max_wait: int = 600) -> None:
    """Warm the cache in the background once Redis becomes ready.

    Spawned only when Redis isn't reachable at startup. Runs in a daemon thread
    so it never blocks worker startup or shutdown: it pings Redis every
    ``interval`` seconds until it's ready (or ``max_wait`` elapses), then warms
    the cache once.

    Args:
        app: The Flask application object (not a proxy) to push a context with.
        interval: Seconds to wait between readiness pings.
        max_wait: Maximum total seconds to wait for Redis before giving up.
    """
    global _cache_warmup_thread_started

    with _cache_warmup_lock:
        if _cache_warmup_thread_started:
            return
        _cache_warmup_thread_started = True

    def _run() -> None:
        global _initial_cache_refresh_done, _cache_warmup_thread_started
        deadline = time.monotonic() + max_wait
        try:
            # Wait for Redis to come up (e.g. the sidecar finishing its restart).
            while not _redis_is_ready():
                if time.monotonic() >= deadline:
                    logger.warning(
                        f"Cache warmup gave up after {max_wait}s; Redis not ready"
                    )
                    return
                time.sleep(interval)

            if _warm_cache_once(app):
                _initial_cache_refresh_done = True
                logger.info("Cache warmed once Redis became available")
            else:
                logger.warning("Cache warmup ran but the refresh did not complete")
        finally:
            # Allow a future attempt to spawn a new thread if this one exited
            # without warming the cache.
            with _cache_warmup_lock:
                _cache_warmup_thread_started = False

    threading.Thread(target=_run, name="cache-warmup", daemon=True).start()


def initialize_cache_refresh_scheduler(hours=3):
    """Set up a scheduled job to refresh TLE cache every X hours"""
    global _initial_cache_refresh_done

    # Use a fixed job ID that's easier to check
    job_id = "cache_refresh_task"

    existing_jobs = scheduler.get_jobs()
    job_exists = any(job.id == job_id for job in existing_jobs)

    if job_exists:
        logger.info(
            f"Cache refresh scheduler job '{job_id}' already exists, not adding again"
        )
    else:
        try:
            scheduler.add_job(
                func=scheduled_cache_refresh_job,
                trigger="interval",
                id=job_id,
                hours=hours,
                misfire_grace_time=900,  # 15 min grace time
                replace_existing=True,  # Replace if it somehow exists
            )
            logger.info(
                f"Added cache refresh scheduler job '{job_id}' "
                f"with interval {hours} hours"
            )

            scheduler.add_job(
                func=check_redis_memory,
                trigger="interval",
                id="redis_memory_check",
                hours=1,  # Check every hour
                misfire_grace_time=300,  # 5 min grace time
                replace_existing=True,
            )
            logger.info("Added Redis memory check scheduler job")
        except Exception as e:
            logger.error(f"Failed to schedule cache refresh job: {e}")

    # Don't perform the refresh here; the caller passes in the Flask app so this
    # doesn't depend on an active app context or the current_app proxy.
    def perform_initial_refresh(app):
        """Perform the initial cache refresh for the given Flask app."""
        global _initial_cache_refresh_done

        # Prevent duplicate initial refresh
        if _initial_cache_refresh_done:
            logger.info("Initial refresh already performed, skipping")
            return True

        try:
            # If Redis is already up (the common case), warm the cache now. Only
            # one worker per pod actually does the work - the pod-local lock
            # inside _warm_cache_once handles that.
            if _redis_is_ready():
                logger.info("Performing initial cache data refresh")
                if _warm_cache_once(app):
                    _initial_cache_refresh_done = True
                    check_redis_memory()
                    return True

            # Redis wasn't reachable during startup (e.g. the sidecar is still
            # coming up after a pod restart). Warm in the background once it's
            # ready, without blocking or failing worker startup.
            logger.warning(
                "Redis not ready during startup; deferring cache warmup "
                "to the background"
            )
            _start_background_cache_warmup(app)
            return False

        except Exception as e:
            logger.error(f"Error during initial cache data refresh: {e}", exc_info=True)
            return False

    return perform_initial_refresh


def check_redis_memory() -> None:
    """Check Redis memory usage and eviction stats."""
    try:
        # Get memory info
        memory_info: dict[str, Any] = redis_client.info(section="memory")  # type: ignore
        used_memory = memory_info.get("used_memory", 0)
        used_memory_peak = memory_info.get("used_memory_peak", 0)
        maxmemory = memory_info.get("maxmemory", 0)
        maxmemory_policy = memory_info.get("maxmemory_policy", "unknown")

        # Get stats for evictions
        stats_info: dict[str, Any] = redis_client.info(section="stats")  # type: ignore
        evicted_keys = stats_info.get("evicted_keys", 0)
        expired_keys = stats_info.get("expired_keys", 0)

        logger.debug(
            f"Redis memory usage: {used_memory/1024/1024:.2f}MB "
            f"(peak: {used_memory_peak/1024/1024:.2f}MB)"
        )

        if maxmemory > 0:
            memory_usage_pct = (used_memory / maxmemory) * 100
            logger.debug(
                f"Redis memory limit: {maxmemory/1024/1024:.2f}MB "
                f"({memory_usage_pct:.1f}% used), policy: {maxmemory_policy}"
            )
        else:
            logger.debug(f"Redis memory limit: unlimited, policy: {maxmemory_policy}")

        if evicted_keys > 0:
            logger.warning(
                f"Redis has evicted {evicted_keys} keys due to memory pressure"
            )

        logger.debug(
            f"Redis expired keys: {expired_keys}, evicted keys: {evicted_keys}"
        )

    except REDIS_UNAVAILABLE_ERRORS as e:
        logger.debug(f"Redis unavailable for memory check: {e}")
    except Exception as e:
        logger.error(f"Failed to get Redis memory info: {e}")
