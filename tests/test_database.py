# ruff: noqa: S101
"""
os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
from core.database.models import TLE, Satellite  # noqa: E402
from core.versions.v1.tasks import propagate_satellite_skyfield
from sqlalchemy.orm import sessionmaker

assert_precision = 0.000001


@pytest.fixture(scope="function")
def db_session(app):


    with app.app_context():
        from core.extensions import db as database

        database.create_all()
        Session = sessionmaker(bind=database.engine)
        Satellite.metadata.create_all(database.engine)
        TLE.metadata.create_all(database.engine)
        # session = Session()
        yield database.session
        database.session.remove()
        database.drop_all()


@pytest.fixture
def satellite_factory(faker, db_session):
    from tests.factories.satellite_factory import SatelliteFactory

    def _factory(*args, **kwargs):
        SatelliteFactory._meta.sqlalchemy_session = db_session
        return SatelliteFactory(*args, **kwargs)

    return _factory


@pytest.fixture
def tle_factory(faker, db_session):
    from tests.factories.tle_factory import TLEFactory

    def _factory(*args, **kwargs):
        TLEFactory._meta.sqlalchemy_session = db_session
        return TLEFactory(*args, **kwargs)

    return _factory


def test_data_creation(tle_factory, satellite_factory, db_session):
    satellite = satellite_factory()
    assert satellite.sat_number is not None

    tle = tle_factory()
    results = propagate_satellite_skyfield(
        tle.tle_line1, tle.tle_line2, 33, -110, 0, 2460322.06041667
    )
    assert results.ra is not None
"""
