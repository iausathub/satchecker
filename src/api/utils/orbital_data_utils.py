from collections.abc import Sequence
from datetime import datetime, timezone
from typing import Any, cast

from sgp4 import exporter

from api.adapters.repositories.orbital_elements_repository import (
    SqlAlchemyOrbitalElementsRepository,
)
from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.domain.models.orbital_data import OrbitalData
from api.domain.models.orbital_elements import OrbitalElements
from api.domain.models.tle import TLE
from api.utils.skyfield_loader import load

ORBITAL_ELEMENTS_CUTOFF = datetime(2026, 7, 13, tzinfo=timezone.utc)

_timescale = None


def _get_timescale():
    # Built lazily when needed.
    global _timescale
    if _timescale is None:
        _timescale = load.timescale()
    return _timescale


def omm_to_tle_lines(orbital_elements: OrbitalElements) -> tuple[str, str]:
    """Convert OMM orbital elements to the equivalent TLE line pair.

    export_tle expects the sgp4 Satrec, which skyfield stores on
    EarthSatellite.model.

    Args:
        orbital_elements: The OMM record to convert.

    Returns:
        A ``(tle_line1, tle_line2)`` tuple.
    """
    satellite = orbital_elements.to_earth_satellite(_get_timescale())
    return cast("tuple[str, str]", exporter.export_tle(satellite.model))


def serialize_orbital_data(orbital_data: TLE | OrbitalElements) -> dict[str, Any]:
    if isinstance(orbital_data, TLE):
        return SqlAlchemyTLERepository.batch_serialize_tles([orbital_data])[0]
    return SqlAlchemyOrbitalElementsRepository.batch_serialize_orbital_elements(
        [orbital_data]
    )[0]


def deserialize_orbital_data(serialized_orbital_data: dict[str, Any]) -> OrbitalData:
    if "tle_line1" in serialized_orbital_data:
        return SqlAlchemyTLERepository.deserialize_tles([serialized_orbital_data])[0]
    return SqlAlchemyOrbitalElementsRepository.deserialize_orbital_elements(
        [serialized_orbital_data]
    )[0]


def deserialize_orbital_data_batch(
    serialized_batch: list[dict[str, Any]],
) -> Sequence[OrbitalData]:
    if not serialized_batch:
        return []
    if "tle_line1" in serialized_batch[0]:
        return SqlAlchemyTLERepository.deserialize_tles(serialized_batch)
    return SqlAlchemyOrbitalElementsRepository.deserialize_orbital_elements(
        serialized_batch
    )
