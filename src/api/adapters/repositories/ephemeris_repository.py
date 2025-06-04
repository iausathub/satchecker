import abc
import logging
from datetime import datetime
from typing import Optional

import numpy as np
from sqlalchemy import desc

from api.adapters.database_orm import (
    EphemerisPointDb,
    InterpolableEphemerisDb,
    SatelliteDb,
)
from api.domain.models.interpolable_ephemeris import (
    EphemerisPoint,
    InterpolableEphemeris,
)
from api.utils.time_utils import ensure_datetime

logger = logging.getLogger(__name__)


class AbstractEphemerisRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, ephemeris: InterpolableEphemeris):
        self._add(ephemeris)
        self.seen.add(ephemeris)

    def get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        ephemeris = self._get_closest_by_satellite_number(
            satellite_number, epoch, data_source
        )
        if ephemeris:
            self.seen.add(ephemeris)
        return ephemeris

    def get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        ephemeris = self._get_closest_by_satellite_name(
            satellite_name, epoch, data_source
        )
        if ephemeris:
            self.seen.add(ephemeris)
        return ephemeris

    def get_latest_by_satellite_number(
        self, satellite_number: str, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        ephemeris = self._get_latest_by_satellite_number(satellite_number, data_source)
        if ephemeris:
            self.seen.add(ephemeris)
        return ephemeris

    def get_latest_by_satellite_name(
        self, satellite_name: str, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        ephemeris = self._get_latest_by_satellite_name(satellite_name, data_source)
        if ephemeris:
            self.seen.add(ephemeris)
        return ephemeris

    @abc.abstractmethod
    def _add(self, ephemeris: InterpolableEphemeris):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_closest_by_satellite_number(
        self, satellite_number: str, data_timestamp: datetime, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_closest_by_satellite_name(
        self, satellite_name: str, data_timestamp: datetime, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_latest_by_satellite_number(
        self, satellite_number: str, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_latest_by_satellite_name(
        self, satellite_name: str, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        raise NotImplementedError


class SqlAlchemyEphemerisRepository(AbstractEphemerisRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, ephemeris: InterpolableEphemeris):
        orm_ephemeris = self._to_orm(ephemeris)
        self.session.add(orm_ephemeris)

    def _to_orm(self, ephemeris: InterpolableEphemeris) -> InterpolableEphemerisDb:
        # Create the main ephemeris record
        orm_ephemeris = InterpolableEphemerisDb(
            satellite=ephemeris.satellite,
            date_collected=ephemeris.date_collected,
            generated_at=ephemeris.generated_at,
            data_source=ephemeris.data_source,
            file_reference=ephemeris.file_reference,
            frame=ephemeris.frame,
            ephemeris_start=ephemeris.ephemeris_start,
            ephemeris_stop=ephemeris.ephemeris_stop,
        )

        # Create the point records
        for point in ephemeris.points:
            orm_point = EphemerisPointDb(
                timestamp=point.timestamp,
                position=point.position.tolist(),
                velocity=point.velocity.tolist(),
                covariance=point.covariance.tolist(),
            )
            orm_ephemeris.points.append(orm_point)

        return orm_ephemeris

    @staticmethod
    def _to_domain(orm_ephemeris: InterpolableEphemerisDb) -> InterpolableEphemeris:
        # Convert points from ORM to domain objects
        points = []
        for point in orm_ephemeris.points:
            points.append(
                EphemerisPoint(
                    timestamp=point.timestamp,
                    position=np.array(point.position),
                    velocity=np.array(point.velocity),
                    covariance=np.array(point.covariance).reshape(6, 6),
                )
            )

        return InterpolableEphemeris(
            satellite=orm_ephemeris.satellite,
            date_collected=orm_ephemeris.date_collected,
            generated_at=orm_ephemeris.generated_at,
            data_source=orm_ephemeris.data_source,
            file_reference=orm_ephemeris.file_reference,
            frame=orm_ephemeris.frame,
            points=points,
            ephemeris_start=orm_ephemeris.ephemeris_start,
            ephemeris_stop=orm_ephemeris.ephemeris_stop,
        )

    def _get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        # Ensure epoch is a datetime object with timezone info
        epoch = ensure_datetime(epoch)

        # First find the ephemeris entry with the closest generated_at time that is
        # before or equal to the requested epoch
        query = (
            self.session.query(InterpolableEphemerisDb)
            .join(InterpolableEphemerisDb.satellite_ref)
            .filter(
                SatelliteDb.sat_number == satellite_number,
                InterpolableEphemerisDb.generated_at <= epoch,
            )
            .order_by(desc(InterpolableEphemerisDb.generated_at))
        )

        if data_source:
            query = query.filter(InterpolableEphemerisDb.data_source == data_source)

        orm_ephemeris = query.first()

        if orm_ephemeris:
            return self._to_domain(orm_ephemeris)

        return None

    def _get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        epoch = ensure_datetime(epoch)

        # First find the ephemeris entry with the closest generated_at time that
        # is before or equal to the requested epoch
        query = (
            self.session.query(InterpolableEphemerisDb)
            .join(InterpolableEphemerisDb.satellite_ref)
            .filter(
                SatelliteDb.sat_name == satellite_name,
                InterpolableEphemerisDb.generated_at <= epoch,
            )
            .order_by(desc(InterpolableEphemerisDb.generated_at))
        )

        if data_source:
            query = query.filter(InterpolableEphemerisDb.data_source == data_source)

        orm_ephemeris = query.first()

        if orm_ephemeris:
            return self._to_domain(orm_ephemeris)

        return None

    def _get_latest_by_satellite_number(
        self, satellite_number: str, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        query = (
            self.session.query(InterpolableEphemerisDb)
            .join(InterpolableEphemerisDb.satellite_ref)
            .filter(SatelliteDb.sat_number == satellite_number)
        )

        if data_source:
            query = query.filter(InterpolableEphemerisDb.data_source == data_source)

        orm_ephemeris = query.order_by(
            desc(InterpolableEphemerisDb.generated_at)
        ).first()

        if orm_ephemeris:
            return self._to_domain(orm_ephemeris)
        return None

    def _get_latest_by_satellite_name(
        self, satellite_name: str, data_source: str = None
    ) -> Optional[InterpolableEphemeris]:
        query = (
            self.session.query(InterpolableEphemerisDb)
            .join(InterpolableEphemerisDb.satellite_ref)
            .filter(SatelliteDb.sat_name == satellite_name)
        )

        if data_source:
            query = query.filter(InterpolableEphemerisDb.data_source == data_source)

        orm_ephemeris = query.order_by(
            desc(InterpolableEphemerisDb.generated_at)
        ).first()

        if orm_ephemeris:
            return self._to_domain(orm_ephemeris)
        return None
