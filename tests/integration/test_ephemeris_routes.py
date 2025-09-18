# ruff: noqa: E501, S101, F841
from datetime import datetime, timedelta, timezone

from astropy.time import TimeDelta
from tests.factories.satellite_factory import (
    SatelliteDesignationFactory,
    SatelliteFactory,
)
from tests.factories.tle_factory import TLEFactory

from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.common import error_messages


def test_get_ephemeris_by_name(client, session, services_available):
    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_name="ISS", valid_from=datetime(2020, 5, 20)
            )
        ]
    )
    tle = TLEFactory(satellite=satellite, epoch=datetime(2020, 5, 30))
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    response = client.get(
        "/ephemeris/name/?name=ISS&latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 200


def test_get_ephemeris_by_name_jd_step(client, session, services_available):
    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_name="ISS", valid_from=datetime(2020, 5, 20)
            )
        ]
    )
    tle = TLEFactory(satellite=satellite, epoch=datetime(2020, 5, 30))
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()  # Commit to ensure data is saved

    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS&latitude=0&longitude=0&elevation=0"
        "&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 200


def test_get_ephemeris_by_catalog_number(client, session, services_available):
    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_number="25544", valid_from=datetime(2020, 5, 20)
            )
        ]
    )
    tle = TLEFactory(satellite=satellite, epoch=datetime(2020, 5, 30))
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 200


def test_get_ephemeris_by_catalog_number_jdstep(client, session, services_available):
    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_number="25544", valid_from=datetime(2020, 5, 20)
            )
        ]
    )
    tle = TLEFactory(satellite=satellite, epoch=datetime(2020, 5, 30))
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 200


def test_get_ephemeris_no_tle(client, services_available):
    response = client.get(
        "/ephemeris/name/?name=ISS&latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 500
    assert "No TLE found" in response.text

    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 500
    assert "No TLE found" in response.text

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 500
    assert "No TLE found" in response.text

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 500
    assert "No TLE found" in response.text


def test_get_ephemeris_data_from_tle(client, services_available):
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        f"/ephemeris/tle/?elevation=150&latitude=32&longitude=-110\
            &julian_date=2459000.5&tle={tle}"
    )
    assert response.status_code == 200


def test_get_ephemeris_data_from_tle_jdstep(client, services_available):
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        f"/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&startjd=2459000.5&stopjd=2459001.5&stepjd=.5&tle={tle}"
    )
    assert response.status_code == 200


def test_get_ephemeris_missing_parameter(client):
    # Missing 'latitude' parameter
    response = client.get(
        "/ephemeris/name/?name=ISS&longitude=0&elevation=0&julian_date=2459000.5"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Missing parameter" in response.text

    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Missing parameter" in response.text

    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&longitude=0&elevation=0&julian_date=2459000.5"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Missing parameter" in response.text

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Missing parameter" in response.text

    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        f"/ephemeris/tle/?elevation=150&longitude=-110&julian_date=2459000.5&tle={tle}"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Missing parameter" in response.text

    response = client.get(
        f"/ephemeris/tle-jdstep/?elevation=150&longitude=-110\
            &startjd=2460193.1&startjd=2459000.5&stopjd=2459001.5&stepjd=.5&tle={tle}"
    )
    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Missing parameter" in response.text


def test_get_ephemeris_by_tle_incorrect_format(client):
    tle = "tle"
    response = client.get(
        f"/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&startjd=2459000.5&stopjd=2459001.5&stepjd=.5&tle={tle}"
    )
    assert response.status_code == 500
    assert "Invalid TLE format" in response.text


def test_get_ephemeris_tle_date_out_of_range(
    client, session, test_time, services_available
):
    # Use a fixed Julian date as the base time to avoid any timezone issues
    base_jd = test_time
    base_datetime = base_jd.to_datetime(timezone=timezone.utc)

    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_name="TEST_ISS_DATE_RANGE",
                valid_from=base_datetime - timedelta(days=30),
            )
        ]
    )
    tle = TLEFactory(satellite=satellite, epoch=base_datetime)
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    # Test past date more than 30 days before TLE epoch
    past_jd = base_jd - TimeDelta(31, format="jd")
    response = client.get(
        f"/ephemeris/name/?name=TEST_ISS_DATE_RANGE&latitude=0&longitude=0&elevation=0&julian_date={past_jd.jd}"
    )
    assert response.status_code == 500
    assert error_messages.TLE_DATE_OUT_OF_RANGE in response.text

    # Test future date more than 30 days after TLE epoch
    future_jd = base_jd + TimeDelta(31, format="jd")
    response = client.get(
        f"/ephemeris/name/?name=TEST_ISS_DATE_RANGE&latitude=0&longitude=0&elevation=0&julian_date={future_jd.jd}"
    )
    assert response.status_code == 500
    assert error_messages.TLE_DATE_OUT_OF_RANGE in response.text


def test_get_ephemeris_tle_date_in_range(client, session, test_time):
    # Use a fixed Julian date as the base time to avoid any timezone issues
    base_jd = test_time
    base_datetime = base_jd.to_datetime(timezone=timezone.utc)

    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_name="TEST_ISS_DATE_RANGE",
                valid_from=base_datetime - timedelta(days=30),
            )
        ]
    )
    tle = TLEFactory(satellite=satellite, epoch=base_datetime)
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    # Test valid date within 30 days after TLE epoch
    valid_future_jd = base_jd + TimeDelta(29, format="jd")
    response = client.get(
        f"/ephemeris/name/?name=TEST_ISS_DATE_RANGE&latitude=0&longitude=0&elevation=0&julian_date={valid_future_jd.jd}"
    )
    assert response.status_code == 200

    # Test valid date within 30 days before TLE epoch
    valid_past_jd = base_jd - TimeDelta(29, format="jd")
    response = client.get(
        f"/ephemeris/name/?name=TEST_ISS_DATE_RANGE&latitude=0&longitude=0&elevation=0&julian_date={valid_past_jd.jd}"
    )
    assert response.status_code == 200


def test_get_ephemeris_no_designation_found(client, session, services_available):
    """Test that NO_DESIGNATION_FOUND error is returned when satellite has TLE but no valid designation at TLE epoch."""
    # Create a satellite with a designation that is valid after the TLE epoch
    base_datetime = datetime(2020, 5, 30, tzinfo=timezone.utc)

    satellite = SatelliteFactory(
        designations=[
            SatelliteDesignationFactory(
                sat_name="NO_DESIGNATION_SAT",
                valid_from=base_datetime + timedelta(days=10),
            )
        ]
    )
    tle = TLEFactory(satellite=satellite, epoch=base_datetime)
    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    response = client.get(
        "/ephemeris/name/?name=NO_DESIGNATION_SAT&latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 500
    assert error_messages.NO_DESIGNATION_FOUND in response.text
