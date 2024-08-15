# ruff: noqa: S101
from datetime import datetime

import pytest
from tests.conftest import FakeSatelliteRepository, FakeTLERepository
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.services.tools_service import (
    get_ids_for_satellite_name,
    get_names_for_satellite_id,
    get_tle_data,
)


def test_get_tle_data():
    satellite = SatelliteFactory(sat_name="ISS")
    tle_1 = TLEFactory(satellite=satellite)
    tle_2 = TLEFactory(satellite=satellite)
    tle_repo = FakeTLERepository([tle_1, tle_2])

    results = get_tle_data(tle_repo, "ISS", "name", None, None, "test", "1.0")
    assert len(results) == 2
    assert results[0]["satellite_name"] == "ISS"
    assert results[1]["satellite_name"] == "ISS"
    assert results[0]["satellite_id"] == satellite.sat_number
    assert results[1]["satellite_id"] == satellite.sat_number
    assert any(tle_1.tle_line1 in result.values() for result in results)
    assert any(tle_1.tle_line2 in result.values() for result in results)
    assert any(tle_2.tle_line1 in result.values() for result in results)
    assert any(tle_2.tle_line2 in result.values() for result in results)
    assert any(
        tle_1.epoch.strftime("%Y-%m-%d %H:%M:%S %Z") in result.values()
        for result in results
    )
    assert any(
        tle_2.epoch.strftime("%Y-%m-%d %H:%M:%S %Z") in result.values()
        for result in results
    )
    assert any(
        tle_1.date_collected.strftime("%Y-%m-%d %H:%M:%S %Z") in result.values()
        for result in results
    )
    assert any(
        tle_2.date_collected.strftime("%Y-%m-%d %H:%M:%S %Z") in result.values()
        for result in results
    )

    results = get_tle_data(tle_repo, "not_found", "name", None, None, "test", "1.0")
    assert len(results) == 0

    results = get_tle_data(
        tle_repo, satellite.sat_number, "catalog", None, None, "test", "1.0"
    )
    assert len(results) == 2

    results = get_tle_data(tle_repo, 12345, "catalog", None, None, "test", "1.0")
    assert len(results) == 0

    tle_1.epoch = datetime(2021, 1, 1)
    tle_2.epoch = datetime(2022, 1, 2)
    results = get_tle_data(
        tle_repo,
        "ISS",
        "name",
        datetime(2020, 1, 1),
        datetime(2021, 1, 2),
        "test",
        "1.0",
    )
    assert len(results) == 1

    results = get_tle_data(tle_repo, 12345, "id", None, None, "test", "1.0")
    assert len(results) == 0


def test_get_ids_for_satellite_name():
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")
    assert len(results) == 1
    assert results[0]["name"] == "ISS"
    assert results[0]["norad_id"] == satellite.sat_number
    assert results[0]["date_added"] == datetime(2024, 1, 1).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )
    assert results[0]["is_current_version"] == satellite.has_current_sat_number

    results = get_ids_for_satellite_name(sat_repo, "not_found", "test", "1.0")
    assert len(results) == 0


def test_get_ids_for_satellite_name_no_match():
    sat_repo = FakeSatelliteRepository([])
    results = get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")
    assert len(results) == 0


def test_get_ids_for_satellite_name_multiple_matches():
    satellite = SatelliteFactory(sat_name="ISS")
    satellite_new = SatelliteFactory(sat_name="ISS")
    sat_repo = FakeSatelliteRepository([satellite, satellite_new])
    results = get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")
    assert len(results) == 2
    assert results[0]["name"] == "ISS"
    assert results[0]["norad_id"] == satellite.sat_number
    assert results[0]["date_added"] == datetime(2024, 1, 1).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )
    assert results[0]["is_current_version"] == satellite.has_current_sat_number
    assert results[1]["name"] == "ISS"
    assert results[1]["norad_id"] == satellite_new.sat_number
    assert results[1]["date_added"] == datetime(2024, 1, 1).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )
    assert results[1]["is_current_version"] == satellite_new.has_current_sat_number


def test_get_ids_for_satellite_name_errors():
    sat_repo = FakeSatelliteRepository([])

    # missing parameters
    with pytest.raises(TypeError):
        results = get_ids_for_satellite_name(sat_repo, "ISS")

    with pytest.raises(TypeError):
        results = get_ids_for_satellite_name(  # noqa: F841
            sat_repo=sat_repo, satellite_name="ISS", api_source="test"
        )


def test_get_names_for_satellite_id():
    satellite = SatelliteFactory(sat_number=25544)
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")
    assert len(results) == 1
    assert results[0]["name"] == satellite.sat_name
    assert results[0]["norad_id"] == 25544
    assert results[0]["date_added"] == datetime(2024, 1, 1).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )
    assert results[0]["is_current_version"] == satellite.has_current_sat_number

    results = get_names_for_satellite_id(sat_repo, 99999, "test", "1.0")
    assert len(results) == 0


def test_get_names_for_satellite_id_no_match():
    sat_repo = FakeSatelliteRepository([])
    results = get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")
    assert len(results) == 0


def test_get_names_for_satellite_id_multiple_matches():
    satellite = SatelliteFactory(sat_number=25544)
    satellite_new = SatelliteFactory(sat_number=25544)
    sat_repo = FakeSatelliteRepository([satellite, satellite_new])
    results = get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")
    assert len(results) == 2
    assert results[0]["name"] == satellite.sat_name
    assert results[0]["norad_id"] == 25544
    assert results[0]["date_added"] == datetime(2024, 1, 1).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )
    assert results[0]["is_current_version"] == satellite.has_current_sat_number
    assert results[1]["name"] == satellite_new.sat_name
    assert results[1]["norad_id"] == 25544
    assert results[1]["date_added"] == datetime(2024, 1, 1).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )
    assert results[1]["is_current_version"] == satellite_new.has_current_sat_number


def test_get_names_for_satellite_id_errors():
    sat_repo = FakeSatelliteRepository([])

    # missing parameters
    with pytest.raises(TypeError):
        results = get_names_for_satellite_id(sat_repo, 123)

    with pytest.raises(TypeError):
        results = get_names_for_satellite_id(  # noqa: F841
            sat_repo=sat_repo, satellite_id=123, api_source="test"
        )
