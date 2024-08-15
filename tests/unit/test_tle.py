# ruff: noqa: S101
import pytest
from tests.factories import TLEFactory


@pytest.fixture
def tle_factory():
    def _factory(*args, **kwargs):
        return TLEFactory(*args, **kwargs)

    return _factory


def test_initialization(tle_factory):
    tle = tle_factory()
    assert tle.date_collected is not None
    assert tle.tle_line1 is not None
    assert tle.tle_line2 is not None
    assert tle.epoch is not None
    assert tle.is_supplemental is not None
    assert tle.data_source is not None
    assert tle.satellite is not None


def test_repr(tle_factory):
    tle = tle_factory()
    assert repr(tle) == f"<TLE {tle.satellite}>"


def test_eq(tle_factory):
    tle1 = tle_factory()
    tle2 = tle_factory()
    assert tle1 != tle2
