import logging
import os

from api.celery_app import celery
from api.config import get_db_login
from api.entrypoints.extensions import db, limiter
from api.entrypoints.v1.routes import api_main, api_v1
from api.entrypoints.v1.routes import ephemeris_routes as ephem_routes  # noqa: F401
from api.entrypoints.v1.routes import routes as v1_routes  # noqa: F401, I001
from api.entrypoints.v1.routes import tools_routes as tool_routes  # noqa: F401, I001
from flask import Flask
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_main, url_prefix="/")
    app.register_blueprint(api_v1, url_prefix="/v1")
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

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)  # noqa: F841
    with app.app_context():
        return app


app = create_app()
celery.conf.update(app.config)
app.extensions["celery"] = celery

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.INFO)

limiter.init_app(app)

db.init_app(app)
