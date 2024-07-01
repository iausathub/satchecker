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
    ctx = app.app_context()
    ctx.push()
    yield app

    ctx.pop()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
