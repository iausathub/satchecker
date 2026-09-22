# ruff: noqa: S101
import io
import zipfile
from datetime import datetime, timedelta, timezone

import pyarrow.parquet as pq
import pytest
from astropy.time import Time
from sgp4.api import Satrec
from tests.conftest import (
    FakeEphemerisRepository,
    FakeOrbitalElementsRepository,
    FakeSatelliteRepository,
    FakeTLERepository,
)
from tests.factories.ephemeris_factory import InterpolableEphemerisFactory
from tests.factories.orbital_elements_factory import OrbitalElementsFactory
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.services.tools_service import (
    get_active_satellites,
    get_adjacent_orbital_data_results,
    get_all_ephemeris_data_at_epoch_formatted,
    get_all_orbital_data_at_epoch_formatted,
    get_ephemeris_data_for_satellite_at_epoch_formatted,
    get_ids_for_satellite_name,
    get_names_for_satellite_id,
    get_nearest_orbital_data_result,
    get_orbital_data,
    get_orbital_data_around_epoch_results,
    get_satellite_data,
    get_starlink_generations,
)
from api.utils.output_utils import (
    EPHEMERIS_CSV_COLUMNS,
    EPHEMERIS_PARQUET_COLUMNS,
    format_date,
)


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


class BrokenOMM:
    """Mock OMM that raises exceptions when accessing certain attributes"""

    def __init__(self, broken_attr=None, sat_number=25544, sat_name="ISS"):
        self.broken_attr = broken_attr
        self.satellite = BrokenSatellite(broken_attr, sat_number, sat_name)
        self.mean_motion = 15.5
        self.eccentricity = 0.0002
        self.inclination = 51.64
        self.ra_of_ascending_node = 247.4
        self.arg_of_pericenter = 130.5
        self.mean_anomaly = 325.0
        self.ephemeris_type = 0
        self.classification_type = "U"
        self.element_set_no = 999
        self.rev_at_epoch = 12345
        self.bstar = 0.0001
        self.mean_motion_dot = 1e-5
        self.mean_motion_ddot = 0.0
        self.epoch = datetime.now()
        self.date_collected = datetime.now()
        self.data_source = "test"

    def to_omm_dict(self):
        # Mirrors OrbitalElements.to_omm_dict so a broken element attribute
        # surfaces from within serialization, like the real code path.
        return {
            "OBJECT_NAME": self.satellite.sat_name,
            "OBJECT_ID": self.satellite.object_id or "",
            "MEAN_MOTION": self.mean_motion,
            "ECCENTRICITY": self.eccentricity,
            "INCLINATION": self.inclination,
            "RA_OF_ASC_NODE": self.ra_of_ascending_node,
            "ARG_OF_PERICENTER": self.arg_of_pericenter,
            "MEAN_ANOMALY": self.mean_anomaly,
            "NORAD_CAT_ID": self.satellite.sat_number,
        }

    def __getattribute__(self, name):
        broken_attr = object.__getattribute__(self, "broken_attr")
        if name == broken_attr:
            raise AttributeError(f"Broken attribute: {name}")
        return object.__getattribute__(self, name)


class BrokenSatellite:
    """Mock satellite that raises exceptions when accessing certain attributes"""

    def __init__(self, broken_attr=None, sat_number=25544, sat_name="ISS"):
        self.broken_attr = broken_attr
        self.sat_name = sat_name
        self.sat_number = sat_number
        self.object_id = "1998-067A"
        self.rcs_size = "LARGE"
        self.launch_date = datetime.now()
        self.decay_date = None
        self.object_type = "PAYLOAD"
        self.generation = "v1.0"
        self.constellation = "ISS"
        self.has_current_sat_number = True  # Required for fake repository filtering

    def __getattribute__(self, name):
        broken_attr = object.__getattribute__(self, "broken_attr")
        if name == broken_attr:
            raise AttributeError(f"Broken satellite attribute: {name}")
        return object.__getattribute__(self, name)


def test_get_tle_data():
    satellite = SatelliteFactory(sat_name="ISS")
    tle_1 = TLEFactory(satellite=satellite)
    tle_2 = TLEFactory(satellite=satellite)
    tle_repo = FakeTLERepository([tle_1, tle_2])

    results = get_orbital_data(
        tle_repo, None, "tle", "ISS", "name", None, None, "test", "1.0"
    )
    assert results["count"] == 2
    assert results["data"][0]["satellite_name"] == "ISS"
    assert results["data"][1]["satellite_name"] == "ISS"
    assert results["data"][0]["satellite_id"] == satellite.sat_number
    assert results["data"][1]["satellite_id"] == satellite.sat_number
    assert any(tle_1.tle_line1 in result.values() for result in results["data"])
    assert any(tle_1.tle_line2 in result.values() for result in results["data"])
    assert any(tle_2.tle_line1 in result.values() for result in results["data"])
    assert any(tle_2.tle_line2 in result.values() for result in results["data"])
    assert any(
        format_date(tle_1.epoch) in result.values() for result in results["data"]
    )
    assert any(
        format_date(tle_2.epoch) in result.values() for result in results["data"]
    )
    assert any(
        format_date(tle_1.date_collected) in result.values()
        for result in results["data"]
    )
    assert any(
        format_date(tle_2.date_collected) in result.values()
        for result in results["data"]
    )
    assert any(tle_1.data_source in result.values() for result in results["data"])
    assert any(tle_2.data_source in result.values() for result in results["data"])

    results = get_orbital_data(
        tle_repo, None, "tle", "not_found", "name", None, None, "test", "1.0"
    )
    assert results["count"] == 0

    results = get_orbital_data(
        tle_repo,
        None,
        "tle",
        satellite.sat_number,
        "catalog",
        None,
        None,
        "test",
        "1.0",
    )
    assert results["count"] == 2

    results = get_orbital_data(
        tle_repo, None, "tle", 12345, "catalog", None, None, "test", "1.0"
    )
    assert results["count"] == 0

    tle_1.epoch = datetime(2021, 1, 1)
    tle_2.epoch = datetime(2022, 1, 2)
    results = get_orbital_data(
        tle_repo,
        None,
        "tle",
        "ISS",
        "name",
        datetime(2020, 1, 1),
        datetime(2021, 1, 2),
        "test",
        "1.0",
    )
    assert results["count"] == 1

    results = get_orbital_data(
        tle_repo, None, "tle", 12345, "id", None, None, "test", "1.0"
    )
    assert results["count"] == 0


def test_get_ids_for_satellite_name():
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = FakeSatelliteRepository([satellite])
    results = get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")
    assert results["count"] == 1
    assert results["data"][0]["name"] == "ISS"
    assert results["data"][0]["norad_id"] == satellite.sat_number
    assert results["data"][0]["date_added"] == format_date(datetime(2024, 1, 1))
    assert results["data"][0]["is_current_version"] == satellite.has_current_sat_number

    results = get_ids_for_satellite_name(sat_repo, "not_found", "test", "1.0")
    assert results["count"] == 0


def test_get_ids_for_satellite_name_no_match():
    sat_repo = FakeSatelliteRepository([])
    results = get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")
    assert results["count"] == 0


def test_get_ids_for_satellite_name_multiple_matches():
    satellite = SatelliteFactory(sat_name="ISS")
    satellite_new = SatelliteFactory(sat_name="ISS")
    sat_repo = FakeSatelliteRepository([satellite, satellite_new])
    results = get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")
    assert results["count"] == 2
    assert results["data"][0]["name"] == "ISS"
    assert results["data"][0]["norad_id"] == satellite.sat_number
    assert results["data"][0]["date_added"] == format_date(datetime(2024, 1, 1))
    assert results["data"][0]["is_current_version"] == satellite.has_current_sat_number
    assert results["data"][1]["name"] == "ISS"
    assert results["data"][1]["norad_id"] == satellite_new.sat_number
    assert results["data"][1]["date_added"] == format_date(datetime(2024, 1, 1))
    assert (
        results["data"][1]["is_current_version"] == satellite_new.has_current_sat_number
    )


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
    assert results["count"] == 1
    assert results["data"][0]["name"] == satellite.sat_name
    assert results["data"][0]["norad_id"] == 25544
    assert results["data"][0]["date_added"] == format_date(datetime(2024, 1, 1))
    assert results["data"][0]["is_current_version"] == satellite.has_current_sat_number

    results = get_names_for_satellite_id(sat_repo, 99999, "test", "1.0")
    assert results["count"] == 0


def test_get_names_for_satellite_id_no_match():
    sat_repo = FakeSatelliteRepository([])
    results = get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")
    assert results["count"] == 0


def test_get_names_for_satellite_id_multiple_matches():
    satellite = SatelliteFactory(sat_number=25544)
    satellite_new = SatelliteFactory(sat_number=25544)
    sat_repo = FakeSatelliteRepository([satellite, satellite_new])
    results = get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")
    assert results["count"] == 2
    assert results["data"][0]["name"] == satellite.sat_name
    assert results["data"][0]["norad_id"] == 25544
    assert results["data"][0]["date_added"] == format_date(datetime(2024, 1, 1))
    assert results["data"][0]["is_current_version"] == satellite.has_current_sat_number
    assert results["data"][1]["name"] == satellite_new.sat_name
    assert results["data"][1]["norad_id"] == 25544
    assert results["data"][1]["date_added"] == format_date(datetime(2024, 1, 1))
    assert (
        results["data"][1]["is_current_version"] == satellite_new.has_current_sat_number
    )


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
    results = get_all_orbital_data_at_epoch_formatted(
        tle_repo, None, "tle", datetime.now(), "json", 1, 100, "test", "1.0"
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

    results = get_all_orbital_data_at_epoch_formatted(
        tle_repo, None, "tle", datetime.now(), "txt", 1, 100, "test", "1.0"
    )
    text_content = results.getvalue().decode("utf-8")
    assert tle_1.tle_line1 in text_content
    assert tle_1.tle_line2 in text_content
    assert tle_2.tle_line1 in text_content
    assert tle_2.tle_line2 in text_content


# Epoch after ORBITAL_ELEMENTS_CUTOFF (2026-07-13), where data is stored as OMM
# and the TLE endpoints must transparently convert it.
POST_CUTOFF_EPOCH = datetime(2026, 8, 1, tzinfo=timezone.utc)


def _post_cutoff_omm(sat_number, sat_name="FENGYUN 1C DEB"):
    """OMM record with realistic elements for a post-cutoff epoch."""
    return OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_name=sat_name, sat_number=sat_number),
        epoch=POST_CUTOFF_EPOCH,
        date_collected=POST_CUTOFF_EPOCH,
        data_source="celestrak",
        classification_type="U",
        mean_motion=14.52723026,
        eccentricity=0.0030132,
        inclination=98.5847,
        ra_of_ascending_node=13.2387,
        arg_of_pericenter=143.9377,
        mean_anomaly=216.3858,
        bstar=0.86550e-2,
        mean_motion_dot=0.00035853,
        mean_motion_ddot=0.0,
        rev_at_epoch=90668,
        ephemeris_type=0,
        element_set_no=999,
    )


def test_get_nearest_tle_after_cutoff_converts_omm():
    """After the cutoff, get-nearest-tle sources from the OMM store and returns
    the equivalent TLE lines, so the endpoint behaves the same as before it."""
    omm = _post_cutoff_omm(25544)
    tle_repo = FakeTLERepository([])
    omm_repo = FakeOrbitalElementsRepository([omm])

    results = get_nearest_orbital_data_result(
        tle_repo, omm_repo, "tle", 25544, "catalog", POST_CUTOFF_EPOCH, "test", "1.0"
    )

    orbital_data = results[0]["orbital_data"]
    assert len(orbital_data) == 1
    record = orbital_data[0]
    # TLE-shaped response, not the OMM element dict.
    assert "tle_line1" in record
    assert "tle_line2" in record
    assert "orbital_elements" not in record
    assert record["satellite_id"] == 25544

    # The converted lines parse back into the source orbit.
    satrec = Satrec.twoline2rv(record["tle_line1"], record["tle_line2"])
    assert satrec.inclo * 180 / 3.141592653589793 == pytest.approx(
        omm.inclination, abs=1e-3
    )


def test_get_all_tles_at_epoch_after_cutoff_converts_omm():
    """tles-at-epoch returns converted OMM records (json + txt) after cutoff."""
    tle_repo = FakeTLERepository([])
    omm_repo = FakeOrbitalElementsRepository(
        [_post_cutoff_omm(25544, "ISS"), _post_cutoff_omm(33591, "NOAA 19")]
    )

    results = get_all_orbital_data_at_epoch_formatted(
        tle_repo, omm_repo, "tle", POST_CUTOFF_EPOCH, "json", 1, 100, "test", "1.0"
    )
    data = results[0]["data"]
    assert len(data) == 2
    for record in data:
        assert "tle_line1" in record
        assert "tle_line2" in record
        assert "orbital_elements" not in record

    # txt format is a valid, non-empty TLE listing.
    txt = get_all_orbital_data_at_epoch_formatted(
        tle_repo, omm_repo, "tle", POST_CUTOFF_EPOCH, "txt", 1, 100, "test", "1.0"
    )
    text_content = txt.getvalue().decode("utf-8")
    assert "1 25544" in text_content
    assert "2 25544" in text_content


def test_get_tle_data_range_spanning_cutoff_merges_stores():
    """get-tle-data over a range spanning the cutoff returns a single continuous
    series: stored TLEs before the cutoff and converted OMM after it."""
    pre_cutoff_epoch = datetime(2026, 6, 1, tzinfo=timezone.utc)
    tle = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544),
        epoch=pre_cutoff_epoch,
    )
    tle_repo = FakeTLERepository([tle])
    omm_repo = FakeOrbitalElementsRepository([_post_cutoff_omm(25544)])

    results = get_orbital_data(
        tle_repo,
        omm_repo,
        "tle",
        25544,
        "catalog",
        datetime(2026, 5, 1, tzinfo=timezone.utc),
        datetime(2026, 9, 1, tzinfo=timezone.utc),
        "test",
        "1.0",
    )

    assert results["count"] == 2
    # Sorted by epoch: stored TLE first, converted OMM second.
    assert results["data"][0]["tle_line1"] == tle.tle_line1
    assert results["data"][1]["tle_line1"].startswith("1 25544")
    for record in results["data"]:
        assert "tle_line1" in record
        assert "tle_line2" in record


def test_get_all_omms_at_epoch_formatted():
    omm_repo = FakeOrbitalElementsRepository([])
    omm_1 = OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_name="ISS"), epoch=datetime.now()
    )
    omm_2 = OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_name="ISS"), epoch=datetime.now()
    )
    omm_repo = FakeOrbitalElementsRepository([omm_1, omm_2])
    results = get_all_orbital_data_at_epoch_formatted(
        None, omm_repo, "omm", datetime.now(), "json", 1, 100, "test", "1.0"
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

    # Check the data contents: SatChecker metadata wraps a nested
    # orbital_elements object using CCSDS OMM field names
    for omm_data in result["data"]:
        assert "satellite_name" in omm_data
        assert "satellite_id" in omm_data
        assert "orbital_elements" in omm_data
        assert "epoch" in omm_data
        assert "date_collected" in omm_data
        assert isinstance(omm_data["satellite_name"], str)
        assert isinstance(omm_data["satellite_id"], int)
        assert omm_data["satellite_name"] == "ISS"

        elements = omm_data["orbital_elements"]
        assert elements["OBJECT_NAME"] == "ISS"
        assert elements["NORAD_CAT_ID"] == omm_data["satellite_id"]
        for key in (
            "MEAN_MOTION",
            "ECCENTRICITY",
            "INCLINATION",
            "RA_OF_ASC_NODE",
            "ARG_OF_PERICENTER",
            "MEAN_ANOMALY",
            "BSTAR",
        ):
            assert key in elements

    # OMM data supports the zip (CSV) format rather than txt
    results = get_all_orbital_data_at_epoch_formatted(
        None, omm_repo, "omm", datetime.now(), "zip", 1, 100, "test", "1.0"
    )
    zip_file = zipfile.ZipFile(results)
    assert "omm_data.csv" in zip_file.namelist()
    csv_content = zip_file.read("omm_data.csv").decode("utf-8")
    # CCSDS OMM field names in the header + 2 data rows
    lines = [line for line in csv_content.splitlines() if line]
    assert len(lines) == 3
    assert "RA_OF_ASC_NODE" in lines[0]
    assert "NORAD_CAT_ID" in lines[0]


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
    results = get_adjacent_orbital_data_results(
        tle_repo, None, "tle", 25544, "catalog", epoch_jd, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 2
    assert results[0]["orbital_data"][0]["satellite_id"] == 25544
    assert results[0]["orbital_data"][1]["satellite_id"] == 25544

    results = get_adjacent_orbital_data_results(
        tle_repo, None, "tle", 1, "catalog", epoch_jd, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 0


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

    results = get_nearest_orbital_data_result(
        tle_repo, None, "tle", 25544, "catalog", epoch, "test", "1.0"
    )
    assert results[0]["orbital_data"][0]["tle_line1"] == tle_1.tle_line1
    assert results[0]["orbital_data"][0]["tle_line2"] == tle_1.tle_line2

    results = get_nearest_orbital_data_result(
        tle_repo, None, "tle", 1, "catalog", epoch, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 0


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

    results = get_orbital_data_around_epoch_results(
        tle_repo, None, "tle", 25544, "catalog", epoch, 2, 2, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 3

    results = get_orbital_data_around_epoch_results(
        tle_repo, None, "tle", 25544, "catalog", epoch, 1, 1, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 2

    results = get_orbital_data_around_epoch_results(
        tle_repo, None, "tle", 25544, "catalog", epoch, 1, 1, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 2

    results = get_orbital_data_around_epoch_results(
        tle_repo, None, "tle", 25544, "catalog", epoch, 0, 2, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 2


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
    assert len(results["data"]) == 1
    assert results["data"][0]["satellite_name"] == "ISS"
    assert results["data"][0]["satellite_id"] == 25544
    assert results["data"][0]["international_designator"] == "1998-067A"
    assert results["data"][0]["rcs_size"] == "LARGE"
    assert results["data"][0]["launch_date"] == "1998-11-20"
    assert results["data"][0]["decay_date"] is None
    assert results["data"][0]["object_type"] == "PAYLOAD"
    assert results["data"][0]["generation"] == "v1.0"
    assert results["data"][0]["constellation"] == "ISS"

    # Retrieval by catalog number
    results = get_satellite_data(sat_repo, 25544, "catalog", "test", "1.0")
    assert len(results["data"]) == 1
    assert results["data"][0]["satellite_name"] == "ISS"

    # Sat not found
    results = get_satellite_data(sat_repo, "NONEXISTENT", "name", "test", "1.0")
    assert len(results) == 0


def test_get_tle_data_repository_exceptions():
    # Test connection exception
    tle_repo = FakeTLERepository([], RuntimeError("Database connection failed"))
    with pytest.raises(RuntimeError, match="Database connection failed"):
        get_orbital_data(
            tle_repo, None, "tle", 25544, "catalog", None, None, "test", "1.0"
        )

    # Test name exception
    tle_repo = FakeTLERepository([], ValueError("Invalid satellite name"))
    with pytest.raises(ValueError, match="Invalid satellite name"):
        get_orbital_data(
            tle_repo, None, "tle", "ISS", "name", None, None, "test", "1.0"
        )


def test_get_tle_data_formatting_exception():
    tle_repo = FakeTLERepository([BrokenTLE("sat_name", sat_number=25544)])

    with pytest.raises(AttributeError, match="Broken satellite attribute: sat_name"):
        get_orbital_data(
            tle_repo, None, "tle", 25544, "catalog", None, None, "test", "1.0"
        )


def test_get_tles_around_epoch_repository_exception():
    tle_repo = FakeTLERepository([], ConnectionError("Connection timeout"))

    with pytest.raises(ConnectionError, match="Connection timeout"):
        get_orbital_data_around_epoch_results(
            tle_repo, None, "tle", 25544, "catalog", datetime.now(), 1, 1, "test", "1.0"
        )


def test_get_tles_around_epoch_formatting_exception():
    tle_repo = FakeTLERepository([BrokenTLE("tle_line1", sat_number=25544)])

    with pytest.raises(AttributeError, match="Broken attribute: tle_line1"):
        get_orbital_data_around_epoch_results(
            tle_repo, None, "tle", 25544, "catalog", datetime.now(), 1, 1, "test", "1.0"
        )


def test_get_nearest_tle_repository_exception():
    tle_repo = FakeTLERepository([], OSError("TLE not found"))

    with pytest.raises(OSError, match="TLE not found"):
        get_nearest_orbital_data_result(
            tle_repo, None, "tle", 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_nearest_tle_formatting_exception():
    tle_repo = FakeTLERepository([BrokenTLE("epoch", sat_number=25544)])

    with pytest.raises(AttributeError, match="Broken attribute: epoch"):
        get_nearest_orbital_data_result(
            tle_repo, None, "tle", 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_adjacent_tle_repository_exception():
    tle_repo = FakeTLERepository([], MemoryError("Out of memory"))

    with pytest.raises(MemoryError, match="Out of memory"):
        get_adjacent_orbital_data_results(
            tle_repo, None, "tle", 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_adjacent_tle_formatting_exceptions():
    # Test TXT exception
    tle_repo = FakeTLERepository([BrokenTLE("sat_name", sat_number=25544)])
    with pytest.raises(AttributeError, match="Broken satellite attribute: sat_name"):
        get_adjacent_orbital_data_results(
            tle_repo,
            None,
            "tle",
            25544,
            "catalog",
            datetime.now(),
            "test",
            "1.0",
            "txt",
        )

    # Test JSON exception
    tle_repo = FakeTLERepository([BrokenTLE("tle_line2", sat_number=25544)])
    with pytest.raises(AttributeError, match="Broken attribute: tle_line2"):
        get_adjacent_orbital_data_results(
            tle_repo,
            None,
            "tle",
            25544,
            "catalog",
            datetime.now(),
            "test",
            "1.0",
            "json",
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
    sat_repo = FakeSatelliteRepository(
        [BrokenSatellite("object_id", sat_number=25544, sat_name="ISS")]
    )

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
    sat_repo = FakeSatelliteRepository([BrokenSatellite("launch_date")])

    with pytest.raises(AttributeError, match="Broken satellite attribute: launch_date"):
        get_active_satellites(sat_repo, None, "test", "1.0")


def test_get_all_tles_at_epoch_repository_exception():
    tle_repo = FakeTLERepository([], TimeoutError("Query timeout"))

    with pytest.raises(TimeoutError, match="Query timeout"):
        get_all_orbital_data_at_epoch_formatted(
            tle_repo, None, "tle", datetime.now(), "json", 1, 100, "test", "1.0"
        )


def test_get_all_tles_at_epoch_formatting_exceptions():
    # Test TXT exception
    tle_repo = FakeTLERepository([BrokenTLE("tle_line1")])
    with pytest.raises(AttributeError, match="Broken attribute: tle_line1"):
        get_all_orbital_data_at_epoch_formatted(
            tle_repo, None, "tle", datetime.now(), "txt", 1, 100, "test", "1.0"
        )

    # Test JSON exception
    tle_repo = FakeTLERepository([BrokenTLE("sat_number")])
    with pytest.raises(AttributeError, match="Broken satellite attribute: sat_number"):
        get_all_orbital_data_at_epoch_formatted(
            tle_repo, None, "tle", datetime.now(), "json", 1, 100, "test", "1.0"
        )


def test_get_all_omms_at_epoch_repository_exception():
    omm_repo = FakeOrbitalElementsRepository([], TimeoutError("Query timeout"))

    with pytest.raises(TimeoutError, match="Query timeout"):
        get_all_orbital_data_at_epoch_formatted(
            None, omm_repo, "omm", datetime.now(), "json", 1, 100, "test", "1.0"
        )


def test_get_all_omms_at_epoch_formatting_exceptions():
    # Test element attribute exception
    omm_repo = FakeOrbitalElementsRepository([BrokenOMM("mean_motion")])
    with pytest.raises(AttributeError, match="Broken attribute: mean_motion"):
        get_all_orbital_data_at_epoch_formatted(
            None, omm_repo, "omm", datetime.now(), "json", 1, 100, "test", "1.0"
        )

    # Test satellite attribute exception
    omm_repo = FakeOrbitalElementsRepository([BrokenOMM("sat_number")])
    with pytest.raises(AttributeError, match="Broken satellite attribute: sat_number"):
        get_all_orbital_data_at_epoch_formatted(
            None, omm_repo, "omm", datetime.now(), "json", 1, 100, "test", "1.0"
        )


def test_satellite_name_id_repository_exceptions():
    sat_repo = FakeSatelliteRepository([], PermissionError("Access denied"))
    with pytest.raises(PermissionError, match="Access denied"):
        get_ids_for_satellite_name(sat_repo, "ISS", "test", "1.0")

    sat_repo = FakeSatelliteRepository([], LookupError("ID not found"))
    with pytest.raises(LookupError, match="ID not found"):
        get_names_for_satellite_id(sat_repo, 25544, "test", "1.0")


def test_get_omm_data():
    satellite = SatelliteFactory(sat_name="ISS")
    omm_1 = OrbitalElementsFactory(satellite=satellite)
    omm_2 = OrbitalElementsFactory(satellite=satellite)
    omm_repo = FakeOrbitalElementsRepository([omm_1, omm_2])

    results = get_orbital_data(
        None, omm_repo, "omm", "ISS", "name", None, None, "test", "1.0"
    )
    assert results["count"] == 2
    assert results["data"][0]["satellite_name"] == "ISS"
    assert results["data"][1]["satellite_name"] == "ISS"
    assert results["data"][0]["satellite_id"] == satellite.sat_number
    # OMM records nest the CCSDS elements rather than TLE lines
    for record in results["data"]:
        assert record["orbital_elements"]["OBJECT_NAME"] == "ISS"
        assert record["orbital_elements"]["NORAD_CAT_ID"] == satellite.sat_number
    epochs = {r["epoch"] for r in results["data"]}
    assert format_date(omm_1.epoch) in epochs
    assert format_date(omm_2.epoch) in epochs

    # No match by name
    results = get_orbital_data(
        None, omm_repo, "omm", "not_found", "name", None, None, "test", "1.0"
    )
    assert results["count"] == 0

    # Match by catalog number
    results = get_orbital_data(
        None,
        omm_repo,
        "omm",
        satellite.sat_number,
        "catalog",
        None,
        None,
        "test",
        "1.0",
    )
    assert results["count"] == 2

    # Date range filtering
    omm_1.epoch = datetime(2021, 1, 1)
    omm_2.epoch = datetime(2022, 1, 2)
    results = get_orbital_data(
        None,
        omm_repo,
        "omm",
        "ISS",
        "name",
        datetime(2020, 1, 1),
        datetime(2021, 1, 2),
        "test",
        "1.0",
    )
    assert results["count"] == 1


def test_get_omm_data_invalid_format():
    omm_repo = FakeOrbitalElementsRepository([])
    with pytest.raises(ValueError, match="Invalid format: xml"):
        get_orbital_data(
            None, omm_repo, "xml", "ISS", "name", None, None, "test", "1.0"
        )


def test_get_omm_data_repository_exception():
    omm_repo = FakeOrbitalElementsRepository([], RuntimeError("Database error"))
    with pytest.raises(RuntimeError, match="Database error"):
        get_orbital_data(
            None, omm_repo, "omm", 25544, "catalog", None, None, "test", "1.0"
        )


def test_get_omm_data_formatting_exception():
    omm_repo = FakeOrbitalElementsRepository(
        [BrokenOMM("mean_motion", sat_number=25544)]
    )
    with pytest.raises(AttributeError, match="Broken attribute: mean_motion"):
        get_orbital_data(
            None, omm_repo, "omm", 25544, "catalog", None, None, "test", "1.0"
        )


def test_get_nearest_omm():
    epoch = datetime.now()
    omm_1 = OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch - timedelta(days=1)
    )
    omm_2 = OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch + timedelta(days=3)
    )
    omm_repo = FakeOrbitalElementsRepository([omm_1, omm_2])

    results = get_nearest_orbital_data_result(
        None, omm_repo, "omm", 25544, "catalog", epoch, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 1
    assert results[0]["orbital_data"][0]["orbital_elements"]["NORAD_CAT_ID"] == 25544

    results = get_nearest_orbital_data_result(
        None, omm_repo, "omm", 1, "catalog", epoch, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 0


def test_get_nearest_omm_invalid_format():
    omm_repo = FakeOrbitalElementsRepository([])
    with pytest.raises(ValueError, match="Invalid format: xml"):
        get_nearest_orbital_data_result(
            None, omm_repo, "xml", 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_nearest_omm_repository_exception():
    omm_repo = FakeOrbitalElementsRepository([], OSError("OMM not found"))
    with pytest.raises(OSError, match="OMM not found"):
        get_nearest_orbital_data_result(
            None, omm_repo, "omm", 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_nearest_omm_formatting_exception():
    omm_repo = FakeOrbitalElementsRepository(
        [BrokenOMM("eccentricity", sat_number=25544)]
    )
    with pytest.raises(AttributeError, match="Broken attribute: eccentricity"):
        get_nearest_orbital_data_result(
            None, omm_repo, "omm", 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_adjacent_omms():
    epoch = datetime.now()
    omm_1 = OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_number=25544),
        epoch=epoch - timedelta(days=1),
    )
    omm_2 = OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_number=25544),
        epoch=epoch + timedelta(days=1),
    )
    omm_repo = FakeOrbitalElementsRepository([omm_1, omm_2])
    epoch_jd = Time(epoch).jd

    results = get_adjacent_orbital_data_results(
        None, omm_repo, "omm", 25544, "catalog", epoch_jd, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 2
    assert results[0]["orbital_data"][0]["satellite_id"] == 25544
    assert "orbital_elements" in results[0]["orbital_data"][0]

    results = get_adjacent_orbital_data_results(
        None, omm_repo, "omm", 1, "catalog", epoch_jd, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 0


def test_get_adjacent_omms_invalid_format():
    omm_repo = FakeOrbitalElementsRepository([])
    with pytest.raises(ValueError, match="Invalid data format: xml"):
        get_adjacent_orbital_data_results(
            None, omm_repo, "xml", 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_adjacent_omms_repository_exception():
    omm_repo = FakeOrbitalElementsRepository([], MemoryError("Out of memory"))
    with pytest.raises(MemoryError, match="Out of memory"):
        get_adjacent_orbital_data_results(
            None, omm_repo, "omm", 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_adjacent_omms_formatting_exception():
    omm_repo = FakeOrbitalElementsRepository(
        [BrokenOMM("inclination", sat_number=25544)]
    )
    with pytest.raises(AttributeError, match="Broken attribute: inclination"):
        get_adjacent_orbital_data_results(
            None, omm_repo, "omm", 25544, "catalog", datetime.now(), "test", "1.0"
        )


def test_get_adjacent_tles_txt_format():
    """The txt path is only valid for TLE data and returns a BytesIO stream."""
    tle_1 = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544),
        epoch=datetime.now() - timedelta(days=1),
    )
    tle_2 = TLEFactory(
        satellite=SatelliteFactory(sat_number=25544),
        epoch=datetime.now() + timedelta(days=1),
    )
    tle_repo = FakeTLERepository([tle_1, tle_2])

    results = get_adjacent_orbital_data_results(
        tle_repo, None, "tle", 25544, "catalog", datetime.now(), "test", "1.0", "txt"
    )
    text_content = results.getvalue().decode("utf-8")
    assert tle_1.tle_line1 in text_content
    assert tle_1.tle_line2 in text_content
    assert tle_2.tle_line1 in text_content
    assert tle_2.tle_line2 in text_content


def test_get_omms_around_epoch():
    epoch = datetime.now()
    omm_1 = OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch - timedelta(days=1)
    )
    omm_2 = OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch + timedelta(days=3)
    )
    omm_3 = OrbitalElementsFactory(
        satellite=SatelliteFactory(sat_number=25544), epoch=epoch + timedelta(days=5)
    )
    omm_repo = FakeOrbitalElementsRepository([omm_1, omm_2, omm_3])

    results = get_orbital_data_around_epoch_results(
        None, omm_repo, "omm", 25544, "catalog", epoch, 2, 2, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 3
    assert "orbital_elements" in results[0]["orbital_data"][0]

    results = get_orbital_data_around_epoch_results(
        None, omm_repo, "omm", 25544, "catalog", epoch, 1, 1, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 2


def test_get_omms_around_epoch_repository_exception():
    omm_repo = FakeOrbitalElementsRepository([], ConnectionError("Connection timeout"))
    with pytest.raises(ConnectionError, match="Connection timeout"):
        get_orbital_data_around_epoch_results(
            None, omm_repo, "omm", 25544, "catalog", datetime.now(), 1, 1, "test", "1.0"
        )


def test_get_omms_around_epoch_formatting_exception():
    omm_repo = FakeOrbitalElementsRepository(
        [BrokenOMM("mean_anomaly", sat_number=25544)]
    )
    with pytest.raises(AttributeError, match="Broken attribute: mean_anomaly"):
        get_orbital_data_around_epoch_results(
            None, omm_repo, "omm", 25544, "catalog", datetime.now(), 1, 1, "test", "1.0"
        )


def test_get_omms_around_epoch_invalid_format():
    omm_repo = FakeOrbitalElementsRepository([])
    with pytest.raises(ValueError, match="Invalid format: xml"):
        get_orbital_data_around_epoch_results(
            None, omm_repo, "xml", 25544, "catalog", datetime.now(), 1, 1, "test", "1.0"
        )


class _StubAroundEpochRepo:
    """Minimal repo returning a fixed value from get_orbital_data_around_epoch.

    Exercises the result-normalization branches (None and single-object) that
    the list-returning fakes never hit.
    """

    def __init__(self, result):
        self._result = result

    def get_orbital_data_around_epoch(
        self, id, id_type, epoch, count_before, count_after
    ):
        return self._result


def test_get_omms_around_epoch_none_result_normalized():
    repo = _StubAroundEpochRepo(None)
    results = get_orbital_data_around_epoch_results(
        None, repo, "omm", 25544, "catalog", datetime.now(), 1, 1, "test", "1.0"
    )
    assert results[0]["orbital_data"] == []


def test_get_omms_around_epoch_single_object_normalized():
    single = OrbitalElementsFactory(satellite=SatelliteFactory(sat_number=25544))
    repo = _StubAroundEpochRepo(single)
    results = get_orbital_data_around_epoch_results(
        None, repo, "omm", 25544, "catalog", datetime.now(), 1, 1, "test", "1.0"
    )
    assert len(results[0]["orbital_data"]) == 1
    assert results[0]["orbital_data"][0]["satellite_id"] == 25544


def test_get_all_orbital_data_at_epoch_formatted_invalid_format():
    omm_repo = FakeOrbitalElementsRepository([])
    with pytest.raises(ValueError, match="Invalid data format: xml"):
        get_all_orbital_data_at_epoch_formatted(
            None, omm_repo, "xml", datetime.now(), "json", 1, 100, "test", "1.0"
        )


def _ephemeris_repo_with_two_satellites():
    """Fake ephemeris repo holding one record each for two satellites."""
    e1 = InterpolableEphemerisFactory(
        satellite=SatelliteFactory(sat_number=11111, sat_name="STARLINK-A")
    )
    e2 = InterpolableEphemerisFactory(
        satellite=SatelliteFactory(sat_number=22222, sat_name="STARLINK-B")
    )
    return FakeEphemerisRepository([e1, e2]), e1, e2


def test_get_all_ephemeris_data_at_epoch_parquet():
    repo, e1, e2 = _ephemeris_repo_with_two_satellites()

    result = get_all_ephemeris_data_at_epoch_formatted(
        repo, datetime.now(timezone.utc), format="parquet"
    )

    assert isinstance(result, io.BytesIO)
    parquet_file = pq.ParquetFile(result)
    # One row per stored point across both records.
    assert parquet_file.metadata.num_rows == len(e1.points) + len(e2.points)
    # S3-aligned schema: exact columns, list<double> vectors, native timestamps.
    schema = parquet_file.schema_arrow
    assert schema.names == EPHEMERIS_PARQUET_COLUMNS
    assert str(schema.field("position").type) == "list<element: double>"
    assert str(schema.field("covariance").type) == "list<element: double>"
    assert "timestamp[us, tz=UTC]" in str(schema.field("timestamp").type)
    table = parquet_file.read()
    assert set(table.column("satellite_id").to_pylist()) == {11111, 22222}
    # Covariance stored flattened as 36 values (6x6, row-major).
    assert len(table.column("covariance").to_pylist()[0]) == 36


def test_get_all_ephemeris_data_at_epoch_zip():
    repo, e1, e2 = _ephemeris_repo_with_two_satellites()

    result = get_all_ephemeris_data_at_epoch_formatted(
        repo, datetime.now(timezone.utc), format="zip"
    )

    assert isinstance(result, io.BytesIO)
    with zipfile.ZipFile(result) as zip_file:
        # One CSV per satellite, named by satellite number.
        assert set(zip_file.namelist()) == {"11111.csv", "22222.csv"}
        lines = zip_file.read("11111.csv").decode().splitlines()
    # Flattened CSV header plus one row per point.
    assert lines[0].split(",") == EPHEMERIS_CSV_COLUMNS
    assert len(lines) == len(e1.points) + 1


def test_get_all_ephemeris_data_at_epoch_empty():
    repo = FakeEphemerisRepository([])

    result = get_all_ephemeris_data_at_epoch_formatted(
        repo, datetime.now(timezone.utc), format="parquet"
    )

    parquet_file = pq.ParquetFile(result)
    assert parquet_file.metadata.num_rows == 0
    assert parquet_file.schema_arrow.names == EPHEMERIS_PARQUET_COLUMNS


def test_get_ephemeris_data_for_satellite_at_epoch_parquet():
    repo, e1, _ = _ephemeris_repo_with_two_satellites()

    result = get_ephemeris_data_for_satellite_at_epoch_formatted(
        repo, "11111", "catalog", datetime.now(timezone.utc), format="parquet"
    )

    parquet_file = pq.ParquetFile(result)
    # Only the requested satellite's points, nothing from the other record.
    assert parquet_file.metadata.num_rows == len(e1.points)
    table = parquet_file.read()
    assert set(table.column("satellite_id").to_pylist()) == {11111}


def test_get_ephemeris_data_for_satellite_at_epoch_by_name():
    repo, e1, _ = _ephemeris_repo_with_two_satellites()

    result = get_ephemeris_data_for_satellite_at_epoch_formatted(
        repo, "STARLINK-A", "name", datetime.now(timezone.utc), format="parquet"
    )

    table = pq.ParquetFile(result).read()
    assert table.num_rows == len(e1.points)
    assert set(table.column("satellite_id").to_pylist()) == {11111}


def test_get_ephemeris_data_for_satellite_at_epoch_zip():
    repo, e1, _ = _ephemeris_repo_with_two_satellites()

    result = get_ephemeris_data_for_satellite_at_epoch_formatted(
        repo, "11111", "catalog", datetime.now(timezone.utc), format="zip"
    )

    with zipfile.ZipFile(result) as zip_file:
        assert zip_file.namelist() == ["11111.csv"]
        lines = zip_file.read("11111.csv").decode().splitlines()
    assert lines[0].split(",") == EPHEMERIS_CSV_COLUMNS
    assert len(lines) == len(e1.points) + 1


def test_get_ephemeris_data_for_satellite_at_epoch_not_found():
    repo, _, _ = _ephemeris_repo_with_two_satellites()

    # A satellite with no record -> empty file, not an error.
    result = get_ephemeris_data_for_satellite_at_epoch_formatted(
        repo, "99999", "catalog", datetime.now(timezone.utc), format="parquet"
    )

    parquet_file = pq.ParquetFile(result)
    assert parquet_file.metadata.num_rows == 0
    assert parquet_file.schema_arrow.names == EPHEMERIS_PARQUET_COLUMNS
