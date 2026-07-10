from collections.abc import Sequence
from datetime import datetime, timezone
from typing import Any

from api.adapters.repositories.orbital_elements_repository import (
    SqlAlchemyOrbitalElementsRepository,
)
from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.domain.models.orbital_data import OrbitalData
from api.domain.models.orbital_elements import OrbitalElements
from api.domain.models.tle import TLE

ORBITAL_ELEMENTS_CUTOFF = datetime(2026, 7, 8, tzinfo=timezone.utc)


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
