import os
from urllib.parse import urlparse

from flask import request
from flask_apscheduler import APScheduler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from redis import Redis


def get_forwarded_address():
    """
    Retrieves the original IP address from the 'X-Forwarded-For' header of a
    HTTP request.

    This is needed due to the way the app is deployed with Docker. If the
    'X-Forwarded-For' header is not present, it falls back to the remote
    address of the request.

    Args:
        request (werkzeug.local.LocalProxy): The HTTP request object.

    Returns:
        str: The original client IP address, or the remote address of the request if the
             'X-Forwarded-For' header is not present.
    """
    forwarded_header = request.headers.get("X-Forwarded-For")
    if forwarded_header:
        return request.headers.getlist("X-Forwarded-For")[0]
    return get_remote_address


db = SQLAlchemy()

limiter = Limiter(
    key_func=get_forwarded_address,
    default_limits=["100 per second", "2000 per minute"],
    storage_uri=(
        f"redis://{os.getenv('REDIS_HOST', 'localhost')}:"
        f"{os.getenv('REDIS_PORT', 6379)}/0"
    ),
    headers_enabled=True,
    strategy="fixed-window",
)
scheduler = APScheduler()

# Parse Redis URL if provided, otherwise use host/port
redis_url = os.getenv("REDIS_PORT")
if redis_url and "://" in redis_url:
    # Parse URL like 'tcp://172.17.0.3:6379'
    parsed = urlparse(redis_url)
    redis_host = parsed.hostname
    redis_port = parsed.port
else:
    # Use separate host/port env vars
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))

# Use parsed values
redis_client = Redis(
    host=redis_host,
    port=redis_port,
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True,
)
