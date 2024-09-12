# import api.core

import os
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import create_app
from api.adapters.database_orm import Base
from api.adapters.repositories.satellite_repository import AbstractSatelliteRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.celery_app import make_celery
from api.entrypoints.extensions import db as database

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

    celery = make_celery(app.name)
    celery.conf.update(app.config)
    app.celery = celery

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

    def _get_most_recent_full_tle_set(self):
        return self._tles


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True
