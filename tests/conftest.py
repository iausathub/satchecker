# noqa: I001
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
import psycopg2
import pytest
import redis
from astropy.coordinates import EarthLocation
from astropy.time import Time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from api import create_app
from api.adapters.database_orm import Base
from api.adapters.repositories.ephemeris_repository import AbstractEphemerisRepository
from api.adapters.repositories.satellite_repository import (
    AbstractSatelliteRepository,
)
from api.adapters.repositories.tdm_repository import AbstractTdmPredictionRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.celery_app import make_celery
from api.domain.models.interpolable_ephemeris import (
    EphemerisPoint,
    InterpolableEphemeris,
)
from api.domain.models.interpolator_splines import InterpolatorSplines
from api.domain.models.satellite import Satellite
from api.entrypoints.extensions import db as database

FIXTURES_DIR = Path(__file__).parent / "fixtures"

if "SQLALCHEMY_DATABASE_URI" not in os.environ:
    os.environ["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:postgres@localhost:5432/test_satchecker"
    )
os.environ["LOCAL_DB"] = "1"


def create_partitions(engine):
    """Create partitions for test data"""
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tle_partitioned_historical
            PARTITION OF tle_partitioned
            FOR VALUES FROM (TIMESTAMP '-infinity') TO ('2020-01-01 00:00:00+00')
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tle_partitioned_2020_2023
            PARTITION OF tle_partitioned
            FOR VALUES FROM ('2020-01-01 00:00:00+00') TO ('2024-01-01 00:00:00+00')
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tle_partitioned_2024
            PARTITION OF tle_partitioned
            FOR VALUES FROM ('2024-01-01 00:00:00+00') TO ('2025-01-01 00:00:00+00')
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tle_partitioned_future
            PARTITION OF tle_partitioned
            FOR VALUES FROM ('2025-01-01 00:00:00+00') TO (TIMESTAMP 'infinity')
        """))

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
        # create_partitions(test_engine)


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
        if "sqlalchemy" not in app.extensions:
            database.init_app(app)

        Base.metadata.create_all(bind=database.engine)

        # create_partitions(database.engine)
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
    if cannot_connect_to_services():
        pytest.skip("PostgreSQL not available - skipping database cleanup")

    yield
    try:
        # Delete from tables in order of dependencies
        session.execute(text("DELETE FROM ephemeris_points"))
        session.execute(text("DELETE FROM interpolable_ephemeris"))
        session.execute(text("DELETE FROM tle"))
        session.execute(text("DELETE FROM tdm_prediction_points"))
        session.execute(text("DELETE FROM tdm_predictions"))
        session.execute(text("DELETE FROM satellites"))
        session.execute(text("DELETE FROM tdm_predictions"))
        session.execute(text("DELETE FROM tdm_prediction_points"))
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@pytest.fixture(autouse=True)
def cleanup_cache(app):
    """Clean up Redis cache after each test"""
    if cannot_connect_to_services():
        pytest.skip("Redis not available - skipping cache cleanup")

    yield
    try:
        redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=0,
        )
        redis_client.flushdb()
    except Exception as e:
        print(f"Error flushing Redis cache: {e}")


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def services_available():
    """Check if external services are available."""
    available = not cannot_connect_to_services()
    if not available:
        pytest.skip("External services not available")
    return available


def cannot_connect_to_services():
    """Check if required services (Redis and Postgres) are available."""
    # Check Redis
    try:
        # Use localhost for local development
        redis_host = os.getenv("REDIS_HOST", "localhost")
        # Handle GitLab CI's TCP URL format
        redis_port_str = os.getenv("REDIS_PORT", "6379")
        if "tcp://" in redis_port_str:
            redis_port = int(redis_port_str.split(":")[-1])
        else:
            redis_port = int(redis_port_str)

        r = redis.Redis(host=redis_host, port=redis_port, db=0)
        r.ping()
    except redis.ConnectionError:
        return True

    # Check Postgres using the environment variable
    try:
        # Use environment variable if set, otherwise use default local connection
        db_url = os.environ.get(
            "SQLALCHEMY_DATABASE_URI",
            "postgresql://postgres:postgres@localhost:5432/test_satchecker",
        )
        parsed = urlparse(db_url)
        conn = psycopg2.connect(
            dbname=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port,
        )
        conn.close()
    except (psycopg2.OperationalError, KeyError):
        return True

    return False


class FakeSatelliteRepository(AbstractSatelliteRepository):
    def __init__(self, satellites, exception_to_raise=None):
        super().__init__()
        self._satellites = satellites
        self.exception_to_raise = exception_to_raise

    def _add(self, satellite):
        self._satellites.add(satellite)

    def _get_norad_ids_from_satellite_name(self, name):
        if self.exception_to_raise:
            raise self.exception_to_raise
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
        if self.exception_to_raise:
            raise self.exception_to_raise
        return [
            [satellite.sat_name, datetime(2024, 1, 1), satellite.has_current_sat_number]
            for satellite in self._satellites
            if satellite.sat_number == id
        ]

    def _get_satellite_data_by_id(self, id):
        if self.exception_to_raise:
            raise self.exception_to_raise
        try:
            id_int = int(id) if isinstance(id, str) and id.isdigit() else id
            matching_satellites = [
                satellite
                for satellite in self._satellites
                if satellite.sat_number == id_int
            ]
            return matching_satellites[0] if matching_satellites else None
        except (ValueError, TypeError):
            return None

    def _get_satellite_data_by_name(self, name):
        if self.exception_to_raise:
            raise self.exception_to_raise
        matching_satellites = [
            satellite for satellite in self._satellites if satellite.sat_name == name
        ]
        return matching_satellites[0] if matching_satellites else None

    def _get_starlink_generations(self):
        if self.exception_to_raise:
            raise self.exception_to_raise
        # Group satellites by generation
        generations = {}
        for satellite in self._satellites:
            if satellite.generation and "starlink" in satellite.sat_name.lower():
                if not isinstance(satellite.launch_date, (datetime, type(None))):
                    raise TypeError("Launch date must be a datetime object or None")
                if satellite.generation not in generations:
                    generations[satellite.generation] = {
                        "earliest": satellite.launch_date,
                        "latest": satellite.launch_date,
                    }
                else:
                    if (
                        satellite.launch_date
                        < generations[satellite.generation]["earliest"]
                    ):
                        generations[satellite.generation][
                            "earliest"
                        ] = satellite.launch_date
                    if (
                        satellite.launch_date
                        > generations[satellite.generation]["latest"]
                    ):
                        generations[satellite.generation][
                            "latest"
                        ] = satellite.launch_date

        # Convert to list of tuples matching the real repository's format
        return [
            (gen, data["earliest"], data["latest"])
            for gen, data in sorted(generations.items())
        ]

    def _get_active_satellites(self, object_type=None):
        if self.exception_to_raise:
            raise self.exception_to_raise
        return [
            satellite
            for satellite in self._satellites
            if satellite.decay_date is None
            and satellite.has_current_sat_number
            and (
                object_type is None
                or satellite.object_type.lower() == object_type.lower()
            )
        ]

    def _search_all_satellites(self, parameters):
        return self._satellites

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
    def __init__(self, tles, exception_to_raise=None):
        self._tles = set(tles)
        self.exception_to_raise = exception_to_raise

    def _add(self, tle):
        self._tles.add(tle)

    def _get_all_for_date_range_by_satellite_name(
        self, satellite_name, start_date, end_date
    ):
        if self.exception_to_raise:
            raise self.exception_to_raise
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
        if self.exception_to_raise:
            raise self.exception_to_raise
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
        if self.exception_to_raise:
            raise self.exception_to_raise
        return min(
            (tle for tle in self._tles if tle.satellite.sat_name == satellite_name),
            key=lambda tle: abs(tle.epoch - epoch),
            default=None,
        )

    def _get_closest_by_satellite_number(self, satellite_number, epoch):
        if self.exception_to_raise:
            raise self.exception_to_raise
        return min(
            (tle for tle in self._tles if tle.satellite.sat_number == satellite_number),
            key=lambda tle: abs(tle.epoch - epoch),
            default=None,
        )

    def _get_all_tles_at_epoch(
        self,
        epoch_date,
        page,
        per_page,
        format,
        constellation=None,
        data_source=None,
        use_generated_tles=False,
    ):
        if self.exception_to_raise:
            raise self.exception_to_raise
        filtered_tles = [
            tle
            for tle in self._tles
            if (constellation is None or tle.satellite.constellation == constellation)
            and (epoch_date is None or tle.epoch <= epoch_date)
            and (
                data_source is None
                or tle.data_source == data_source
                or data_source == "any"
            )
        ]
        return filtered_tles, len(filtered_tles), "database"

    def _get_adjacent_tles(self, id, id_type, epoch):
        if self.exception_to_raise:
            raise self.exception_to_raise
        # limit to one before and one after for the given id (satellite number)
        tles = [tle for tle in self._tles if tle.satellite.sat_number == id]
        return tles[:1] + tles[1:]

    def _get_tles_around_epoch(self, id, id_type, epoch, count_before, count_after):
        if self.exception_to_raise:
            raise self.exception_to_raise
        # limit to count_before + count_after
        tles = [tle for tle in self._tles if tle.satellite.sat_number == id]
        return tles[: count_before + count_after]

    def _get_nearest_tle(self, id, id_type, epoch):
        if self.exception_to_raise:
            raise self.exception_to_raise
        return min(
            (tle for tle in self._tles if tle.satellite.sat_number == id),
            key=lambda tle: abs(tle.epoch - epoch),
            default=None,
        )


class FakeEphemerisRepository(AbstractEphemerisRepository):
    def __init__(self, ephemeris):
        self._ephemeris = ephemeris

    def _add(self, ephemeris):
        self._ephemeris.add(ephemeris)

    def _get_closest_by_satellite_number(self, satellite_number, epoch):
        satellite_number_int = int(satellite_number)
        return min(
            (
                ephemeris
                for ephemeris in self._ephemeris
                if ephemeris.satellite.sat_number == satellite_number_int
            ),
            key=lambda ephemeris: abs(ephemeris.generated_at - epoch),
            default=None,
        )

    def _get_closest_by_satellite_name(self, satellite_name, epoch):
        return min(
            (
                ephemeris
                for ephemeris in self._ephemeris
                if ephemeris.satellite.sat_name == satellite_name
            ),
            key=lambda ephemeris: abs(ephemeris.generated_at - epoch),
            default=None,
        )

    def _get_latest_by_satellite_number(self, satellite_number):
        return max(
            (
                ephemeris
                for ephemeris in self._ephemeris
                if ephemeris.satellite.sat_number == satellite_number
            ),
            key=lambda ephemeris: ephemeris.generated_at,
            default=None,
        )

    def _get_latest_by_satellite_name(self, satellite_name):
        return max(
            (
                ephemeris
                for ephemeris in self._ephemeris
                if ephemeris.satellite.sat_name == satellite_name
            ),
            key=lambda ephemeris: ephemeris.generated_at,
            default=None,
        )

    def _get_satellites_with_ephemeris(
        self, start_time: datetime, end_time: datetime
    ) -> list[Satellite]:
        return [ephemeris.satellite for ephemeris in self._ephemeris]

    def _add_interpolator_splines(self, interpolator_splines: InterpolatorSplines):

        if not hasattr(self, "_interpolator_splines"):
            self._interpolator_splines = []
        self._interpolator_splines.append(interpolator_splines)

    def _get_interpolator_splines(
        self, ephemeris_id: int
    ) -> InterpolatorSplines | None:
        if not hasattr(self, "_interpolator_splines"):
            return None
        for splines in self._interpolator_splines:
            if splines.ephemeris_id == ephemeris_id:
                return splines
        return None

    def _get_all_interpolator_splines_at_epoch(
        self, epoch_date: datetime
    ) -> list[InterpolatorSplines]:
        if not hasattr(self, "_interpolator_splines"):
            return []
        return [
            splines
            for splines in self._interpolator_splines
            if splines.time_range_start <= epoch_date <= splines.time_range_end
        ]

    def _get_closest_by_satellite_numbers(
        self,
        satellite_numbers: list[str],
        epoch: datetime,
        data_source: str | None = None,
    ) -> dict[int, InterpolableEphemeris]:
        results = {}
        for satellite_number in satellite_numbers:
            closest_ephemeris = self._get_closest_by_satellite_number(
                satellite_number, epoch
            )
            if closest_ephemeris:
                if data_source is None or closest_ephemeris.data_source == data_source:
                    results[int(satellite_number)] = closest_ephemeris
        return results


class FakeTdmPredictionRepository(AbstractTdmPredictionRepository):
    def __init__(self, tdm_predictions, tdm_prediction_points, exception_to_raise=None):
        self._tdm_predictions = set(tdm_predictions)
        self._tdm_prediction_points = set(tdm_prediction_points)
        self.exception_to_raise = exception_to_raise

    def _add(self, tdm_prediction):
        self._tdm_predictions.add(tdm_prediction)

    def _get_all_tdm_predictions_at_epoch(
        self, epoch_date, duration, site_name, constellation
    ):
        if self.exception_to_raise:
            raise self.exception_to_raise
        range_end = epoch_date + timedelta(seconds=duration)
        results = [
            p
            for p in self._tdm_predictions
            if p.time_range_start <= epoch_date
            and p.time_range_end >= range_end
            and (constellation is None or p.satellite.constellation == constellation)
            and (site_name is None or p.site_name == site_name)
        ]
        return results, len(results), "fake"

    def _get_tdm_prediction_points(self, tdm_prediction_ids):
        if self.exception_to_raise:
            raise self.exception_to_raise
        return [
            pt
            for pt in self._tdm_prediction_points
            if pt.tdm_prediction_id in tdm_prediction_ids
        ]


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


@pytest.fixture
def test_location():
    return EarthLocation(lat=43.1929, lon=-81.3256, height=300)


@pytest.fixture
def test_time():
    return Time("2024-10-01T18:19:13", format="isot", scale="utc")


# Starlink-31570 ephemeris fixture built from a trimmed MEME operator file.
# The sample covers 2025-10-10 19:07:42–19:57:42 UTC (50 one-minute points).
@pytest.fixture(scope="module")
def starlink_ephemeris():
    """
    InterpolableEphemeris for STARLINK-31570 (NORAD 59324) built from a
    50-point slice of a real operator MEME file stored in tests/fixtures/.

    Ephemeris span: 2025-10-10 19:07:42 – 19:57:42 UTC (1-minute cadence).
    The sub-satellite point at index 30 (19:37:42 UTC, JD 2460959.317847) is
    near (Lat -0.808°, Lon -1.084°) — useful as a test observer location.
    """
    lines = (FIXTURES_DIR / "sample_starlink_ephemeris.txt").read_text().splitlines()

    def _date_time(s):
        return datetime.strptime(s.replace(" UTC", ""), "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        )

    generated_at = _date_time(lines[0].split(":", 1)[1].strip())
    ephemeris_start = _date_time(
        re.search(r"ephemeris_start:(.+?) ephemeris_stop:", lines[1]).group(1)
    )
    ephemeris_stop = _date_time(
        re.search(r"ephemeris_stop:(.+?) step_size:", lines[1]).group(1)
    )

    row_idx, col_idx = np.tril_indices(6)
    points = []
    for i in range(4, len(lines), 4):  # skip 3 header lines + "UVW" frame line
        parts = lines[i].split()
        ts = datetime.strptime(parts[0][:13], "%Y%j%H%M%S").replace(tzinfo=timezone.utc)
        pos = np.array(parts[1:4], dtype=float)
        vel = np.array(parts[4:7], dtype=float)
        cov_vals = np.array(
            [x for row in lines[i + 1 : i + 4] for x in row.split()], dtype=float
        )
        cov = np.zeros((6, 6))
        cov[row_idx, col_idx] = cov_vals
        cov[col_idx, row_idx] = cov_vals
        points.append(EphemerisPoint(ts, pos, vel, cov))

    return InterpolableEphemeris(
        id=1,
        satellite=Satellite(sat_number=59324, sat_name="STARLINK-31570"),
        generated_at=generated_at,
        data_source="spacetrack",
        frame="UVW",
        points=points,
        ephemeris_start=ephemeris_start,
        ephemeris_stop=ephemeris_stop,
    )
