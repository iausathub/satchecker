import abc
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import DateTime, String, bindparam, text

from api.adapters.database_orm import TLEDb
from api.adapters.repositories.orbital_data_lookup_mixin import OrbitalDataLookupMixin
from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.domain.models.satellite import Satellite as Satellite
from api.domain.models.tle import TLE
from api.services.cache_service import RECENT_TLES_CACHE_KEY, get_cached_data

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
    ) -> TLE | None:
        tle = self._get_closest_by_satellite_number(
            satellite_number, epoch, data_source
        )
        if tle:
            self.seen.add(tle)
        return tle

    def get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> TLE | None:
        tle = self._get_closest_by_satellite_name(satellite_name, epoch, data_source)
        if tle:
            self.seen.add(tle)
        return tle

    def get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[TLE]:
        return self._get_all_for_date_range_by_satellite_number(
            satellite_number, start_date, end_date
        )

    def get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: datetime | None,
        end_date: datetime | None,
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
        constellation: str | None = None,
        data_source_limit: str | None = None,
        use_generated_tles: bool = False,
    ) -> tuple[list[TLE], int, str]:
        return self._get_all_tles_at_epoch(
            epoch_date,
            page,
            per_page,
            format,
            constellation,
            data_source_limit,
            use_generated_tles,
        )

    def get_nearest_tle(self, id: str, id_type: str, epoch: datetime) -> TLE | None:
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
    ) -> TLE | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> TLE | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_tles_at_epoch(
        self,
        epoch_date: datetime,
        page: int,
        per_page: int,
        format: str,
        constellation: str | None = None,
        data_source_limit: str | None = None,
        use_generated_tles: bool = False,
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
    def _get_nearest_tle(self, id: str, id_type: str, epoch: datetime) -> TLE | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_adjacent_tles(self, id: str, id_type: str, epoch: datetime) -> list[TLE]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, tle: TLE):
        raise NotImplementedError


class SqlAlchemyTLERepository(OrbitalDataLookupMixin, AbstractTLERepository):
    _orm_model = TLEDb

    def __init__(self, session):
        super().__init__()
        self.session = session
        # Default cache TTL in seconds - can be overridden in tests
        self.cache_ttl = 10800  # 3 hours
        self.cache_enabled = True

    @staticmethod
    def _to_domain(orm_tle) -> TLE | None:
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
    def batch_serialize_tles(tles: list[TLE]) -> list[dict[str, Any]]:
        """
        Efficiently serialize a batch of TLEs for caching.
        Much faster than serializing one by one, especially for large datasets.

        Args:
            tles: List of TLE objects to serialize

        Returns:
            List of serialized TLE dictionaries
        """
        result: list[dict[str, Any]] = []
        result_append = result.append

        for tle in tles:
            # Get satellite information once to avoid repeated attribute access
            satellite = tle.satellite
            decay_date = satellite.decay_date

            # Create efficient TLE dictionary with direct attribute access
            tle_dict = {
                "tle_line1": tle.tle_line1,
                "tle_line2": tle.tle_line2,
                "epoch": tle.epoch.isoformat(),
                "date_collected": tle.date_collected.isoformat(),
                "is_supplemental": tle.is_supplemental,
                "data_source": tle.data_source,
                "satellite": {
                    "sat_name": satellite.sat_name,
                    "sat_number": satellite.sat_number,
                    "decay_date": decay_date.isoformat() if decay_date else None,
                    "has_current_sat_number": getattr(
                        satellite, "has_current_sat_number", True
                    ),
                },
            }
            result_append(tle_dict)

        return result

    @staticmethod
    def deserialize_tles(serialized_tles: list[dict[str, Any]]) -> list[TLE]:
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
        return self._lookup_add_record(tle)

    def _get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> TLE | None:
        return self._lookup_closest_by_satellite_number(
            satellite_number, epoch, data_source
        )

    def _get_closest_by_satellite_name(
        self,
        satellite_name: str,
        epoch: datetime,
        data_source: str,
    ) -> TLE | None:
        return self._lookup_closest_by_satellite_name(
            satellite_name, epoch, data_source
        )

    def _get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[TLE]:
        return self._lookup_all_for_date_range_by_satellite_number(
            satellite_number, start_date, end_date
        )

    def _get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[TLE]:
        return self._lookup_all_for_date_range_by_satellite_name(
            satellite_name, start_date, end_date
        )

    def _get_all_tles_at_epoch(
        self,
        epoch_date: datetime,
        page: int,
        per_page: int,
        format: str,
        constellation: str | None = None,
        data_source_limit: str | None = None,
        use_generated_tles: bool = False,
    ) -> tuple[list[TLE], int, str]:
        # Ensure epoch_date has a timezone if not already set
        if epoch_date.tzinfo is None:
            epoch_date = epoch_date.replace(tzinfo=timezone.utc)

        two_weeks_prior = epoch_date - timedelta(weeks=2)

        # Ensure current_time has the same timezone awareness as epoch_date
        current_time = datetime.now(timezone.utc)
        total_count = 0

        logger.debug(
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
                        tles = self.deserialize_tles(serialized_tles)

                        logger.debug(f"Returning {len(tles)} TLEs from cache")
                        execution_time = time.time() - start_time
                        logger.debug(
                            f"Cache retrieval completed in {execution_time:.2f} seconds"
                        )
                        return tles, total_count, "cache"
            else:
                logger.debug(f"Cache miss for epoch {epoch_date}")

        except Exception as e:
            logger.error(f"Error getting TLEs from cache: {e}")
            logger.error("TLE cache retrieval failed, loading from database")
            # continue with the database query in case of error

        # If we get here, we need to query the database
        logger.debug("Querying database for TLEs")
        try:
            # First get valid satellites
            satellites_sql = text("""
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
            """)

            if data_source_limit == "any":
                data_source_limit = None

            # Then get their latest TLEs
            tles_sql = text("""
                WITH latest_tles AS (
                    SELECT DISTINCT ON (sat_id)
                        id, sat_id, date_collected, tle_line1, tle_line2,
                        epoch, is_supplemental, data_source
                    FROM tle
                    WHERE epoch BETWEEN :start_date AND :end_date
                    AND sat_id = ANY(:satellite_ids)
                    AND (:data_source_limit IS NULL OR data_source = :data_source_limit)
                    AND (
                        (:use_generated_tles AND data_source = 'generated')
                        OR (NOT :use_generated_tles AND data_source != 'generated')
                    )
                    ORDER BY sat_id, epoch DESC
                )
                SELECT * FROM latest_tles
                ORDER BY epoch DESC
            """)

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
                    "use_generated_tles": use_generated_tles,
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
                logger.debug(
                    f"Pagination: returning {len(tles)} TLEs out of {total_count} total"
                )

            execution_time = time.time() - start_time
            logger.debug(f"Database query completed in {execution_time:.2f} seconds")
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
        constellation: str | None = None,
        data_source: str | None = None,
    ) -> tuple[list[TLE], int, str]:  # pragma: no cover
        # Ensure epoch_date has a timezone if not already set
        if epoch_date.tzinfo is None:
            epoch_date = epoch_date.replace(tzinfo=timezone.utc)

        two_weeks_prior = epoch_date - timedelta(weeks=2)

        # Ensure current_time has the same timezone awareness as epoch_date
        current_time = datetime.now(timezone.utc)
        total_count = 0

        logger.debug(
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
                        tles = self.deserialize_tles(serialized_tles)

                        logger.debug(f"Returning {len(tles)} TLEs from cache")
                        execution_time = time.time() - start_time
                        logger.debug(
                            f"Cache retrieval completed in {execution_time:.2f} seconds"
                        )
                        return tles, total_count, "cache"
            else:
                logger.debug(f"Cache miss for epoch {epoch_date}")

        except Exception as e:
            logger.error(f"Error getting TLEs from cache: {e}")
            logger.error("TLE cache retrieval failed, loading from database")
            # continue with the database query in case of error

        # If we get here, we need to query the database
        logger.debug("Querying database for TLEs")

        if data_source == "any":
            data_source = None

        try:
            tles_sql = text("""
                WITH RECURSIVE latest_per_sat AS (
                    SELECT
                        s.id AS sat_id,
                        (
                            SELECT t.id
                            FROM tle t
                            WHERE t.sat_id = s.id
                                AND t.epoch BETWEEN :start_date AND :end_date
                                AND (
                                :data_source IS NULL OR t.data_source = :data_source
                                )
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
                """).bindparams(  # noqa: E501
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
                logger.debug(
                    f"Pagination: returning {len(tles)} TLEs out of {total_count} total"
                )

            execution_time = time.time() - start_time
            logger.debug(f"Database query completed in {execution_time:.2f} seconds")
            return tles, total_count, "database"

        except Exception as e:
            logger.error(f"Error getting TLEs: {e}")
            self.session.rollback()
            logger.error("Database query failed, rolling back transaction")
            raise

    def _get_nearest_tle(self, id: str, id_type: str, epoch: datetime) -> TLE | None:
        return self._lookup_nearest_at_epoch(id, id_type, epoch)

    def _get_adjacent_tles(self, id: str, id_type: str, epoch: datetime) -> list[TLE]:
        return self._lookup_adjacent_at_epoch(id, id_type, epoch)

    def _get_tles_around_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
        count_before: int,
        count_after: int,
    ) -> list[TLE]:
        return self._lookup_records_around_epoch(
            id, id_type, epoch, count_before, count_after
        )
