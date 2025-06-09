# ruff: noqa: S101
from datetime import datetime, timedelta

import pytest
from astropy.time import Time
from tests.conftest import FakeSatelliteRepository, FakeTLERepository
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.services.tools_service import (
    get_active_satellites,
    get_adjacent_tle_results,
    get_all_tles_at_epoch_formatted,
    get_ids_for_satellite_name,
    get_names_for_satellite_id,
    get_nearest_tle_result,
    get_satellite_data,
    get_starlink_generations,
    get_tle_data,
    get_tles_around_epoch_results,
)
from api.utils.output_utils import format_date


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
    assert any(format_date(tle_1.epoch) in result.values() for result in results)
    assert any(format_date(tle_2.epoch) in result.values() for result in results)
    assert any(
        format_date(tle_1.date_collected) in result.values() for result in results
    )
    assert any(
        format_date(tle_2.date_collected) in result.values() for result in results
    )
    assert any(tle_1.data_source in result.values() for result in results)
    assert any(tle_2.data_source in result.values() for result in results)

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
    assert results[0]["date_added"] == format_date(datetime(2024, 1, 1))
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
    assert results[0]["date_added"] == format_date(datetime(2024, 1, 1))
    assert results[0]["is_current_version"] == satellite.has_current_sat_number
    assert results[1]["name"] == "ISS"
    assert results[1]["norad_id"] == satellite_new.sat_number
    assert results[1]["date_added"] == format_date(datetime(2024, 1, 1))
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
    assert results[0]["date_added"] == format_date(datetime(2024, 1, 1))
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
    assert results[0]["date_added"] == format_date(datetime(2024, 1, 1))
    assert results[0]["is_current_version"] == satellite.has_current_sat_number
    assert results[1]["name"] == satellite_new.sat_name
    assert results[1]["norad_id"] == 25544
    assert results[1]["date_added"] == format_date(datetime(2024, 1, 1))
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


def test_get_active_satellites():
    sat_repo = FakeSatelliteRepository([])
    results = get_active_satellites(sat_repo, None, "test", "1.0")
    assert results["count"] == 0

    satellite = SatelliteFactory(
        sat_name="ISS", has_current_sat_number=True, decay_date=None
    )
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_active_satellites(sat_repo, None, "test", "1.0")
    assert results["count"] == 1
    assert results["data"][0]["satellite_name"] == "ISS"
    assert results["data"][0]["satellite_id"] == satellite.sat_number
    assert results["data"][0]["international_designator"] == satellite.object_id
    assert results["data"][0]["rcs_size"] == satellite.rcs_size
    assert results["data"][0]["launch_date"] == satellite.launch_date.strftime(
        "%Y-%m-%d"
    )
    assert results["data"][0]["decay_date"] == satellite.decay_date
    assert results["data"][0]["object_type"] == satellite.object_type


def test_get_starlink_generations():
    sat_repo = FakeSatelliteRepository([])
    results = get_starlink_generations(sat_repo, "test", "1.0")
    assert results["count"] == 0

    satellite = SatelliteFactory(
        sat_name="starlink1",
        has_current_sat_number=True,
        launch_date=datetime(2019, 5, 10),
        generation="gen1",
    )

    sat_repo = FakeSatelliteRepository([satellite])
    results = get_starlink_generations(sat_repo, "test", "1.0")
    assert results["count"] == 1
    assert results["data"][0]["generation"] == "gen1"
    assert results["data"][0]["earliest_launch_date"] == "2019-05-10 00:00:00 UTC"
    assert results["data"][0]["latest_launch_date"] == "2019-05-10 00:00:00 UTC"

    satellite2 = SatelliteFactory(
        sat_name="starlink2",
        has_current_sat_number=True,
        launch_date=datetime(2019, 5, 20),
        generation="gen1",
    )
    sat_repo = FakeSatelliteRepository([satellite, satellite2])
    results = get_starlink_generations(sat_repo, "test", "1.0")
    assert results["count"] == 1  # Only one generation
    assert results["data"][0]["generation"] == "gen1"
    assert results["data"][0]["earliest_launch_date"] == "2019-05-10 00:00:00 UTC"
    assert results["data"][0]["latest_launch_date"] == "2019-05-20 00:00:00 UTC"

    satellite3 = SatelliteFactory(
        sat_name="starlink3",
        has_current_sat_number=True,
        launch_date=datetime(2020, 6, 10),
        generation="gen2",
    )
    sat_repo = FakeSatelliteRepository([satellite, satellite2, satellite3])
    results = get_starlink_generations(sat_repo, "test", "1.0")
    assert results["count"] == 2  # Two generations
    assert results["data"][0]["generation"] == "gen1"
    assert results["data"][0]["earliest_launch_date"] == "2019-05-10 00:00:00 UTC"
    assert results["data"][0]["latest_launch_date"] == "2019-05-20 00:00:00 UTC"
    assert results["data"][1]["generation"] == "gen2"
    assert results["data"][1]["earliest_launch_date"] == "2020-06-10 00:00:00 UTC"
    assert results["data"][1]["latest_launch_date"] == "2020-06-10 00:00:00 UTC"


def test_get_starlink_generations_errors():
    # Create a satellite with an invalid launch date type
    satellite = SatelliteFactory(
        sat_name="starlink1",
        has_current_sat_number=True,
        launch_date="invalid_date",  # This will cause TypeError in the repository
        generation="gen1",
    )
    sat_repo = FakeSatelliteRepository([satellite])
    with pytest.raises(TypeError):
        results = get_starlink_generations(sat_repo, "test", "1.0")

    with pytest.raises(AttributeError):
        results = get_starlink_generations(None, "test", "1.0")  # noqa: F841


def test_get_active_satellites_with_object_type():
    satellite = SatelliteFactory(
        sat_name="ISS",
        has_current_sat_number=True,
        decay_date=None,
        object_type="payload",
    )
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_active_satellites(sat_repo, "payload", "test", "1.0")
    assert results["count"] == 1
    assert results["data"][0]["satellite_name"] == "ISS"
    assert results["data"][0]["satellite_id"] == satellite.sat_number
    assert results["data"][0]["international_designator"] == satellite.object_id
    assert results["data"][0]["rcs_size"] == satellite.rcs_size
    assert results["data"][0]["launch_date"] == satellite.launch_date.strftime(
        "%Y-%m-%d"
    )
    assert results["data"][0]["decay_date"] == satellite.decay_date
    assert results["data"][0]["object_type"] == satellite.object_type


def test_get_active_satellites_with_invalid_object_type():
    satellite = SatelliteFactory(
        sat_name="ISS",
        has_current_sat_number=True,
        decay_date=None,
        object_type="payload",
    )
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_active_satellites(sat_repo, "invalid", "test", "1.0")
    assert results["count"] == 0


def test_get_all_tles_at_epoch_formatted():
    tle_repo = FakeTLERepository([])
    tle_1 = TLEFactory(satellite=SatelliteFactory(sat_name="ISS"), epoch=datetime.now())
    tle_2 = TLEFactory(satellite=SatelliteFactory(sat_name="ISS"), epoch=datetime.now())
    tle_repo = FakeTLERepository([tle_1, tle_2])
    results = get_all_tles_at_epoch_formatted(
        tle_repo, datetime.now(), "json", 1, 100, "test", "1.0"
    )

    # Results should be a list with one dictionary
    assert isinstance(results, list)
    assert len(results) == 1

    # Check the structure matches the actual API response
    result = results[0]
    assert result["per_page"] == 100
    assert result["page"] == 1
    assert len(result["data"]) == 2
    assert result["source"] == "test"
    assert result["version"] == "1.0"

    # Check the data contents
    for tle_data in result["data"]:
        assert "satellite_name" in tle_data
        assert "satellite_id" in tle_data
        assert "tle_line1" in tle_data
        assert "tle_line2" in tle_data
        assert "epoch" in tle_data
        assert "date_collected" in tle_data
        assert isinstance(tle_data["satellite_name"], str)
        assert isinstance(tle_data["satellite_id"], int)
        assert isinstance(tle_data["tle_line1"], str)
        assert isinstance(tle_data["tle_line2"], str)
        assert tle_data["satellite_name"] == "ISS"

    results = get_all_tles_at_epoch_formatted(
        tle_repo, datetime.now(), "txt", 1, 100, "test", "1.0"
    )
    text_content = results.getvalue().decode("utf-8")
    assert tle_1.tle_line1 in text_content
    assert tle_1.tle_line2 in text_content
    assert tle_2.tle_line1 in text_content
    assert tle_2.tle_line2 in text_content


def test_get_adjacent_tles():
    tle_repo = FakeTLERepository([])
    tle_1 = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544),
        epoch=datetime.now() - timedelta(days=1),
    )
    tle_2 = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544),
        epoch=datetime.now() + timedelta(days=1),
    )
    tle_repo = FakeTLERepository([tle_1, tle_2])
    epoch_jd = Time(datetime.now()).jd
    results = get_adjacent_tle_results(
        tle_repo, 25544, "catalog", epoch_jd, "test", "1.0"
    )
    assert len(results[0]["tle_data"]) == 2
    assert results[0]["tle_data"][0]["satellite_id"] == 25544
    assert results[0]["tle_data"][1]["satellite_id"] == 25544

    results = get_adjacent_tle_results(tle_repo, 1, "catalog", epoch_jd, "test", "1.0")
    assert len(results[0]["tle_data"]) == 0


def test_get_nearest_tle():
    tle_repo = FakeTLERepository([])
    epoch = datetime.now()
    tle_1 = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch - timedelta(days=1)
    )
    tle_2 = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch + timedelta(days=3)
    )
    tle_repo = FakeTLERepository([tle_1, tle_2])

    results = get_nearest_tle_result(tle_repo, 25544, "catalog", epoch, "test", "1.0")
    assert results[0]["tle_data"][0]["tle_line1"] == tle_1.tle_line1
    assert results[0]["tle_data"][0]["tle_line2"] == tle_1.tle_line2

    results = get_nearest_tle_result(tle_repo, 1, "catalog", epoch, "test", "1.0")
    assert len(results[0]["tle_data"]) == 0


def test_get_tles_around_epoch():
    tle_repo = FakeTLERepository([])
    epoch = datetime.now()
    tle_1 = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch - timedelta(days=1)
    )
    tle_2 = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch + timedelta(days=3)
    )
    tle_3 = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch + timedelta(days=5)
    )
    tle_repo = FakeTLERepository([tle_1, tle_2, tle_3])

    results = get_tles_around_epoch_results(
        tle_repo, 25544, "catalog", epoch, 2, 2, "test", "1.0"
    )
    assert len(results[0]["tle_data"]) == 3

    results = get_tles_around_epoch_results(
        tle_repo, 25544, "catalog", epoch, 1, 1, "test", "1.0"
    )
    assert len(results[0]["tle_data"]) == 2

    results = get_tles_around_epoch_results(
        tle_repo, 25544, "catalog", epoch, 1, 1, "test", "1.0"
    )
    assert len(results[0]["tle_data"]) == 2

    results = get_tles_around_epoch_results(
        tle_repo, 25544, "catalog", epoch, 0, 2, "test", "1.0"
    )
    assert len(results[0]["tle_data"]) == 2


def test_get_satellite_data():
    # Satellite with all fields populated
    satellite = SatelliteFactory(
        sat_name="ISS",
        sat_number=25544,
        object_id="1998-067A",
        rcs_size="LARGE",
        launch_date=datetime(1998, 11, 20),
        decay_date=None,
        object_type="PAYLOAD",
        generation="v1.0",
        constellation="ISS",
    )
    sat_repo = FakeSatelliteRepository([satellite])

    # Retrieval by name
    results = get_satellite_data(sat_repo, "ISS", "name", "test", "1.0")
    assert len(results) == 1
    assert results[0]["satellite_name"] == "ISS"
    assert results[0]["satellite_id"] == 25544
    assert results[0]["international_designator"] == "1998-067A"
    assert results[0]["rcs_size"] == "LARGE"
    assert results[0]["launch_date"] == "1998-11-20"
    assert results[0]["decay_date"] is None
    assert results[0]["object_type"] == "PAYLOAD"
    assert results[0]["generation"] == "v1.0"
    assert results[0]["constellation"] == "ISS"

    # Retrieval by catalog number
    results = get_satellite_data(sat_repo, "25544", "catalog", "test", "1.0")
    assert len(results) == 1
    assert results[0]["satellite_name"] == "ISS"

    # Sat not found
    results = get_satellite_data(sat_repo, "NONEXISTENT", "name", "test", "1.0")
    assert len(results) == 0
