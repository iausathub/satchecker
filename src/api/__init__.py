"""API package initialization."""

import logging
import os
import sys

from flask import Flask

from api.celery_app import celery


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
            broker_url="redis://localhost:6379/0",
            result_backend="redis://localhost:6379/0",
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
    # First, clear any existing handlers to avoid duplicates
    if app.logger.handlers:
        app.logger.handlers = []

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    is_gunicorn = "gunicorn" in sys.modules

    if is_gunicorn:
        # Use Gunicorn's logger for production
        gunicorn_logger = logging.getLogger("gunicorn.error")
        for handler in gunicorn_logger.handlers:
            handler.setFormatter(formatter)
            app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Production logging configured (using Gunicorn logger)")
    else:
        # Create a handler that writes to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
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
