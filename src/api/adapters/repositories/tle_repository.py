import abc
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from sqlalchemy import DateTime, String, and_, bindparam, func, text
from sqlalchemy.orm.exc import NoResultFound

from api.adapters.database_orm import SatelliteDb, TLEDb
from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.domain.models.satellite import Satellite as Satellite
from api.domain.models.tle import TLE
from api.services.cache_service import RECENT_TLES_CACHE_KEY, get_cached_data
from api.utils.time_utils import ensure_datetime

# Set up logger
logger = logging.getLogger(__name__)


class AbstractTLERepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, tle: TLE):
        self._add(tle)
        self.seen.add(tle)

    def get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> Optional[TLE]:
        tle = self._get_closest_by_satellite_number(
            satellite_number, epoch, data_source
        )
        if tle:
            self.seen.add(tle)
        return tle

    def get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> Optional[TLE]:
        tle = self._get_closest_by_satellite_name(satellite_name, epoch, data_source)
        if tle:
            self.seen.add(tle)
        return tle

    def get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> list[TLE]:
        return self._get_all_for_date_range_by_satellite_number(
            satellite_number, start_date, end_date
        )

    def get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> list[TLE]:
        return self._get_all_for_date_range_by_satellite_name(
            satellite_name, start_date, end_date
        )

    def get_all_tles_at_epoch(
        self,
        epoch_date: datetime,
        page: int,
        per_page: int,
        format: str,
        constellation: Optional[str] = None,
        data_source_limit: Optional[str] = None,
    ) -> tuple[list[TLE], int, str]:
        return self._get_all_tles_at_epoch(
            epoch_date, page, per_page, format, constellation, data_source_limit
        )

    def get_nearest_tle(self, id: str, id_type: str, epoch: datetime) -> Optional[TLE]:
        return self._get_nearest_tle(id, id_type, epoch)

    def get_adjacent_tles(self, id: str, id_type: str, epoch: datetime) -> list[TLE]:
        return self._get_adjacent_tles(id, id_type, epoch)

    def get_tles_around_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
        count_before: int,
        count_after: int,
    ) -> list[TLE]:
        return self._get_tles_around_epoch(
            id, id_type, epoch, count_before, count_after
        )

    @abc.abstractmethod
    def _get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> Optional[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> Optional[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> list[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> list[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_tles_at_epoch(
        self,
        epoch_date: datetime,
        page: int,
        per_page: int,
        format: str,
        constellation: Optional[str] = None,
        data_source: Optional[str] = None,
    ) -> tuple[list[TLE], int, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_tles_around_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
        count_before: int,
        count_after: int,
    ) -> list[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_nearest_tle(self, id: str, id_type: str, epoch: datetime) -> Optional[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_adjacent_tles(self, id: str, id_type: str, epoch: datetime) -> list[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, satellite: TLE):
        raise NotImplementedError


class SqlAlchemyTLERepository(AbstractTLERepository):
    def __init__(self, session):
        super().__init__()
        self.session = session
        # Default cache TTL in seconds - can be overridden in tests
        self.cache_ttl = 10800  # 3 hours
        self.cache_enabled = True

    @staticmethod
    def _to_domain(orm_tle) -> Optional[TLE]:
        # Return None if orm_tle is None
        if orm_tle is None:
            return None

        # Return None or raise an exception if satellite is None
        if orm_tle.satellite is None:
            logger.warning(f"Found TLE with ID {orm_tle.id} without a satellite")
            return None

        # Only convert if we have a valid satellite
        satellite = SqlAlchemySatelliteRepository._to_domain(orm_tle.satellite)
        if satellite is None:
            logger.warning(f"Failed to convert satellite for TLE with ID {orm_tle.id}")
            return None

        return TLE(
            date_collected=orm_tle.date_collected,
            tle_line1=orm_tle.tle_line1,
            tle_line2=orm_tle.tle_line2,
            epoch=orm_tle.epoch,
            is_supplemental=orm_tle.is_supplemental,
            data_source=orm_tle.data_source,
            satellite=satellite,
        )

    @staticmethod
    def _to_orm(domain_tle) -> TLEDb:
        return TLEDb(
            date_collected=domain_tle.date_collected,
            tle_line1=domain_tle.tle_line1,
            tle_line2=domain_tle.tle_line2,
            epoch=domain_tle.epoch,
            is_supplemental=domain_tle.is_supplemental,
            data_source=domain_tle.data_source,
            satellite=SqlAlchemySatelliteRepository._to_orm(domain_tle.satellite),
        )

    @staticmethod
    def deserialize_cached_tles(serialized_tles: list[dict[str, Any]]) -> list[TLE]:
        """
        Convert serialized TLE dictionaries from the cache back into domain TLE objects.

        Args:
            serialized_tles: List of serialized TLE dictionaries from the cache

        Returns:
            List of TLE domain objects
        """
        tles = []

        for tle_dict in serialized_tles:
            try:
                # Extract satellite data and create Satellite domain object
                sat_data = tle_dict.get("satellite", {})

                # Parse decay_date if it exists
                decay_date_str = sat_data.get("decay_date")
                decay_date = None
                if decay_date_str:
                    try:
                        decay_date = datetime.fromisoformat(decay_date_str)
                    except ValueError:
                        logger.warning(f"Could not parse decay_date: {decay_date_str}")

                # Create the Satellite object
                satellite = Satellite(
                    sat_name=sat_data.get("sat_name", ""),
                    sat_number=sat_data.get("sat_number", ""),
                    decay_date=decay_date,
                    has_current_sat_number=sat_data.get("has_current_sat_number", True),
                    constellation=sat_data.get("constellation", ""),
                )

                # Parse datetime fields
                epoch = datetime.fromisoformat(tle_dict.get("epoch", ""))
                date_collected = datetime.fromisoformat(
                    tle_dict.get("date_collected", "")
                )

                # Create the TLE domain object
                tle = TLE(
                    satellite=satellite,
                    tle_line1=tle_dict.get("tle_line1", ""),
                    tle_line2=tle_dict.get("tle_line2", ""),
                    epoch=epoch,
                    date_collected=date_collected,
                    is_supplemental=tle_dict.get("is_supplemental", False),
                    data_source=tle_dict.get("data_source", ""),
                )

                tles.append(tle)
            except Exception as e:
                logger.error(f"Error deserializing TLEs: {e}")
                raise e

        return tles

    def _add(self, tle: TLE):
        orm_tle = self._to_orm(tle)

        try:
            existing_satellite = (
                self.session.query(SatelliteDb)
                .filter(
                    SatelliteDb.sat_number == tle.satellite.sat_number,
                    SatelliteDb.sat_name == tle.satellite.sat_name,
                )
                .one()
            )
            orm_tle.satellite = existing_satellite
        except NoResultFound:
            # Satellite does not exist, so it will be added with the TLE
            pass

        self.session.add(orm_tle)

    def _get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> Optional[TLE]:
        filter_conditions = [SatelliteDb.sat_number == satellite_number]
        if data_source != "any":
            filter_conditions.append(TLEDb.data_source == data_source)

        # Ensure epoch is a datetime object with timezone info
        epoch = ensure_datetime(epoch)
        epoch_param = bindparam("epoch", epoch, type_=DateTime(timezone=True))

        result = (
            self.session.query(TLEDb)
            .join(TLEDb.satellite)
            .filter(and_(*filter_conditions))
            .order_by(
                func.abs(
                    func.extract("epoch", TLEDb.epoch)
                    - func.extract("epoch", epoch_param)
                )
            )
            .first()
        )

        if result is None:
            return None

        return self._to_domain(result)

    def _get_closest_by_satellite_name(
        self,
        satellite_name: str,
        epoch: datetime,
        data_source: str,
    ) -> Optional[TLE]:
        filter_conditions = [SatelliteDb.sat_name == satellite_name]
        if data_source != "any":
            filter_conditions.append(TLEDb.data_source == data_source)

        # Ensure epoch is a datetime object with timezone info
        epoch = ensure_datetime(epoch)
        epoch_param = bindparam("epoch", epoch, type_=DateTime(timezone=True))

        result = (
            self.session.query(TLEDb)
            .join(TLEDb.satellite)
            .filter(and_(*filter_conditions))
            .order_by(
                func.abs(
                    func.extract("epoch", TLEDb.epoch)
                    - func.extract("epoch", epoch_param)
                )
            )
            .first()
        )

        if result is None:
            return None

        return self._to_domain(result)

    def _get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> list[TLE]:
        query = (
            self.session.query(TLEDb)
            .join(TLEDb.satellite)
            .filter(SatelliteDb.sat_number == satellite_number)
        )

        if start_date is not None:
            query = query.filter(TLEDb.epoch >= start_date)

        if end_date is not None:
            query = query.filter(TLEDb.epoch <= end_date)

        results = query.all()
        # Filter out any None values that may result from _to_domain
        return [
            tle
            for tle in (self._to_domain(result) for result in results)
            if tle is not None
        ]

    def _get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> list[TLE]:
        query = (
            self.session.query(TLEDb)
            .join(TLEDb.satellite)
            .filter(SatelliteDb.sat_name == satellite_name)
        )
        if start_date is not None:
            query = query.filter(TLEDb.epoch >= start_date)

        if end_date is not None:
            query = query.filter(TLEDb.epoch <= end_date)

        results = query.all()
        # Filter out any None values that may result from _to_domain
        return [
            tle
            for tle in (self._to_domain(result) for result in results)
            if tle is not None
        ]

    def _get_all_tles_at_epoch(
        self,
        epoch_date: datetime,
        page: int,
        per_page: int,
        format: str,
        constellation: Optional[str] = None,
        data_source_limit: Optional[str] = None,
    ) -> tuple[list[TLE], int, str]:
        # Ensure epoch_date has a timezone if not already set
        if epoch_date.tzinfo is None:
            epoch_date = epoch_date.replace(tzinfo=timezone.utc)

        two_weeks_prior = epoch_date - timedelta(weeks=2)

        # Ensure current_time has the same timezone awareness as epoch_date
        current_time = datetime.now(timezone.utc)
        total_count = 0

        logger.info(
            f"Fetching TLEs for epoch {epoch_date} (page {page}, per_page {per_page})"
        )
        start_time = time.time()

        try:
            # if the epoch date is in the future, or up to 3 hours ago, use the cache
            if (epoch_date > current_time - timedelta(hours=3)) and self.cache_enabled:
                cached_data = get_cached_data(RECENT_TLES_CACHE_KEY)

                if cached_data:
                    total_count = cached_data.get("total_count", 0)

                if total_count > 0:
                    cached_at_str = cached_data.get(
                        "cached_at", "2000-01-01T00:00:00+00:00"
                    )

                    try:
                        cached_at = datetime.fromisoformat(cached_at_str)
                        # If cached_at has no timezone but should have one, add UTC
                        if cached_at.tzinfo is None and current_time.tzinfo is not None:
                            cached_at = cached_at.replace(tzinfo=timezone.utc)
                    except ValueError as e:
                        logger.error(
                            f"Failed to parse cached_at timestamp: "
                            f"{cached_at_str} - {e}"
                        )
                        cached_at = datetime(2000, 1, 1, tzinfo=timezone.utc)

                    # make sure that the cache is not older than 3 hours as
                    # a double check that this is recent data
                    cache_age = (current_time - cached_at).total_seconds()
                    if cache_age < self.cache_ttl:
                        # Get serialized TLEs from cache
                        serialized_tles = cached_data.get("tles", [])

                        # Deserialize the TLEs
                        tles = self.deserialize_cached_tles(serialized_tles)

                        logger.debug(f"Returning {len(tles)} TLEs from cache")
                        execution_time = time.time() - start_time
                        logger.info(
                            f"Cache retrieval completed in {execution_time:.2f} seconds"
                        )
                        return tles, total_count, "cache"
            else:
                logger.info(f"Cache miss for epoch {epoch_date}")

        except Exception as e:
            logger.error(f"Error getting TLEs from cache: {e}")
            logger.error("TLE cache retrieval failed, loading from database")
            # continue with the database query in case of error

        # If we get here, we need to query the database
        logger.info("Querying database for TLEs")
        try:
            # First get valid satellites
            satellites_sql = text(
                """
                SELECT id, sat_name, sat_number, decay_date, has_current_sat_number,
                constellation, launch_date
                FROM satellites s
                WHERE s.launch_date <= :epoch_date
                AND (s.decay_date IS NULL OR s.decay_date > :epoch_date)
                AND s.sat_name != 'TBA - TO BE ASSIGNED'
                AND (
                    :constellation IS NULL
                    OR (s.constellation IS NOT NULL AND s.constellation
                    ILIKE :constellation || '%')
                )
            """
            )

            if data_source_limit == "any":
                data_source_limit = None

            # Then get their latest TLEs
            tles_sql = text(
                """
                WITH latest_tles AS (
                    SELECT DISTINCT ON (sat_id)
                        id, sat_id, date_collected, tle_line1, tle_line2,
                        epoch, is_supplemental, data_source
                    FROM tle
                    WHERE epoch BETWEEN :start_date AND :end_date
                    AND sat_id = ANY(:satellite_ids)
                    AND (:data_source_limit IS NULL OR data_source = :data_source_limit)
                    ORDER BY sat_id, epoch DESC
                )
                SELECT * FROM latest_tles
                ORDER BY epoch DESC
            """
            )

            # Get valid satellites first
            satellites_result = self.session.execute(
                satellites_sql,
                {"epoch_date": epoch_date, "constellation": constellation},
            )
            valid_satellites = {row.id: row for row in satellites_result}

            if not valid_satellites:
                return [], 0, "database"

            # Then get TLEs for those satellites
            tles_result = self.session.execute(
                tles_sql,
                {
                    "start_date": two_weeks_prior,
                    "end_date": epoch_date,
                    "satellite_ids": list(valid_satellites.keys()),
                    "data_source_limit": data_source_limit,
                },
            )

            # Map results to domain objects
            tles = []
            for row in tles_result:
                sat_data = valid_satellites[row.sat_id]
                satellite = Satellite(
                    sat_name=sat_data.sat_name,
                    sat_number=sat_data.sat_number,
                    decay_date=sat_data.decay_date,
                    has_current_sat_number=sat_data.has_current_sat_number,
                    constellation=sat_data.constellation,
                )

                tle = TLE(
                    satellite=satellite,
                    date_collected=row.date_collected,
                    tle_line1=row.tle_line1,
                    tle_line2=row.tle_line2,
                    epoch=row.epoch,
                    is_supplemental=row.is_supplemental,
                    data_source=row.data_source,
                )
                tles.append(tle)

            # Handle pagination
            total_count = len(tles)
            if format != "zip":
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page
                tles = tles[start_idx:end_idx]
                logger.info(
                    f"Pagination: returning {len(tles)} TLEs out of {total_count} total"
                )

            execution_time = time.time() - start_time
            logger.info(f"Database query completed in {execution_time:.2f} seconds")
            return tles, total_count, "database"

        except Exception as e:
            logger.error(f"Error getting TLEs: {e}")
            self.session.rollback()
            logger.error("Database query failed, rolling back transaction")
            raise

    def _get_all_tles_at_epoch_experimental(
        self,
        epoch_date: datetime,
        page: int,
        per_page: int,
        format: str,
        constellation: Optional[str] = None,
        data_source: Optional[str] = None,
    ) -> tuple[list[TLE], int, str]:  # pragma: no cover
        # Ensure epoch_date has a timezone if not already set
        if epoch_date.tzinfo is None:
            epoch_date = epoch_date.replace(tzinfo=timezone.utc)

        two_weeks_prior = epoch_date - timedelta(weeks=2)

        # Ensure current_time has the same timezone awareness as epoch_date
        current_time = datetime.now(timezone.utc)
        total_count = 0

        logger.info(
            f"Fetching TLEs for epoch {epoch_date} (page {page}, per_page {per_page})"
        )
        start_time = time.time()

        try:
            # if the epoch date is in the future, or up to 3 hours ago, use the cache
            if (epoch_date > current_time - timedelta(hours=3)) and self.cache_enabled:
                cached_data = get_cached_data(RECENT_TLES_CACHE_KEY)

                if cached_data:
                    total_count = cached_data.get("total_count", 0)

                if total_count > 0:
                    cached_at_str = cached_data.get(
                        "cached_at", "2000-01-01T00:00:00+00:00"
                    )

                    try:
                        cached_at = datetime.fromisoformat(cached_at_str)
                        # If cached_at has no timezone but should have one, add UTC
                        if cached_at.tzinfo is None and current_time.tzinfo is not None:
                            cached_at = cached_at.replace(tzinfo=timezone.utc)
                    except ValueError as e:
                        logger.error(
                            f"Failed to parse cached_at timestamp: "
                            f"{cached_at_str} - {e}"
                        )
                        cached_at = datetime(2000, 1, 1, tzinfo=timezone.utc)

                    # make sure that the cache is not older than 3 hours as
                    # a double check that this is recent data
                    cache_age = (current_time - cached_at).total_seconds()
                    if cache_age < self.cache_ttl:
                        # Get serialized TLEs from cache
                        serialized_tles = cached_data.get("tles", [])

                        # Deserialize the TLEs
                        tles = self.deserialize_cached_tles(serialized_tles)

                        logger.debug(f"Returning {len(tles)} TLEs from cache")
                        execution_time = time.time() - start_time
                        logger.info(
                            f"Cache retrieval completed in {execution_time:.2f} seconds"
                        )
                        return tles, total_count, "cache"
            else:
                logger.info(f"Cache miss for epoch {epoch_date}")

        except Exception as e:
            logger.error(f"Error getting TLEs from cache: {e}")
            logger.error("TLE cache retrieval failed, loading from database")
            # continue with the database query in case of error

        # If we get here, we need to query the database
        logger.info("Querying database for TLEs")

        if data_source == "any":
            data_source = None

        try:
            tles_sql = text(
                """
                WITH RECURSIVE latest_per_sat AS (
                    SELECT
                        s.id AS sat_id,
                        (
                            SELECT t.id
                            FROM tle t
                            WHERE t.sat_id = s.id
                                AND t.epoch BETWEEN :start_date AND :end_date
                                AND (:data_source IS NULL OR t.data_source = :data_source)
                            ORDER BY t.epoch DESC
                            LIMIT 1
                        ) AS tle_id
                    FROM satellites s
                    WHERE s.launch_date <= :epoch_date
                        AND (s.decay_date IS NULL OR s.decay_date > :epoch_date)
                        AND s.sat_name != 'TBA - TO BE ASSIGNED'
                        AND (
                            :constellation IS NULL
                            OR (s.constellation IS NOT NULL AND s.constellation
                            ILIKE :constellation || '%')
                        )
                )
                SELECT t.*, s.*
                FROM latest_per_sat l
                JOIN tle t ON t.id = l.tle_id
                JOIN satellites s ON s.id = l.sat_id
                ORDER BY t.epoch DESC
                """  # noqa: E501
            ).bindparams(
                start_date=bindparam("start_date", type_=DateTime(timezone=True)),
                end_date=bindparam("end_date", type_=DateTime(timezone=True)),
                epoch_date=bindparam("epoch_date", type_=DateTime(timezone=True)),
                constellation=bindparam("constellation", type_=String),
                data_source=bindparam("data_source", type_=String),
            )

            # Then get TLEs for those satellites
            tles_result = self.session.execute(
                tles_sql,
                {
                    "start_date": two_weeks_prior,
                    "end_date": epoch_date,
                    "epoch_date": epoch_date,
                    "constellation": constellation,
                    "data_source": data_source,
                },
            )

            # Map results to domain objects
            tles = []
            for row in tles_result:
                satellite = Satellite(
                    sat_name=row.sat_name,
                    sat_number=row.sat_number,
                    decay_date=row.decay_date,
                    has_current_sat_number=row.has_current_sat_number,
                    constellation=row.constellation,
                )

                tle = TLE(
                    satellite=satellite,
                    date_collected=row.date_collected,
                    tle_line1=row.tle_line1,
                    tle_line2=row.tle_line2,
                    epoch=row.epoch,
                    is_supplemental=row.is_supplemental,
                    data_source=row.data_source,
                )
                tles.append(tle)

            # Handle pagination
            total_count = len(tles)
            if format != "zip":
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page
                tles = tles[start_idx:end_idx]
                logger.info(
                    f"Pagination: returning {len(tles)} TLEs out of {total_count} total"
                )

            execution_time = time.time() - start_time
            logger.info(f"Database query completed in {execution_time:.2f} seconds")
            return tles, total_count, "database"

        except Exception as e:
            logger.error(f"Error getting TLEs: {e}")
            self.session.rollback()
            logger.error("Database query failed, rolling back transaction")
            raise

    def _get_nearest_tle(self, id: str, id_type: str, epoch: datetime) -> Optional[TLE]:
        try:
            if id_type == "catalog":
                nearest_sat_id = self._get_correct_satellite_id_at_tle_epoch(
                    id, id_type, epoch
                )
                if nearest_sat_id is None:
                    return None
            else:
                nearest_sat_id = self._get_correct_satellite_id_at_tle_epoch(
                    id, id_type, epoch
                )
                if nearest_sat_id is None:
                    return None

            # Create a bind parameter for the epoch
            epoch_param = bindparam("epoch", epoch, type_=DateTime(timezone=True))

            # Then get the nearest TLE for this satellite
            nearest_tle = (
                self.session.query(TLEDb)
                .filter(TLEDb.sat_id == nearest_sat_id)
                .order_by(
                    func.abs(
                        func.extract("epoch", TLEDb.epoch)
                        - func.extract("epoch", epoch_param)
                    )
                )
                .first()
            )

            if nearest_tle is None:
                return None

            return self._to_domain(nearest_tle)

        except NoResultFound:
            return None

        except Exception:
            self.session.rollback()
            raise

    def _get_adjacent_tles(self, id: str, id_type: str, epoch: datetime) -> list[TLE]:
        if epoch.tzinfo is None:
            epoch = epoch.replace(tzinfo=timezone.utc)

        try:
            if id_type == "catalog":
                # Get all satellites with the same catalog number.
                # This is because there are often multiple satellite names
                # associated with the same catalog number, and until the
                # database is updated to have a satellite name history, we
                # need to see which one has the TLE that is closest to the
                # specified epoch.
                nearest_sat_id = self._get_correct_satellite_id_at_tle_epoch(
                    id, id_type, epoch
                )
                if nearest_sat_id is None:
                    return []

            # Get the TLE before the specified epoch
            before_tle = (
                self.session.query(TLEDb)
                .filter(TLEDb.sat_id == nearest_sat_id, TLEDb.epoch < epoch)
                .order_by(TLEDb.epoch.desc())
                .first()
            )

            # Get the TLE after the specified epoch
            after_tle = (
                self.session.query(TLEDb)
                .filter(TLEDb.sat_id == nearest_sat_id, TLEDb.epoch > epoch)
                .order_by(TLEDb.epoch.asc())
                .first()
            )

            # Convert to domain objects if they exist
            result = []
            if before_tle:
                domain_before = self._to_domain(before_tle)
                if domain_before is not None:
                    result.append(domain_before)

            if after_tle:
                domain_after = self._to_domain(after_tle)
                if domain_after is not None:
                    result.append(domain_after)

            return result

        except NoResultFound:
            return []

        except Exception:
            self.session.rollback()
            raise

    def _get_tles_around_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
        count_before: int,
        count_after: int,
    ) -> list[TLE]:
        try:
            if id_type == "catalog":
                nearest_sat_id = self._get_correct_satellite_id_at_tle_epoch(
                    id, id_type, epoch
                )
                if nearest_sat_id is None:
                    return []

            # Get the TLEs before the specified epoch
            before_tles = (
                self.session.query(TLEDb)
                .filter(TLEDb.sat_id == nearest_sat_id, TLEDb.epoch < epoch)
                .order_by(TLEDb.epoch.desc())
                .limit(count_before)
                .all()
            )

            # Get the TLEs after the specified epoch
            after_tles = (
                self.session.query(TLEDb)
                .filter(TLEDb.sat_id == nearest_sat_id, TLEDb.epoch > epoch)
                .order_by(TLEDb.epoch.asc())
                .limit(count_after)
                .all()
            )

            # Convert to domain objects
            result = []
            for tle in before_tles:
                domain_tle = self._to_domain(tle)
                if domain_tle is not None:
                    result.append(domain_tle)

            for tle in after_tles:
                domain_tle = self._to_domain(tle)
                if domain_tle is not None:
                    result.append(domain_tle)

            return result
        except NoResultFound:
            return []

        except Exception:
            self.session.rollback()
            raise

    def _get_correct_satellite_id_at_tle_epoch(
        self, id: str, id_type: str, epoch: datetime
    ) -> Optional[int]:
        if id_type == "catalog":
            satellites_with_this_identifier = (
                self.session.query(SatelliteDb)
                .filter(SatelliteDb.sat_number == id)
                .all()
            )
        else:
            satellites_with_this_identifier = (
                self.session.query(SatelliteDb).filter(SatelliteDb.sat_name == id).all()
            )

        if len(satellites_with_this_identifier) == 0:
            return None

        epoch = ensure_datetime(epoch)
        # Create a bind parameter for the epoch
        epoch_param = bindparam("epoch", epoch, type_=DateTime(timezone=True))

        # get the closest TLE for each satellite
        closest_tles = []
        for sat in satellites_with_this_identifier:
            closest_tles.append(
                self.session.query(TLEDb)
                .filter(TLEDb.sat_id == sat.id)
                .order_by(
                    func.abs(
                        func.extract("epoch", TLEDb.epoch)
                        - func.extract("epoch", epoch_param)
                    )
                )
                .first()
            )
        # get the TLE with the epoch closest to the specified epoch
        nearest_tle = min(closest_tles, key=lambda tle: abs(tle.epoch - epoch))
        nearest_sat_id = int(
            nearest_tle.sat_id
        )  # Explicitly cast to int for type checker

        return nearest_sat_id
