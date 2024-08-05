from api.adapters.repositories.satellite_repository import AbstractSatelliteRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository
from astropy.coordinates import EarthLocation
from astropy.time import Time


def generate_ephemeris_data(
    sat_repo: AbstractSatelliteRepository,
    tle_repo: AbstractTLERepository,
    identifier: str,
    identifier_type: str,
    location: EarthLocation,
    dates: list[Time],
    min_altitude: float,
    max_altitude: float,
    data_source: str = "",
    jd_step: bool = False,
) -> list[dict]:
    pass
