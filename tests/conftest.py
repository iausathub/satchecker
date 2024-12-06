# import api.core

import os
from datetime import datetime

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from api import create_app
from api.adapters.database_orm import Base
from api.adapters.repositories.satellite_repository import AbstractSatelliteRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.celery_app import make_celery
from api.entrypoints.extensions import db as database

os.environ["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres@localhost:5432/test_satchecker"
)
os.environ["LOCAL_DB"] = "1"


def create_partitions(engine):
    """Create partitions for test data"""
    with engine.connect() as conn:
        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS tle_partitioned_historical
            PARTITION OF tle_partitioned
            FOR VALUES FROM (TIMESTAMP '-infinity') TO ('2020-01-01 00:00:00+00')
        """
            )
        )

        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS tle_partitioned_2020_2023
            PARTITION OF tle_partitioned
            FOR VALUES FROM ('2020-01-01 00:00:00+00') TO ('2024-01-01 00:00:00+00')
        """
            )
        )

        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS tle_partitioned_2024
            PARTITION OF tle_partitioned
            FOR VALUES FROM ('2024-01-01 00:00:00+00') TO ('2025-01-01 00:00:00+00')
        """
            )
        )

        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS tle_partitioned_future
            PARTITION OF tle_partitioned
            FOR VALUES FROM ('2025-01-01 00:00:00+00') TO (TIMESTAMP 'infinity')
        """
            )
        )

        conn.execute(text("commit"))


def create_test_db():
    """Set up the test database with partitions."""
    db_url = os.environ["SQLALCHEMY_DATABASE_URI"]
    db_name = db_url.rsplit("/", 1)[-1]
    default_db_url = db_url.rsplit("/", 1)[0] + "/postgres"

    engine = create_engine(default_db_url)

    with engine.connect() as conn:
        conn.execute(text("commit"))
        try:
            conn.execute(text(f"CREATE DATABASE {db_name}"))
        except ProgrammingError:
            conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
            conn.execute(text(f"CREATE DATABASE {db_name}"))
        finally:
            conn.execute(text("commit"))

    # Initialize the database and partitions
    test_engine = create_engine(db_url)
    with test_engine.connect() as conn:
        conn.execute(text("commit"))
        create_partitions(test_engine)


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": os.environ["SQLALCHEMY_DATABASE_URI"],
        }
    )

    celery = make_celery(app.name)
    celery.conf.update(app.config)
    app.celery = celery

    with app.app_context():
        database.init_app(app)

        Base.metadata.create_all(bind=database.engine)

        create_partitions(database.engine)
        yield app
        database.session.remove()
        Base.metadata.drop_all(bind=database.engine)


@pytest.fixture
def pg_session_factory(app):
    """Create a new session factory for each test"""
    Session = sessionmaker(bind=database.engine)  # noqa: N806
    return Session


@pytest.fixture
def session(pg_session_factory):
    """Provide a transactional scope around a series of operations."""
    session = pg_session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def cleanup_database(session):
    """Cleanup database after each test."""
    yield
    try:
        # Delete from tle_partitioned first since it references satellites
        session.execute(text("DELETE FROM tle_partitioned"))
        session.execute(text("DELETE FROM satellites"))
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


class FakeSatelliteRepository(AbstractSatelliteRepository):
    def __init__(self, satellites):
        self._satellites = satellites

    def _add(self, satellite):
        self._satellites.add(satellite)

    def _get_norad_ids_from_satellite_name(self, name):
        return [
            [
                satellite.sat_number,
                datetime(2024, 1, 1),
                satellite.has_current_sat_number,
            ]
            for satellite in self._satellites
            if satellite.sat_name == name
        ]

    def _get_satellite_names_from_norad_id(self, id):
        return [
            [satellite.sat_name, datetime(2024, 1, 1), satellite.has_current_sat_number]
            for satellite in self._satellites
            if satellite.sat_number == id
        ]

    def _get_satellite_data_by_id(self, id):
        return [
            [satellite.sat_name, datetime(2024, 1, 1), satellite.has_current_sat_number]
            for satellite in self._satellites
            if satellite.sat_number == id
        ]

    def _get_satellite_data_by_name(self, name):
        return [
            [
                satellite.sat_number,
                datetime(2024, 1, 1),
                satellite.has_current_sat_number,
            ]
            for satellite in self._satellites
            if satellite.sat_name == name
        ]

    def _get(self, satellite_id):
        return next(
            (
                satellite
                for satellite in self._satellites
                if satellite.sat_number == satellite_id
            ),  # noqa: E501
            None,
        )


class FakeTLERepository(AbstractTLERepository):
    def __init__(self, tles):
        self._tles = set(tles)

    def _add(self, tle):
        self._tles.add(tle)

    def _get_all_for_date_range_by_satellite_name(
        self, satellite_name, start_date, end_date
    ):
        return [
            tle
            for tle in self._tles
            if (
                tle.satellite.sat_name == satellite_name
                and (
                    (start_date is None or start_date <= tle.epoch)
                    and (end_date is None or tle.epoch <= end_date)
                )
            )
        ]

    def _get_all_for_date_range_by_satellite_number(
        self, satellite_number, start_date, end_date
    ):
        return [
            tle
            for tle in self._tles
            if (
                tle.satellite.sat_number == satellite_number
                and (
                    (start_date is None or start_date <= tle.epoch)
                    and (end_date is None or tle.epoch <= end_date)
                )
            )
        ]

    def _get_closest_by_satellite_name(self, satellite_name, epoch):
        return min(
            (tle for tle in self._tles if tle.satellite.sat_name == satellite_name),
            key=lambda tle: abs(tle.epoch - epoch),
            default=None,
        )

    def _get_closest_by_satellite_number(self, satellite_number, epoch):
        return min(
            (tle for tle in self._tles if tle.satellite.sat_number == satellite_number),
            key=lambda tle: abs(tle.epoch - epoch),
            default=None,
        )

    def _get_all_tles_at_epoch(self, epoch_date, page, per_page, format):
        return list(self._tles), len(self._tles)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True
