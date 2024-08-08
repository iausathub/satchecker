# ruff: noqa: E501, S101, F841
from src.api.adapters.repositories import satellite_repository
from tests.factories.satellite_factory import SatelliteFactory


class FakeSatelliteRepository(satellite_repository.AbstractSatelliteRepository):
    def __init__(self, satellites):
        self._satellites = set(satellites)

    def _add(self, satellite):
        self._satellites.add(satellite)

    def _get(self, reference):
        return next(b for b in self._satellites if b.reference == reference)

    def _get_norad_ids_from_satellite_name(self, name):
        # check all the satellites in self._satellites and return the sat_numbers from all with matching name
        return [sat.sat_number for sat in self._satellites if sat.sat_name == name]

    def _get_satellite_names_from_norad_id(self, id):
        # check all the satellites in self._satellites and return the sat_names from all with matching sat_number
        return [sat.sat_name for sat in self._satellites if sat.sat_number == id]


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_get_ephemeris_by_name(client):
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = FakeSatelliteRepository([satellite])

    response = client.get(
        "/ephemeris/name/?name=ISS&latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 200


def test_get_ephemeris_by_name_jd_step(client):
    satellite = SatelliteFactory(sat_name="ISS")
    sat_repo = FakeSatelliteRepository([satellite])

    response = client.get(
        "/ephemeris/name-jdstep/?name=ISS&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 200


def test_get_ephemeris_by_catalog_number(client):
    satellite = SatelliteFactory(sat_number="25544")
    sat_repo = FakeSatelliteRepository([satellite])

    response = client.get(
        "/ephemeris/catalog-number/?catalog=25544&latitude=0&longitude=0&elevation=0&julian_date=2459000.5"
    )
    assert response.status_code == 200


def test_get_ephemeris_by_catalog_number_jdstep(client):
    satellite = SatelliteFactory(sat_number="25544")
    sat_repo = FakeSatelliteRepository([satellite])

    response = client.get(
        "/ephemeris/catalog-number-jdstep/?catalog=25544&latitude=0&longitude=0&elevation=0&startjd=2459000.5&stopjd=2459001.5&stepjd=0.5"
    )
    assert response.status_code == 200


def test_get_ephemeris_data_from_tle(client):
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        f"/ephemeris/tle/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&julian_date=2459000.5&tle={tle}"
    )
    assert response.status_code == 200


def test_get_ephemeris_data_from_tle_jdstep(client):
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    response = client.get(
        f"/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&startjd=2459000.5&stopjd=2459001.5&stepjd=.5&tle={tle}"
    )
    assert response.status_code == 200


def test_get_ephemeris_by_name_missing_parameter(client):
    # Missing 'latitude' parameter
    response = client.get(
        "/ephemeris/name/?name=ISS&longitude=0&elevation=0&julian_date=2459000.5"
    )

    # Check that the correct error code was returned
    assert response.status_code == 400
    assert "Incorrect parameters" in response.text


def test_get_ephemeris_by_tle_incorrect_format(client):
    tle = "tle"
    response = client.get(
        f"/ephemeris/tle-jdstep/?elevation=150&latitude=32&longitude=-110\
            &startjd=2460193.1&startjd=2459000.5&stopjd=2459001.5&stepjd=.5&tle={tle}"
    )
    assert response.status_code == 500
    assert "Incorrect TLE format" in response.text
