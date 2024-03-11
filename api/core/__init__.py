import logging

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from core import utils
from core.extensions import db


def create_app():
    app = Flask(__name__)

    db_login = utils.get_db_login()

    # fmt: off
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@{}:{}/{}".format(
        db_login[0], db_login[1], db_login[2], db_login[3], db_login[4]
    )
    # fmt: on

    return app


app = create_app()

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
