# ruff: noqa: S101
import pytest
from tests.factories import SatelliteFactory


@pytest.fixture
def satellite_factory():
    def _factory(*args, **kwargs):
        return SatelliteFactory(*args, **kwargs)

    return _factory


def test_initialization(satellite_factory):
    satellite = satellite_factory()
    assert satellite.constellation is not None
    assert satellite.rcs_size is not None
    assert satellite.launch_date is not None
    assert satellite.decay_date is not None
    assert satellite.object_id is not None
    assert satellite.object_type is not None
    assert satellite.designations is not None


def test_repr(satellite_factory):
    satellite = satellite_factory()
    assert str(satellite) == f"<Satellite {satellite.object_id}>"


def test_eq(satellite_factory):
    satellite_a = satellite_factory()
    satellite_b = satellite_factory()
    assert satellite_a != satellite_b
