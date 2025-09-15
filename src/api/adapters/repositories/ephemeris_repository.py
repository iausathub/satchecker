import abc
import logging
import pickle
from datetime import datetime
from typing import Optional

import numpy as np
from sqlalchemy import DateTime, bindparam, desc, func

from api.adapters.database_orm import (
    EphemerisPointDb,
    InterpolableEphemerisDb,
    InterpolatedSplineDb,
    SatelliteDb,
)
from api.domain.models.interpolable_ephemeris import (
    EphemerisPoint,
    InterpolableEphemeris,
)
from api.domain.models.interpolator_splines import InterpolatorSplines
from api.domain.models.satellite import Satellite
from api.utils.time_utils import ensure_datetime

logger = logging.getLogger(__name__)


class AbstractEphemerisRepository(abc.ABC):
    def __init__(self):
        self.seen = set()
        self.interpolator_splines_seen = set()

    def add(self, ephemeris: InterpolableEphemeris):
        self._add(ephemeris)
        self.seen.add(ephemeris)

    def get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: Optional[str] = None
    ) -> Optional[InterpolableEphemeris]:
        ephemeris = self._get_closest_by_satellite_number(
            satellite_number, epoch, data_source
        )
        if ephemeris:
            self.seen.add(ephemeris)
        return ephemeris

    def get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: Optional[str] = None
    ) -> Optional[InterpolableEphemeris]:
        ephemeris = self._get_closest_by_satellite_name(
            satellite_name, epoch, data_source
        )
        if ephemeris:
            self.seen.add(ephemeris)
        return ephemeris

    def get_latest_by_satellite_number(
        self, satellite_number: str, data_source: Optional[str] = None
    ) -> Optional[InterpolableEphemeris]:
        ephemeris = self._get_latest_by_satellite_number(satellite_number, data_source)
        if ephemeris:
            self.seen.add(ephemeris)
        return ephemeris

    def get_latest_by_satellite_name(
        self, satellite_name: str, data_source: Optional[str] = None
    ) -> Optional[InterpolableEphemeris]:
        ephemeris = self._get_latest_by_satellite_name(satellite_name, data_source)
        if ephemeris:
            self.seen.add(ephemeris)
        return ephemeris

    def get_satellites_with_ephemeris(
        self, start_time: datetime, end_time: datetime
    ) -> list[Satellite]:
        return self._get_satellites_with_ephemeris(start_time, end_time)

    def add_interpolator_splines(self, interpolator_splines: InterpolatorSplines):
        self._add_interpolator_splines(interpolator_splines)
        self.interpolator_splines_seen.add(interpolator_splines)

    def get_interpolator_splines(
        self, ephemeris_id: int
    ) -> Optional[InterpolatorSplines]:
        return self._get_interpolator_splines(ephemeris_id)

    def get_all_interpolator_splines_at_epoch(
        self, epoch_date: datetime
    ) -> list[InterpolatorSplines]:
        return self._get_all_interpolator_splines_at_epoch(epoch_date)

    @abc.abstractmethod
    def _add(self, ephemeris: InterpolableEphemeris):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_closest_by_satellite_number(
        self,
        satellite_number: str,
        data_timestamp: datetime,
        data_source: Optional[str] = None,
    ) -> Optional[InterpolableEphemeris]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_closest_by_satellite_name(
        self,
        satellite_name: str,
        data_timestamp: datetime,
        data_source: Optional[str] = None,
    ) -> Optional[InterpolableEphemeris]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_latest_by_satellite_number(
        self, satellite_number: str, data_source: Optional[str] = None
    ) -> Optional[InterpolableEphemeris]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_latest_by_satellite_name(
        self, satellite_name: str, data_source: Optional[str] = None
    ) -> Optional[InterpolableEphemeris]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_satellites_with_ephemeris(
        self, start_time: datetime, end_time: datetime
    ) -> list[Satellite]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add_interpolator_splines(self, interpolator_splines: InterpolatorSplines):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_interpolator_splines(
        self, ephemeris_id: int
    ) -> Optional[InterpolatorSplines]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_interpolator_splines_at_epoch(
        self, epoch_date: datetime
    ) -> list[InterpolatorSplines]:
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
                    timestamp=ensure_datetime(point.timestamp),
                    position=np.array(point.position),
                    velocity=np.array(point.velocity),
                    covariance=np.array(point.covariance).reshape(6, 6),
                )
            )

        return InterpolableEphemeris(
            id=orm_ephemeris.id,
            satellite=int(orm_ephemeris.satellite),
            date_collected=ensure_datetime(orm_ephemeris.date_collected),
            generated_at=ensure_datetime(orm_ephemeris.generated_at),
            data_source=str(orm_ephemeris.data_source),
            file_reference=(
                str(orm_ephemeris.file_reference)
                if orm_ephemeris.file_reference is not None
                else None
            ),
            frame=str(orm_ephemeris.frame),
            points=points,
            ephemeris_start=ensure_datetime(orm_ephemeris.ephemeris_start),
            ephemeris_stop=ensure_datetime(orm_ephemeris.ephemeris_stop),
        )

    def _add_interpolator_splines(self, interpolator_splines: InterpolatorSplines):
        try:
            # Check if interpolator splines already exist for this satellite
            # and time range
            existing = (
                self.session.query(InterpolatedSplineDb)
                .filter(
                    InterpolatedSplineDb.satellite == interpolator_splines.sat_id,
                    InterpolatedSplineDb.time_range_start
                    == interpolator_splines.time_range_start,
                    InterpolatedSplineDb.time_range_end
                    == interpolator_splines.time_range_end,
                )
                .first()
            )

            if existing:
                # Skip if record already exists
                logger.info(
                    f"Skipping...existing interpolator splines for ephemeris "
                    f"{interpolator_splines.ephemeris_id}"
                )
                return
            else:
                # Insert new record
                orm_interpolator_splines = self._to_orm_interpolator_splines(
                    interpolator_splines
                )
                self.session.add(orm_interpolator_splines)
                logger.info(
                    f"Added new interpolator splines for ephemeris "
                    f"{interpolator_splines.ephemeris_id}"
                )
                self.session.commit()
        except Exception as e:
            logger.error(f"Database error in _add_interpolator_splines: {e}")
            self.session.rollback()
            raise

    def _to_orm_interpolator_splines(
        self, interpolator_splines: InterpolatorSplines
    ) -> InterpolatedSplineDb:
        return InterpolatedSplineDb(
            satellite=interpolator_splines.sat_id,
            ephemeris=interpolator_splines.ephemeris_id,
            time_range_start=interpolator_splines.time_range_start,
            time_range_end=interpolator_splines.time_range_end,
            created_at=interpolator_splines.generated_at,
            data_source=interpolator_splines.data_source,
            method=interpolator_splines.method,
            chunk_size=interpolator_splines.chunk_size,
            overlap=interpolator_splines.overlap,
            n_sigma_points=interpolator_splines.n_sigma_points,
            interpolator_data=interpolator_splines.serialize_for_storage(),
        )

    @staticmethod
    def _to_domain_interpolator_splines(
        orm_interpolator_splines: InterpolatedSplineDb,
    ) -> InterpolatorSplines:
        # Safe to use pickle.loads here as data comes from our own database
        interpolated_splines = pickle.loads(  # noqa: S301
            orm_interpolator_splines.interpolator_data
        )
        return InterpolatorSplines(
            sat_id=orm_interpolator_splines.satellite,
            ephemeris_id=orm_interpolator_splines.ephemeris,
            time_range_start=orm_interpolator_splines.time_range_start,
            time_range_end=orm_interpolator_splines.time_range_end,
            generated_at=orm_interpolator_splines.created_at,
            data_source=orm_interpolator_splines.data_source,
            interpolated_splines=interpolated_splines,
            method=orm_interpolator_splines.method,
            chunk_size=orm_interpolator_splines.chunk_size,
            overlap=orm_interpolator_splines.overlap,
            n_sigma_points=orm_interpolator_splines.n_sigma_points,
        )

    def _get_interpolator_splines(
        self, ephemeris_id: int
    ) -> Optional[InterpolatorSplines]:
        orm_interpolator_splines = (
            self.session.query(InterpolatedSplineDb)
            .filter(InterpolatedSplineDb.ephemeris == ephemeris_id)
            .first()
        )
        if orm_interpolator_splines:
            return self._to_domain_interpolator_splines(orm_interpolator_splines)
        return None

    def _get_all_interpolator_splines_at_epoch(
        self, epoch_date: datetime
    ) -> list[InterpolatorSplines]:
        # Use DISTINCT ON to get the spline with the latest time_range_start
        # per satellite that doesn't exceed epoch_date
        orm_interpolator_splines = (
            self.session.query(InterpolatedSplineDb)
            .filter(
                InterpolatedSplineDb.time_range_start <= epoch_date,
                InterpolatedSplineDb.time_range_end >= epoch_date,
            )
            .distinct(InterpolatedSplineDb.satellite)
            .order_by(
                InterpolatedSplineDb.satellite,
                desc(InterpolatedSplineDb.time_range_start),
            )
        )

        if orm_interpolator_splines:
            return [
                self._to_domain_interpolator_splines(row)
                for row in orm_interpolator_splines
            ]
        return []

    def _get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: Optional[str] = None
    ) -> Optional[InterpolableEphemeris]:
        # Ensure epoch is a datetime object with timezone info
        epoch = ensure_datetime(epoch)
        epoch_param = bindparam("epoch", epoch, type_=DateTime(timezone=True))

        # Find any ephemeris that covers the epoch, then get the most recent one
        query = (
            self.session.query(InterpolableEphemerisDb)
            .join(InterpolableEphemerisDb.satellite_ref)
            .filter(
                SatelliteDb.sat_number == satellite_number,
                InterpolableEphemerisDb.ephemeris_start <= epoch,
                InterpolableEphemerisDb.ephemeris_stop >= epoch,
            )
            .order_by(
                func.abs(
                    func.extract("epoch", InterpolableEphemerisDb.generated_at)
                    - func.extract("epoch", epoch_param)
                )
            )
        )

        if data_source:
            query = query.filter(InterpolableEphemerisDb.data_source == data_source)

        orm_ephemeris = query.first()

        if orm_ephemeris:
            return self._to_domain(orm_ephemeris)

        return None

    def _get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: Optional[str] = None
    ) -> Optional[InterpolableEphemeris]:
        epoch = ensure_datetime(epoch)
        epoch_param = bindparam("epoch", epoch, type_=DateTime(timezone=True))

        # First find the ephemeris entry with the closest generated_at time that
        # is before or equal to the requested epoch
        query = (
            self.session.query(InterpolableEphemerisDb)
            .join(InterpolableEphemerisDb.satellite_ref)
            .filter(
                SatelliteDb.sat_name == satellite_name,
                InterpolableEphemerisDb.generated_at <= epoch,
                InterpolableEphemerisDb.ephemeris_start <= epoch,
                InterpolableEphemerisDb.ephemeris_stop >= epoch,
            )
            .order_by(
                func.abs(
                    func.extract("epoch", InterpolableEphemerisDb.generated_at)
                    - func.extract("epoch", epoch_param)
                )
            )
        )

        if data_source:
            query = query.filter(InterpolableEphemerisDb.data_source == data_source)

        orm_ephemeris = query.first()

        if orm_ephemeris:
            return self._to_domain(orm_ephemeris)

        return None

    def _get_latest_by_satellite_number(
        self, satellite_number: str, data_source: Optional[str] = None
    ) -> Optional[InterpolableEphemeris]:
        logger.error(f"Satellite number: {satellite_number}")
        logger.error(f"Data source: {data_source}")
        query = (
            self.session.query(InterpolableEphemerisDb)
            .join(InterpolableEphemerisDb.satellite_ref)
            .filter(SatelliteDb.sat_number == satellite_number)
        )
        logger.error(f"Query: {query}")
        logger.error(f"Data source: {data_source}")

        if data_source:
            query = query.filter(InterpolableEphemerisDb.data_source == data_source)

        orm_ephemeris = query.order_by(
            desc(InterpolableEphemerisDb.generated_at)
        ).first()

        logger.info(f"ORM ephemeris: {orm_ephemeris}")
        if orm_ephemeris:
            return self._to_domain(orm_ephemeris)
        return None

    def _get_latest_by_satellite_name(
        self, satellite_name: str, data_source: Optional[str] = None
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

    def _get_satellites_with_ephemeris(
        self, start_time: datetime, end_time: datetime
    ) -> list[Satellite]:
        try:
            # Ensure epoch is a datetime object with timezone info
            start_time = ensure_datetime(start_time)
            end_time = ensure_datetime(end_time)

            # Get satellites that have ephemeris data valid for the epoch
            # (epoch must be within the ephemeris time range and generated
            # at or before epoch)
            query = (
                self.session.query(SatelliteDb.sat_number)
                .join(
                    InterpolableEphemerisDb,
                    SatelliteDb.id == InterpolableEphemerisDb.satellite,
                )
                .filter(
                    InterpolableEphemerisDb.generated_at <= start_time,
                    InterpolableEphemerisDb.ephemeris_start <= start_time,
                    InterpolableEphemerisDb.ephemeris_stop >= end_time,
                )
                .distinct()
            )

            # Extract satellite numbers from the query results
            satellite_numbers = [row[0] for row in query.all()]

            return satellite_numbers
        except Exception as e:
            logger.error(f"Error getting satellites with ephemeris: {e}")
            return []
