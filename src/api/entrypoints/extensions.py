import os

from flasgger import Swagger
from flask import request
from flask_apscheduler import APScheduler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from redis import ConnectionPool, Redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry

from api.utils.redis_config import get_redis_config


def get_forwarded_address() -> str:
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
    return get_remote_address()


db = SQLAlchemy()

scheduler = APScheduler()

# Get Redis configuration
redis_host, redis_port, _ = get_redis_config()

# Configure retry logic with exponential backoff for better resilience
retry = Retry(ExponentialBackoff(cap=10, base=1.5), 3)  # Maximum number of retries

# Connection pool for better performance
redis_pool = ConnectionPool(
    host=redis_host,
    port=redis_port,
    db=int(os.getenv("REDIS_DB", 0)),
    max_connections=20,
    decode_responses=True,
    retry_on_timeout=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)

redis_client = Redis(
    connection_pool=redis_pool,
    retry=retry,
    retry_on_timeout=True,
    socket_timeout=5,
    health_check_interval=30,  # Check connection health every 30 seconds
)

limiter = Limiter(
    key_func=get_forwarded_address,
    default_limits=["100 per second", "2000 per minute"],
    storage_uri=(f"redis://{redis_host}:{redis_port}/0"),
    headers_enabled=True,
    strategy="moving-window",
    swallow_errors=True,
)

# Initialize Swagger for documentation
swagger = Swagger(
    template={
        "openapi": "3.0.2",
        "info": {
            "title": "SatChecker API",
            "description": "API for satellite information and tracking",
            "version": "1.3",
            "contact": {
                "name": "IAU CPS",
                "url": "https://satchecker.cps.iau.org/",
            },
        },
        "components": {
            "securitySchemes": {
                "APIKeyHeader": {"type": "apiKey", "name": "X-API-Key", "in": "header"}
            },
        },
        "security": [{"APIKeyHeader": []}],
    },
    parse=True,  # Parse docstrings
    config={
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: not rule.rule.startswith("/v1"),
                "model_filter": lambda tag: True,  # Include all models
            }
        ],
        "swagger_ui": True,
        "specs_route": "/api/docs/",
        "template_file": "flasgger/index.html",  # Use our custom template
    },
)
