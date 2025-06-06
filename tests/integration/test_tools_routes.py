# ruff: noqa: E501, S101, F841
import time
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
def test_get_adjacent_tles_nonexistent_satellite(client, session):
    """Test get_adjacent_tles with a satellite that doesn't exist."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use a satellite ID that doesn't exist in the database
    response = client.get(
        f"/tools/get-adjacent-tles/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )

    # Should return success but with empty tle_data
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 0


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_adjacent_tles_errors(client, session):
    """Test get_adjacent_tles with various error conditions."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use an invalid id_type
    response = client.get(
        f"/tools/get-adjacent-tles/?id=25544&id_type=invalid&epoch={epoch_jd}"
    )

    # Should return a bad request status
    assert response.status_code == 400
    assert "Error" in response.json["message"]

    # Missing id parameter
    response = client.get("/tools/get-adjacent-tles/?id_type=catalog&epoch=2460000.5")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Missing id_type parameter
    response = client.get("/tools/get-adjacent-tles/?id=25544&epoch=2460000.5")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Missing epoch parameter
    response = client.get("/tools/get-adjacent-tles/?id=25544&id_type=catalog")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Using a non-numeric value for epoch
    response = client.get(
        "/tools/get-adjacent-tles/?id=25544&id_type=catalog&epoch=10-01-2024"
    )
    assert response.status_code == 500
    assert "ValidationError" in response.json["error_type"]


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

    # Use a satellite ID that doesn't exist in the database
    response = client.get(
        f"/tools/get-nearest-tle/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )

    # Should return success but with empty tle_data
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 0


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_nearest_tle_nonexistent_satellite(client, session):
    """Test get_nearest_tle with a satellite that doesn't exist."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use a satellite ID that doesn't exist in the database
    response = client.get(
        f"/tools/get-nearest-tle/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )

    # Should return success but with empty tle_data
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 0


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_nearest_tle_errors(client, session):
    """Test get_nearest_tle with an invalid ID type."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use an invalid id_type
    response = client.get(
        f"/tools/get-nearest-tle/?id=25544&id_type=invalid&epoch={epoch_jd}"
    )

    # Should return a bad request status
    assert response.status_code == 400
    assert "Error" in response.json["message"]

    # Missing id parameter
    response = client.get("/tools/get-nearest-tle/?id_type=catalog&epoch=2460000.5")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Missing id_type parameter
    response = client.get("/tools/get-nearest-tle/?id=25544&epoch=2460000.5")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Missing epoch parameter
    response = client.get("/tools/get-nearest-tle/?id=25544&id_type=catalog")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Using a non-numeric value for epoch
    response = client.get(
        "/tools/get-nearest-tle/?id=25544&id_type=catalog&epoch=10-01-2024"
    )
    assert response.status_code == 500
    assert "ValidationError" in response.json["error_type"]


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_nearest_tle_name_id_type(client, session):
    """Test get_nearest_tle with id_type=name."""
    # Create a satellite with a specific name
    satellite = SatelliteFactory(
        sat_name="TEST_SAT", decay_date=None, has_current_sat_number=True
    )
    epoch = datetime.now()
    tle = TLEFactory(satellite=satellite, epoch=epoch)
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    epoch_jd = Time(epoch).jd
    response = client.get(
        f"/tools/get-nearest-tle/?id=TEST_SAT&id_type=name&epoch={epoch_jd}"
    )

    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 1
    assert response.json[0]["tle_data"][0]["satellite_name"] == "TEST_SAT"


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
def test_get_tles_around_epoch_nonexistent_satellite(client, session):
    """Test get_tles_around_epoch with a satellite that doesn't exist."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use a satellite ID that doesn't exist in the database
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=99999&id_type=catalog&epoch={epoch_jd}"
    )

    # Should return success but with empty tle_data
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 0


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tles_around_epoch_errors(client, session):
    """Test get_tles_around_epoch with various error conditions."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Use an invalid id_type
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=invalid&epoch={epoch_jd}"
    )

    # Should return a bad request status
    assert response.status_code == 400
    assert "Error" in response.json["message"]

    # Missing id parameter
    response = client.get(
        "/tools/get-tles-around-epoch/?id_type=catalog&epoch=2460000.5"
    )
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Missing id_type parameter
    response = client.get("/tools/get-tles-around-epoch/?id=25544&epoch=2460000.5")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Missing epoch parameter
    response = client.get("/tools/get-tles-around-epoch/?id=25544&id_type=catalog")
    assert response.status_code == 400
    assert "Missing parameter" in response.json["message"]

    # Using a non-numeric value for epoch
    response = client.get(
        "/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch=10-01-2024"
    )
    assert response.status_code == 500
    assert "ValidationError" in response.json["error_type"]


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_tles_around_epoch_custom_counts(client, session):
    """Test get_tles_around_epoch with custom count_before and count_after parameters."""
    satellite = SatelliteFactory(
        sat_number="25544", decay_date=None, has_current_sat_number=True
    )
    epoch = datetime.now()

    # Create 5 TLEs before and 5 TLEs after the epoch
    tles_before = []
    tles_after = []
    tle_repo = tle_repository.SqlAlchemyTLERepository(session)

    for i in range(1, 6):
        tle_before = TLEFactory(satellite=satellite, epoch=epoch - timedelta(days=i))
        tle_after = TLEFactory(satellite=satellite, epoch=epoch + timedelta(days=i))
        tles_before.append(tle_before)
        tles_after.append(tle_after)
        tle_repo.add(tle_before)
        tle_repo.add(tle_after)

    session.commit()

    epoch_jd = Time(epoch).jd

    # Test with default counts (2 before, 2 after)
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}"
    )
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 4

    # Test with custom counts (3 before, 1 after)
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}&count_before=3&count_after=1"
    )
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 4

    # Test with custom counts (0 before, 4 after)
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}&count_before=0&count_after=4"
    )
    assert response.status_code == 200
    assert len(response.json[0]["tle_data"]) == 4

    # Test with invalid counts
    response = client.get(
        f"/tools/get-tles-around-epoch/?id=25544&id_type=catalog&epoch={epoch_jd}&count_before=-1&count_after=-2"
    )
    assert response.status_code == 500
    assert "Error" in response.json["message"]


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


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_get_starlink_generations(client):
    satellite = SatelliteFactory(
        sat_name="starlink1",
        has_current_sat_number=True,
        launch_date=datetime(2019, 5, 10),
        generation="gen1",
    )
    satellite2 = SatelliteFactory(
        sat_name="starlink2",
        has_current_sat_number=True,
        launch_date=datetime(2019, 5, 20),
        generation="gen1",
    )
    sat_repo = satellite_repository.SqlAlchemySatelliteRepository(db.session)
    sat_repo.add(satellite)
    sat_repo.add(satellite2)
    db.session.commit()

    response = client.get("/tools/get-starlink-generations/")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["data"][0]["generation"] == "gen1"


@pytest.mark.skipif(
    cannot_connect_to_services(),
    reason="Services not available",
)
def test_rate_limiting(client, session):
    """Test rate limiting on a TLE endpoint."""
    epoch = datetime.now()
    epoch_jd = Time(epoch).jd

    # Create a valid request URL
    url = f"/tools/get-nearest-tle/?id=25544&id_type=catalog&epoch={epoch_jd}"

    num_requests = 110  # Slightly over the per-second limit of 100

    responses = []
    for _ in range(num_requests):
        responses.append(client.get(url))

    success_count = sum(1 for r in responses if r.status_code == 200)
    rate_limited_count = sum(1 for r in responses if r.status_code == 429)

    assert success_count > 0
    assert rate_limited_count > 0

    # The last request should be rate limited
    assert responses[-1].status_code == 429

    time.sleep(5)
    response = client.get(url)
    assert response.status_code == 200
