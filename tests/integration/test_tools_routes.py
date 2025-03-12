# ruff: noqa: E501, S101, F841
from datetime import datetime, timedelta

import pytest
from astropy.time import Time
from tests.conftest import cannot_connect_to_services
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.adapters.repositories import satellite_repository, tle_repository
from api.entrypoints.extensions import db


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tle_data(client, session):
    satellite = SatelliteFactory(sat_name="ISS")

    tle = TLEFactory(satellite=satellite)
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)

    session.commit()
    response = client.get("/tools/get-tle-data/?id=ISS&id_type=name")
    assert response.status_code == 200


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tle_data_no_match(client):
    response = client.get("/tools/get-tle-data/?id=ISS&id_type=name")

    assert response.status_code == 200
    assert response.json == []


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_names_from_norad_id(client):
    satellite = SatelliteFactory(sat_number="25544")
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/names-from-norad-id/?id=25544")
    assert response.status_code == 200
    assert response.json[0]["norad_id"] == "25544"


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_names_from_norad_id_no_match(client):
    response = client.get("/tools/names-from-norad-id/?id=25544")
    assert response.status_code == 200
    assert response.json == []


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_norad_ids_from_name(client):
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/norad-ids-from-name/?name=ISS")
    assert response.status_code == 200
    assert response.json[0]["name"] == "ISS"


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_norad_ids_from_name_no_match(client):
    response = client.get("/tools/norad-ids-from-name/?name=ISS")
    assert response.status_code == 200
    assert response.json == []


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_data(client):
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/get-satellite-data/?id=ISS&id_type=name")
    assert response.status_code == 200
    assert response.json[0]["satellite_name"] == "ISS"


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_satellite_data_no_match(client):
    response = client.get("/tools/get-satellite-data/?id=ISS&id_type=name")
    assert response.status_code == 200
    assert response.json == []


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tles_at_epoch(client, session):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    epoch_date = datetime.strptime("2024-10-21", "%Y-%m-%d")
    tle = TLEFactory(satellite=satellite, epoch=epoch_date)
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

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


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tles_at_epoch_pagination(client, session):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    epoch_date = datetime.strptime("2024-10-22", "%Y-%m-%d")
    tle = TLEFactory(satellite=satellite, epoch=epoch_date)
    print(tle.epoch)
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()
    epoch_date = 2460606
    response = client.get(f"/tools/tles-at-epoch/?epoch={epoch_date}&page=1&per_page=1")
    tles = response.json[0]["data"]
    assert response.status_code == 200
    assert len(response.json) == 1
    assert tles[0]["satellite_name"] == "ISS"


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tles_at_epoch_optional_epoch_date(client, session):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    # get current date for TLE epoch
    epoch_date = datetime.now()
    tle = TLEFactory(
        satellite=satellite,
        epoch=epoch_date,
    )
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()
    response = client.get("/tools/tles-at-epoch/")
    tles = response.json[0]["data"]
    assert response.status_code == 200
    assert len(response.json) > 0
    assert tles[0]["satellite_name"] == "ISS"


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tles_at_epoch_zipped(client, session):
    satellite = SatelliteFactory(
        sat_name="ISS", decay_date=None, has_current_sat_number=True
    )
    # get current date for TLE epoch
    epoch_date = datetime.now()
    tle = TLEFactory(
        satellite=satellite,
        epoch=epoch_date,
    )
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()
    response = client.get("/tools/tles-at-epoch/?format=zip")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/zip"
    assert (
        response.headers["Content-Disposition"] == "attachment; filename=tle_data.zip"
    )


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_adjacent_tles(client, session):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = datetime.now()
    tle = TLEFactory(satellite=satellite, epoch=epoch - timedelta(days=1))
    tle2 = TLEFactory(satellite=satellite, epoch=epoch + timedelta(days=1))
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    tle_repo.add(tle2)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-adjacent-tles/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 2


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_nearest_tle(client, session):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = datetime.now()
    tle = TLEFactory(satellite=satellite, epoch=epoch - timedelta(days=1))
    tle2 = TLEFactory(satellite=satellite, epoch=epoch + timedelta(days=1))
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    tle_repo.add(tle2)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-nearest-tle/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 1


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tles_around_epoch(client, session):
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = datetime.now()
    tle = TLEFactory(satellite=satellite, epoch=epoch - timedelta(days=1))
    tle2 = TLEFactory(satellite=satellite, epoch=epoch + timedelta(days=1))
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    tle_repo.add(tle2)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 2


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_active_satellites(client):
    satellite = SatelliteFactory(
        sat_name="ISS",
        has_current_sat_number=True,
        decay_date=None,
        object_type="PAYLOAD",
    )
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    db.session.commit()

    response = client.get("/tools/get-active-satellites/?object_type=payload")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["satellite_name"] == "ISS"

    response = client.get("/tools/get-active-satellites/?object_type=invalid")
    assert response.status_code == 400
