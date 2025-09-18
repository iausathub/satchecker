import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional

from astropy.coordinates import EarthLocation
from astropy.time import Time

from api.domain.models.tle import TLE
from api.entrypoints.extensions import db, redis_client, scheduler

# Use the application's centralized logging configuration
logger = logging.getLogger(__name__)

DEFAULT_CACHE_TTL = 3600  # 1 hour in seconds
RECENT_TLES_CACHE_KEY = "recent_tles"


def create_fov_cache_key(
    location: EarthLocation,
    mid_obs_time_jd: Time,
    start_time_jd: Time,
    duration: float,
    ra: float,
    dec: float,
    fov_radius: float,
    include_tles: bool = False,
    constellation: Optional[str] = None,
    data_source: Optional[str] = None,
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
        f"include_tles_{include_tles}",
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
                logger.info(
                    f"Caching {results_count} results in data structure "
                    f"for key {key}"
                )
            if "tles" in data:
                tles_count = len(data["tles"]) if data["tles"] else 0
                logger.info(
                    f"Caching {tles_count} TLEs in data structure for key {key}"
                )

        if serialized_size > 500 * 1024 * 1024:
            logger.warning(
                f"Data for key {key} is too large to cache "
                f"({serialized_size} bytes), skipping"
            )
            return False

        logger.info(f"Attempting to cache data for key {key}: {serialized_size} bytes")
        redis_client.setex(key, ttl, serialized)

        check_redis_memory()

        # Immediately verify the data was cached successfully
        verification_data = redis_client.get(key)
        if verification_data:
            verified_data = json.loads(str(verification_data))
            if isinstance(verified_data, dict):
                if "results" in verified_data:
                    verified_count = (
                        len(verified_data["results"]) if verified_data["results"] else 0
                    )
                    logger.info(
                        f"Verification: Retrieved {verified_count} results "
                        f"from cache for key {key}"
                    )
                if "tles" in verified_data:
                    verified_tles = (
                        len(verified_data["tles"]) if verified_data["tles"] else 0
                    )
                    logger.info(
                        f"Verification: Retrieved {verified_tles} TLEs "
                        f"from cache for key {key}"
                    )
            logger.info(f"Successfully cached and verified data for key {key}")
        else:
            logger.warning(
                "Cache verification failed - data not found immediately "
                f"after setex for key {key}"
            )
            return False

        return True
    except Exception as e:
        logger.warning(f"Cache set error for key {key}: {e}", exc_info=True)
        return False


def batch_serialize_tles(tles: list[TLE]) -> list[dict[str, Any]]:
    """
    Efficiently serialize a batch of TLEs for caching.
    Much faster than serializing one by one, especially for large datasets.

    Args:
        tles: List of TLE objects to serialize

    Returns:
        List of serialized TLE dictionaries
    """
    result: list[dict[str, Any]] = []
    result_append = result.append

    for tle in tles:
        # Get satellite information once to avoid repeated attribute access
        satellite = tle.satellite
        decay_date = satellite.decay_date

        # Get the designation that was valid at the TLE's epoch time
        epoch_designation = satellite.get_designation_at_date(tle.epoch)
        if epoch_designation is None:
            logger.warning(
                f"No satellite designation found for {satellite.object_id} "
                f"at {tle.epoch}"
            )
            continue
        # Create efficient TLE dictionary with direct attribute access
        tle_dict = {
            "tle_line1": tle.tle_line1,
            "tle_line2": tle.tle_line2,
            "epoch": tle.epoch.isoformat(),
            "date_collected": tle.date_collected.isoformat(),
            "is_supplemental": tle.is_supplemental,
            "data_source": tle.data_source,
            "satellite": {
                "sat_name": epoch_designation.sat_name,
                "sat_number": epoch_designation.sat_number,
                "decay_date": decay_date.isoformat() if decay_date else None,
                "constellation": satellite.constellation,
            },
        }
        result_append(tle_dict)

    return result


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
            serialized_tles = batch_serialize_tles(tles)
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

        return True

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
        # Access the Flask app directly through the scheduler

        app = scheduler.app

        logger.info(
            f"Scheduled TLE cache refresh triggered at {datetime.now(timezone.utc)}"
        )

        # Execute refresh_tle_cache within the app context
        with app.app_context():
            logger.info("Running scheduled refresh with app context")
            refresh_tle_cache()
    except Exception as e:
        logger.error(f"Error in scheduled TLE refresh: {e}", exc_info=True)


# Global flag to track if the initial refresh has been done
_initial_cache_refresh_done = False


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

    # Don't perform immediate refresh here, as it might not have app context
    def perform_initial_refresh():
        """Performs the initial cache refresh with proper app context"""
        global _initial_cache_refresh_done

        # Prevent duplicate initial refresh
        if _initial_cache_refresh_done:
            logger.info("Initial refresh already performed, skipping")
            return True

        try:
            from flask import current_app

            # Check if we're in an application context
            if not current_app:
                logger.warning(
                    "No Flask app context available for initial cache refresh"
                )
                return False

            # Since we're already in an app context, we can use it directly
            logger.info("Performing initial TLE cache refresh")
            session = db.session
            result = refresh_tle_cache(session=session)
            _initial_cache_refresh_done = True

            check_redis_memory()

            return result

        except Exception as e:
            logger.error(f"Error during initial TLE cache refresh: {e}", exc_info=True)
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

        logger.info(
            f"Redis memory usage: {used_memory/1024/1024:.2f}MB "
            f"(peak: {used_memory_peak/1024/1024:.2f}MB)"
        )

        if maxmemory > 0:
            memory_usage_pct = (used_memory / maxmemory) * 100
            logger.info(
                f"Redis memory limit: {maxmemory/1024/1024:.2f}MB "
                f"({memory_usage_pct:.1f}% used), policy: {maxmemory_policy}"
            )
        else:
            logger.info(f"Redis memory limit: unlimited, policy: {maxmemory_policy}")

        if evicted_keys > 0:
            logger.warning(
                f"Redis has evicted {evicted_keys} keys due to memory pressure"
            )

        logger.info(f"Redis expired keys: {expired_keys}, evicted keys: {evicted_keys}")

    except Exception as e:
        logger.error(f"Failed to get Redis memory info: {e}")
