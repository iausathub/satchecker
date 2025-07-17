# ruff: noqa: S101
from datetime import datetime, timedelta, timezone

import pytest
from astropy.time import Time
from tests.conftest import FakeSatelliteRepository, FakeTLERepository
from tests.factories.satellite_factory import (
    SatelliteDesignationFactory,
    SatelliteFactory,
)
from tests.factories.tle_factory import TLEFactory

from api.domain.models.satellite_designation import SatelliteDesignation
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


class BrokenTLE:
    """Mock TLE that raises exceptions when accessing certain attributes"""

    def __init__(self, broken_attr=None, sat_number=25544, sat_name="ISS"):
        self.broken_attr = broken_attr
        self.satellite = BrokenSatellite(broken_attr, sat_number, sat_name)
        self.tle_line1 = "1 25544U 98067A   21001.00000000  .00001000  00000-0  10000-3 0  9990"  # noqa: E501
        self.tle_line2 = "2 25544  51.6400 000.0000 0000000   0.0000   0.0000 15.50000000000000"  # noqa: E501
        self.epoch = datetime.now()
        self.date_collected = datetime.now()
        self.data_source = "test"

    def __getattribute__(self, name):
        broken_attr = object.__getattribute__(self, "broken_attr")
        if name == broken_attr:
            raise AttributeError(f"Broken attribute: {name}")
        return object.__getattribute__(self, name)


class BrokenSatellite:
    """Mock satellite that raises exceptions when accessing certain attributes"""

    def __init__(self, broken_attr=None, sat_number=25544, sat_name="ISS"):
        self.broken_attr = broken_attr
        self.object_id = "1998-067A"
        self.rcs_size = "LARGE"
        self.launch_date = datetime.now()
        self.decay_date = None
        self.object_type = "PAYLOAD"
        self.generation = "v1.0"
        self.constellation = "ISS"
        self.designations = [
            SatelliteDesignation(
                sat_name=sat_name,
                sat_number=sat_number,
                valid_from=datetime.now(),
                valid_to=None,
            )
        ]

    def __getattribute__(self, name):
        broken_attr = object.__getattribute__(self, "broken_attr")
        if name == broken_attr:
            raise AttributeError(f"Broken satellite attribute: {name}")
        return object.__getattribute__(self, name)

    def get_current_designation(self):
        return self.designations[0]

    def get_designation_at_date(self, date):
        return self.designations[0]


def test_get_tle_data():
    epoch = datetime(2021, 1, 1, tzinfo=timezone.utc)
    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_name="ISS",
                sat_number=25544,
                valid_from=datetime(1957, 10, 4, tzinfo=timezone.utc),
                valid_to=None,
            )
        ]
    )
    tle_1 = TLEFactory(satellite=satellite)
    tle_2 = TLEFactory(satellite=satellite)
    tle_repo = FakeTLERepository([tle_1, tle_2])

    results = get_tle_data(tle_repo, "ISS", "name", None, None, "test", "1.0")
    assert len(results) == 2
    assert results[0]["satellite_name"] == "ISS"
    assert results[1]["satellite_name"] == "ISS"
    assert results[0]["satellite_id"] == satellite.get_current_designation().sat_number
    assert results[1]["satellite_id"] == satellite.get_current_designation().sat_number
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
        tle_repo,
        satellite.get_current_designation().sat_number,
        "catalog",
        None,
        None,
        "test",
        "1.0",
    )
    assert len(results) == 2

    results = get_tle_data(tle_repo, 12345, "catalog", None, None, "test", "1.0")
    assert len(results) == 0

    tle_1.epoch = epoch
    tle_2.epoch = epoch + timedelta(days=365)
    results = get_tle_data(
        tle_repo,
        "ISS",
        "name",
        datetime(2020, 1, 1, tzinfo=timezone.utc),
        datetime(2021, 1, 2, tzinfo=timezone.utc),
        "test",
        "1.0",
    )
    assert len(results) == 1

    results = get_tle_data(tle_repo, 12345, "id", None, None, "test", "1.0")
    assert len(results) == 0


def test_get_ids_for_satellite_name():
    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_name="ISS",
                sat_number=25544,
                valid_from=datetime(2024, 1, 1),
                valid_to=None,
            )
        ]
    )
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")
    assert len(results) == 1
    assert results[0]["name"] == "ISS"
    assert results[0]["norad_id"] == 25544
    assert results[0]["valid_from"] == format_date(datetime(2024, 1, 1))
    assert results[0]["valid_to"] is None

    results = get_ids_for_satellite_name(sat_repo, "not_found", "test", "1.0")
    assert len(results) == 0


def test_get_ids_for_satellite_name_no_match():
    sat_repo = FakeSatelliteRepository([])
    results = get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")
    assert len(results) == 0


def test_get_ids_for_satellite_name_multiple_matches():
    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_name="ISS",
                sat_number=25545,
                valid_from=datetime(2023, 1, 1),
                valid_to=datetime(2024, 1, 1),
            ),
            SatelliteDesignationFactory(
                sat_name="ISS",
                sat_number=25544,
                valid_from=datetime(2024, 1, 1),
                valid_to=None,
            ),
        ]
    )
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")
    assert len(results) == 2
    assert results[0]["name"] == "ISS"
    assert results[0]["norad_id"] == 25545
    assert results[0]["valid_from"] == format_date(datetime(2023, 1, 1))
    assert results[0]["valid_to"] == format_date(datetime(2024, 1, 1))
    assert results[1]["name"] == "ISS"
    assert results[1]["norad_id"] == 25544
    assert results[1]["valid_from"] == format_date(datetime(2024, 1, 1))
    assert results[1]["valid_to"] is None


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
    satellite = SatelliteFactory(
        designations=[SatelliteDesignationFactory(sat_number=25544)]
    )
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")
    assert len(results) == 1
    assert results[0]["name"] == satellite.get_current_designation().sat_name
    assert results[0]["norad_id"] == 25544
    assert results[0]["valid_from"] == satellite.get_current_designation().valid_from
    assert results[0]["valid_to"] == satellite.get_current_designation().valid_to

    results = get_names_for_satellite_id(sat_repo, 99999, "test", "1.0")
    assert len(results) == 0


def test_get_names_for_satellite_id_no_match():
    sat_repo = FakeSatelliteRepository([])
    results = get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")
    assert len(results) == 0


def test_get_names_for_satellite_id_multiple_matches():
    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_name="ISS",
                sat_number=25544,
                valid_from=datetime(2024, 1, 1),
                valid_to=datetime(2024, 1, 2),
            ),
            SatelliteDesignationFactory(
                sat_name="ISS",
                sat_number=25544,
                valid_from=datetime(2024, 1, 2),
                valid_to=None,
            ),
        ]
    )

    sat_repo = FakeSatelliteRepository([satellite])
    results = get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")
    assert len(results) == 2
    assert results[0]["name"] == satellite.get_current_designation().sat_name
    assert results[0]["norad_id"] == 25544
    assert results[0]["valid_from"] == datetime(2024, 1, 1)
    assert results[0]["valid_to"] == datetime(2024, 1, 2)
    assert results[1]["name"] == satellite.get_current_designation().sat_name
    assert results[1]["norad_id"] == 25544
    assert results[1]["valid_from"] == datetime(2024, 1, 2)
    assert results[1]["valid_to"] is None


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
        designations=[
            SatelliteDesignationFactory(
                sat_name="ISS",
                sat_number=25544,
                valid_from=datetime.now(),
                valid_to=None,
            )
        ],
        decay_date=None,
    )
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_active_satellites(sat_repo, None, "test", "1.0")
    assert results["count"] == 1
    assert results["data"][0]["satellite_name"] == "ISS"
    assert (
        results["data"][0]["satellite_id"]
        == satellite.get_current_designation().sat_number
    )
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
        designations=[
            SatelliteDesignationFactory(
                sat_name="starlink1",
                sat_number=25544,
                valid_from=datetime(2019, 5, 10),
                valid_to=None,
            )
        ],
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
        designations=[
            SatelliteDesignationFactory(
                sat_name="starlink2",
                sat_number=25545,
                valid_from=datetime(2019, 5, 20),
                valid_to=None,
            )
        ],
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
        designations=[
            SatelliteDesignationFactory(
                sat_name="starlink3",
                sat_number=25546,
                valid_from=datetime(2020, 6, 10),
                valid_to=None,
            )
        ],
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
        designations=[
            SatelliteDesignationFactory(
                sat_name="starlink1",
                sat_number=25544,
                valid_from=datetime(2019, 5, 10),
                valid_to=None,
            )
        ],
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
        designations=[SatelliteDesignationFactory(sat_name="ISS")],
        decay_date=None,
        object_type="payload",
    )
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_active_satellites(sat_repo, "payload", "test", "1.0")
    assert results["count"] == 1
    assert results["data"][0]["satellite_name"] == "ISS"
    assert (
        results["data"][0]["satellite_id"]
        == satellite.get_current_designation().sat_number
    )
    assert results["data"][0]["international_designator"] == satellite.object_id
    assert results["data"][0]["rcs_size"] == satellite.rcs_size
    assert results["data"][0]["launch_date"] == satellite.launch_date.strftime(
        "%Y-%m-%d"
    )
    assert results["data"][0]["decay_date"] == satellite.decay_date
    assert results["data"][0]["object_type"] == satellite.object_type


def test_get_active_satellites_with_invalid_object_type():
    satellite = SatelliteFactory(
        designations=[SatelliteDesignationFactory(sat_name="ISS")],
        decay_date=None,
        object_type="payload",
    )
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_active_satellites(sat_repo, "invalid", "test", "1.0")
    assert results["count"] == 0


def test_get_all_tles_at_epoch_formatted():
    tle_repo = FakeTLERepository([])
    tle_1 = TLEFactory(
        satellite=SatelliteFactory(
            designations=[SatelliteDesignationFactory(sat_name="ISS")]
        ),
        epoch=datetime.now(),
    )
    tle_2 = TLEFactory(
        satellite=SatelliteFactory(
            designations=[SatelliteDesignationFactory(sat_name="ISS")]
        ),
        epoch=datetime.now(),
    )
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
        satellite=SatelliteFactory(
            designations=[SatelliteDesignationFactory(sat_number=25544)]
        ),
        epoch=datetime.now() - timedelta(days=1),
    )
    tle_2 = TLEFactory(
        satellite=SatelliteFactory(
            designations=[SatelliteDesignationFactory(sat_number=25544)]
        ),
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
        satellite=SatelliteFactory(
            designations=[SatelliteDesignationFactory(sat_number=25544)]
        ),
        epoch=epoch - timedelta(days=1),
    )
    tle_2 = TLEFactory(
        satellite=SatelliteFactory(
            designations=[SatelliteDesignationFactory(sat_number=25544)]
        ),
        epoch=epoch + timedelta(days=3),
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
        satellite=SatelliteFactory(
            designations=[SatelliteDesignationFactory(sat_number=25544)]
        ),
        epoch=epoch - timedelta(days=1),
    )
    tle_2 = TLEFactory(
        satellite=SatelliteFactory(
            designations=[SatelliteDesignationFactory(sat_number=25544)]
        ),
        epoch=epoch + timedelta(days=3),
    )
    tle_3 = TLEFactory(
        satellite=SatelliteFactory(
            designations=[SatelliteDesignationFactory(sat_number=25544)]
        ),
        epoch=epoch + timedelta(days=5),
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
        designations=[SatelliteDesignationFactory(sat_name="ISS", sat_number=25544)],
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


def test_get_tle_data_repository_exceptions():
    # Test connection exception
    tle_repo = FakeTLERepository([], RuntimeError("Database connection failed"))
    with pytest.raises(RuntimeError, match="Database connection failed"):
        get_tle_data(tle_repo, 25544, "catalog", None, None, "test", "1.0")

    # Test name exception
    tle_repo = FakeTLERepository([], ValueError("Invalid satellite name"))
    with pytest.raises(ValueError, match="Invalid satellite name"):
        get_tle_data(tle_repo, "ISS", "name", None, None, "test", "1.0")


def test_get_tle_data_formatting_exception():
    tle_repo = FakeTLERepository(
        [BrokenTLE("get_designation_at_date", sat_number=25544)]
    )

    with pytest.raises(
        AttributeError, match="Broken satellite attribute: get_designation_at_date"
    ):
        get_tle_data(tle_repo, 25544, "catalog", None, None, "test", "1.0")


def test_get_tles_around_epoch_repository_exception():
    tle_repo = FakeTLERepository([], ConnectionError("Connection timeout"))

    with pytest.raises(ConnectionError, match="Connection timeout"):
        get_tles_around_epoch_results(
            tle_repo, 25544, "catalog", datetime.now(), 1, 1, "test", "1.0"
        )


def test_get_tles_around_epoch_formatting_exception():
    tle_repo = FakeTLERepository([BrokenTLE("tle_line1", sat_number=25544)])

    with pytest.raises(AttributeError, match="Broken attribute: tle_line1"):
        get_tles_around_epoch_results(
            tle_repo, 25544, "catalog", datetime.now(), 1, 1, "test", "1.0"
        )


def test_get_nearest_tle_repository_exception():
    tle_repo = FakeTLERepository([], OSError("TLE not found"))

    with pytest.raises(OSError, match="TLE not found"):
        get_nearest_tle_result(
            tle_repo, 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_nearest_tle_formatting_exception():
    tle_repo = FakeTLERepository([BrokenTLE("epoch", sat_number=25544)])

    with pytest.raises(AttributeError, match="Broken attribute: epoch"):
        get_nearest_tle_result(
            tle_repo, 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_adjacent_tle_repository_exception():
    tle_repo = FakeTLERepository([], MemoryError("Out of memory"))

    with pytest.raises(MemoryError, match="Out of memory"):
        get_adjacent_tle_results(
            tle_repo, 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_adjacent_tle_formatting_exceptions():
    # Test TXT exception
    tle_repo = FakeTLERepository(
        [BrokenTLE("get_designation_at_date", sat_number=25544)]
    )
    with pytest.raises(
        AttributeError, match="Broken satellite attribute: get_designation_at_date"
    ):
        get_adjacent_tle_results(
            tle_repo, 25544, "catalog", datetime.now(), "test", "1.0", "txt"
        )

    # Test JSON exception
    tle_repo = FakeTLERepository([BrokenTLE("tle_line2", sat_number=25544)])
    with pytest.raises(AttributeError, match="Broken attribute: tle_line2"):
        get_adjacent_tle_results(
            tle_repo, 25544, "catalog", datetime.now(), "test", "1.0", "json"
        )


def test_get_satellite_data_repository_exceptions():
    # Test by ID exception
    sat_repo = FakeSatelliteRepository([], KeyError("Satellite not found"))
    with pytest.raises(KeyError, match="Satellite not found"):
        get_satellite_data(sat_repo, 25544, "catalog", "test", "1.0")

    # Test by name exception
    sat_repo = FakeSatelliteRepository([], ValueError("Invalid name format"))
    with pytest.raises(ValueError, match="Invalid name format"):
        get_satellite_data(sat_repo, "ISS", "name", "test", "1.0")


def test_get_satellite_data_formatting_exception():
    sat_repo = FakeSatelliteRepository([BrokenSatellite("object_id", 25544, "ISS")])

    with pytest.raises(AttributeError, match="Broken satellite attribute: object_id"):
        get_satellite_data(sat_repo, 25544, "catalog", "test", "1.0")


def test_get_starlink_generations_repository_exception():
    sat_repo = FakeSatelliteRepository([], RuntimeError("Query failed"))

    with pytest.raises(RuntimeError, match="Query failed"):
        get_starlink_generations(sat_repo, "test", "1.0")


def test_get_active_satellites_repository_exception():
    sat_repo = FakeSatelliteRepository([], OSError("Database error"))

    with pytest.raises(OSError, match="Database error"):
        get_active_satellites(sat_repo, None, "test", "1.0")


def test_get_active_satellites_formatting_exception():
    sat_repo = FakeSatelliteRepository([BrokenSatellite("launch_date", 25544, "ISS")])

    with pytest.raises(AttributeError, match="Broken satellite attribute: launch_date"):
        get_active_satellites(sat_repo, None, "test", "1.0")


def test_get_all_tles_at_epoch_repository_exception():
    tle_repo = FakeTLERepository([], TimeoutError("Query timeout"))

    with pytest.raises(TimeoutError, match="Query timeout"):
        get_all_tles_at_epoch_formatted(
            tle_repo, datetime.now(), "json", 1, 100, "test", "1.0"
        )


def test_get_all_tles_at_epoch_formatting_exceptions():
    # Test TXT exception
    tle_repo = FakeTLERepository([BrokenTLE("tle_line1")])
    with pytest.raises(AttributeError, match="Broken attribute: tle_line1"):
        get_all_tles_at_epoch_formatted(
            tle_repo, datetime.now(), "txt", 1, 100, "test", "1.0"
        )

    # Test JSON exception
    tle_repo = FakeTLERepository([BrokenTLE("get_designation_at_date")])
    with pytest.raises(
        AttributeError, match="Broken satellite attribute: get_designation_at_date"
    ):
        get_all_tles_at_epoch_formatted(
            tle_repo, datetime.now(), "json", 1, 100, "test", "1.0"
        )


def test_satellite_name_id_repository_exceptions():
    sat_repo = FakeSatelliteRepository([], PermissionError("Access denied"))
    with pytest.raises(PermissionError, match="Access denied"):
        get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")

    sat_repo = FakeSatelliteRepository([], LookupError("ID not found"))
    with pytest.raises(LookupError, match="ID not found"):
        get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")
