"""API package initialization."""

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone

from flask import Flask

from api.celery_app import celery


class JSONFormatter(logging.Formatter):
    # Regex to strip ANSI color codes
    ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")

    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc)

        # Strip ANSI color codes from message
        message = self.ANSI_ESCAPE.sub("", record.getMessage())

        log_data = {
            "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": message,
        }
        # Add extra fields if present (from our request logging)
        for key in [
            "endpoint",
            "method",
            "path",
            "status",
            "duration_ms",
            "ip",
            "query",
            "user_agent",
        ]:
            if hasattr(record, key):
                log_data[key] = getattr(record, key)

        # Include exception traceback if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, static_url_path="/static")

    # Import and register blueprints
    from api.entrypoints.v1.routes import api_main, api_v1

    app.register_blueprint(api_main, url_prefix="/")
    app.register_blueprint(api_v1, url_prefix="/v1")

    # Initialize error handler
    from api.middleware.error_handler import init_error_handler

    init_error_handler(app)

    # Initialize request logger
    from api.middleware.request_logger import init_request_logging

    init_request_logging(app)

    # Configure database
    from api.config import get_db_login

    db_login = get_db_login()

    if os.environ.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI"
        )
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql://{db_login[0]}:{db_login[1]}@"
            f"{db_login[2]}:{db_login[3]}/{db_login[4]}"
            "?options=-c%20timezone=utc"
        )
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "echo": True,
            "use_native_hstore": False,
        }

    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=False,
            task_track_started=True,
        ),
    )

    # Swagger configuration
    app.config["SWAGGER"] = {
        "title": "SatChecker API",
        "uiversion": 3,
        "openapi": "3.0.2",
        "specs_route": "/api/docs/",
        "static_url_path": "/static",
        "template_file": "flasgger/index.html",  # Use the custom template
    }

    # Initialize extensions
    from api.entrypoints.extensions import db, limiter, swagger

    db.init_app(app)
    limiter.init_app(app)
    swagger.init_app(app)

    # Initialize migrations
    from flask_migrate import Migrate

    migrate = Migrate(app, db)  # noqa: F841

    # Initialize celery

    celery.conf.update(app.config)
    app.extensions["celery"] = celery

    setup_logging(app)

    return app


def setup_logging(app):
    """Set up logging based on the running environment."""
    is_gunicorn = "gunicorn" in sys.modules

    # Configure root logger - all other loggers inherit from this
    root_logger = logging.getLogger()

    # Clear existing handlers to avoid duplicates
    root_logger.handlers = []
    app.logger.handlers = []

    # Prevent app.logger from propagating to root (avoid duplicates)
    app.logger.propagate = False

    if is_gunicorn:  # pragma: no cover
        # JSON log format for better use in Grafana
        formatter: logging.Formatter = JSONFormatter()

        gunicorn_logger = logging.getLogger("gunicorn.error")
        for handler in gunicorn_logger.handlers:
            handler.setFormatter(formatter)
            root_logger.addHandler(handler)
            app.logger.addHandler(handler)

        root_logger.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Production logging configured (JSON)")
    else:
        # Text format for local development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)
        app.logger.addHandler(console_handler)

        log_level = logging.DEBUG if app.debug else logging.INFO
        root_logger.setLevel(log_level)
        app.logger.setLevel(log_level)
        app.logger.info("Development logging configured")


app = create_app()

# Initialize cache
with app.app_context():
    from api.services.cache_service import initialize_cache_refresh_scheduler

    try:
        app.logger.info("Setting up cache refresh scheduler")
        initial_refresh_func = initialize_cache_refresh_scheduler(hours=3)
        refresh_success = initial_refresh_func()
        if not refresh_success:
            app.logger.warning("Initial TLE cache refresh was not successful")
    except Exception as e:
        app.logger.error(f"Error during cache initialization: {e}", exc_info=True)
