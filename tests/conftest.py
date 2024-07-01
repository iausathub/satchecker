# import api.core
import os

import pytest

from api import satchecker

os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"


@pytest.fixture()
def app():
    app = satchecker.app
    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.app_context():
        yield app
    # yield app


@pytest.fixture()
def client(app):
    with app.app_context():
        return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
