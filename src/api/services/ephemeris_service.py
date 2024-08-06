from astropy.coordinates import EarthLocation
from astropy.time import Time

from src.api.adapters.repositories.satellite_repository import (
    AbstractSatelliteRepository,
)
from src.api.adapters.repositories.tle_repository import AbstractTLERepository
from src.api.domain.models.tle import TLE


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
) -> list[dict]:
    return []


def generate_ephemeris_data_user(
    tle: TLE,
    location: EarthLocation,
    dates: list[Time],
    min_altitude: float,
    max_altitude: float,
) -> list[dict]:
    return []
