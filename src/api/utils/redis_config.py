import logging
import os
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def get_redis_config():
    """
    Get Redis host and port from environment variables.
    Returns tuple of (host, port, source_description).
    """
    # Check REDIS_URL first
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        parsed = urlparse(redis_url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 6379
        return host, port, f"REDIS_URL={redis_url}"

    # Otherwise use REDIS_HOST and REDIS_PORT separately
    host = os.getenv("REDIS_HOST", "localhost")
    port_str = os.getenv("REDIS_PORT", "6379")
    port = int(port_str)
    return host, port, f"REDIS_HOST={host}, REDIS_PORT={port_str}"


def get_redis_url() -> str:
    """Get Redis URL string from environment variables."""
    host, port, _ = get_redis_config()
    return f"redis://{host}:{port}"
