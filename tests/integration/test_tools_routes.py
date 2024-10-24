# ruff: noqa: E501, S101, F841
from datetime import datetime

from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.adapters.repositories import satellite_repository, tle_repository
from api.entrypoints.extensions import db


def test_get_tle_data(client):
    satellite = SatelliteFactory(sat_name="ISS")
    tle = TLEFactory(satellite=satellite)
    tle_repo = tle_repository.SqlAlchemyTLERepository(db.session)
    tle_repo.add(tle)
    db.session.commit()

    response = client.get("/tools/get-tle-data/?id=ISS&id_type=name")

    assert response.status_code == 200
    assert "ISS" in response.json[0]["satellite_name"]


def test_get_tle_data_no_match(client):
    response = client.get("/tools/get-tle-data/?id=ISS&id_type=name")

    assert response.status_code == 200
    assert response.json == []


def test_get_names_from_norad_id(client):
    satellite = SatelliteFactory(sat_number="25544")
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/names-from-norad-id/?id=25544")
    assert response.status_code == 200
    assert response.json[0]["norad_id"] == "25544"


def test_get_names_from_norad_id_no_match(client):
    response = client.get("/tools/names-from-norad-id/?id=25544")
    assert response.status_code == 200
    assert response.json == []


def test_get_norad_ids_from_name(client):
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/norad-ids-from-name/?name=ISS")
    assert response.status_code == 200
    assert response.json[0]["name"] == "ISS"


def test_get_norad_ids_from_name_no_match(client):
    response = client.get("/tools/norad-ids-from-name/?name=ISS")
    assert response.status_code == 200
    assert response.json == []


def test_get_satellite_data(client):
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/get-satellite-data/?id=ISS&id_type=name")
    assert response.status_code == 200
    assert response.json[0]["satellite_name"] == "ISS"


def test_get_satellite_data_no_match(client):
    response = client.get("/tools/get-satellite-data/?id=ISS&id_type=name")
    assert response.status_code == 200
    assert response.json == []


def test_get_tles_at_epoch(client):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    epoch_date = datetime.strptime("2024-10-21", "%Y-%m-%d")
    tle = TLEFactory(satellite=satellite, epoch=epoch_date)
    tle_repo = tle_repository.SqlAlchemyTLERepository(db.session)
    tle_repo.add(tle)
    db.session.commit()

    epoch_date = 2460605
    response = client.get(f"/tools/tles-at-epoch/?epoch={epoch_date}")
    tles = response.json[0]["data"]

    assert response.status_code == 200
    assert len(response.json) > 0
    assert tles[0]["satellite_name"] == "ISS"

    # test that older TLEs ( > 1 week ) are not returned
    epoch_date = 2460505
    response = client.get(f"/tools/tles-at-epoch/?epoch={epoch_date}")
    tles = response.json[0]["data"]

    assert response.status_code == 200
    assert len(response.json[0]["data"]) == 0


def test_get_tles_at_epoch_pagination(client):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    epoch_date = datetime.strptime("2024-10-22", "%Y-%m-%d")
    tle = TLEFactory(satellite=satellite, epoch=epoch_date)
    print(tle.epoch)
    tle_repo = tle_repository.SqlAlchemyTLERepository(db.session)
    tle_repo.add(tle)
    db.session.commit()

    epoch_date = 2460606
    response = client.get(f"/tools/tles-at-epoch/?epoch={epoch_date}&page=1&per_page=1")
    tles = response.json[0]["data"]

    assert response.status_code == 200
    assert len(response.json) == 1
    assert tles[0]["satellite_name"] == "ISS"


def test_get_tles_at_epoch_optional_epoch_date(client):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    # get current date for TLE epoch
    epoch_date = datetime.now()
    tle = TLEFactory(
        satellite=satellite,
        epoch=epoch_date,
    )
    tle_repo = tle_repository.SqlAlchemyTLERepository(db.session)
    tle_repo.add(tle)
    db.session.commit()

    response = client.get("/tools/tles-at-epoch/")

    tles = response.json[0]["data"]

    assert response.status_code == 200
    assert len(response.json) > 0
    assert tles[0]["satellite_name"] == "ISS"
