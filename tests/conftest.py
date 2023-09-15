import pytest
from api import satchecker
from api.core.extensions import db
#import api.core 

@pytest.fixture()
def app():
    app = satchecker.app
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()