# import api.core

import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api import create_app
from src.api.adapters.database_orm import Base
from src.api.entrypoints.extensions import db as database

os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
os.environ["LOCAL_DB"] = "1"


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
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        database.init_app(app)
        Base.metadata.create_all(bind=database.engine)
        yield app
        database.session.remove()
        Base.metadata.drop_all(bind=database.engine)


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
