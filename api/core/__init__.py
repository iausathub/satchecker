import logging

from celery import Celery, Task
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from core import utils
from core.extensions import db


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app():
    app = Flask(__name__)

    db_login = utils.get_db_login()

    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost:6379/0",
            result_backend="redis://localhost:6379/0",
            task_ignore_result=False,
            task_track_started=True,
        ),
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{db_login[0]}:{db_login[1]}@"
        f"{db_login[2]}:{db_login[3]}/{db_login[4]}?options=-c%20timezone=utc"
    )
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"echo": True, "use_native_hstore": False}
    return app


app = create_app()
celery = celery_init_app(app)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.INFO)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per second", "2000 per minute"],
)

db.init_app(app)

from core import routes  # noqa: E402, F401, I001
