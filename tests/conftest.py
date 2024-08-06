# import api.core

import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api import create_app
from src.api.adapters.database_orm import Base

os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
os.environ["LOCAL_DB"] = "1"


""" @pytest.fixture()
def app():

    from api import satchecker
    app = (
        satchecker.app
    )  # ({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        from core.extensions import db as database
        database.create_all()
        yield app
        database.session.remove()
        database.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
 """


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    session = sessionmaker(bind=in_memory_sqlite_db)
    yield session
    Base.metadata.drop_all(in_memory_sqlite_db)


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
