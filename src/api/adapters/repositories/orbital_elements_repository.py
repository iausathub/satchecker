import abc
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import text

from api.adapters.database_orm import OrbitalElementsDb
from api.adapters.repositories.orbital_data_lookup_mixin import OrbitalDataLookupMixin
from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.domain.models.orbital_elements import OrbitalElements
from api.domain.models.satellite import Satellite
from api.services.cache_service import (
    RECENT_ORBITAL_ELEMENTS_CACHE_KEY,
    get_cached_data,
)

logger = logging.getLogger(__name__)


class AbstractOrbitalElementsRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, orbital_elements: OrbitalElements):
        self._add(orbital_elements)
        self.seen.add(orbital_elements)

    def get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> OrbitalElements | None:
        record = self._get_closest_by_satellite_number(
            satellite_number, epoch, data_source
        )
        if record:
            self.seen.add(record)
        return record

    def get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> OrbitalElements | None:
        record = self._get_closest_by_satellite_name(satellite_name, epoch, data_source)
        if record:
            self.seen.add(record)
        return record

    def get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[OrbitalElements]:
        return self._get_all_for_date_range_by_satellite_number(
            satellite_number, start_date, end_date
        )

    def get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[OrbitalElements]:
        return self._get_all_for_date_range_by_satellite_name(
            satellite_name, start_date, end_date
        )

    def get_all_orbital_elements_at_epoch(
        self,
        epoch_date: datetime,
        page: int,
        per_page: int,
        format: str,
        constellation: str | None = None,
        data_source_limit: str | None = None,
        use_generated_tles: bool = False,
    ) -> tuple[list[OrbitalElements], int, str]:
        return self._get_all_orbital_elements_at_epoch(
            epoch_date,
            page,
            per_page,
            format,
            constellation,
            data_source_limit,
            use_generated_tles,
        )

    def get_nearest_orbital_elements(
        self, id: str, id_type: str, epoch: datetime
    ) -> OrbitalElements | None:
        return self._get_nearest_orbital_elements(id, id_type, epoch)

    def get_adjacent_orbital_elements(
        self, id: str, id_type: str, epoch: datetime
    ) -> list[OrbitalElements]:
        return self._get_adjacent_orbital_elements(id, id_type, epoch)

    def get_orbital_elements_around_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
        count_before: int,
        count_after: int,
    ) -> list[OrbitalElements]:
        return self._get_orbital_elements_around_epoch(
            id, id_type, epoch, count_before, count_after
        )

    @abc.abstractmethod
    def _get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> OrbitalElements | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> OrbitalElements | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[OrbitalElements]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[OrbitalElements]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_orbital_elements_at_epoch(
        self,
        epoch_date: datetime,
        page: int,
        per_page: int,
        format: str,
        constellation: str | None = None,
        data_source_limit: str | None = None,
        use_generated_tles: bool = False,
    ) -> tuple[list[OrbitalElements], int, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_orbital_elements_around_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
        count_before: int,
        count_after: int,
    ) -> list[OrbitalElements]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_nearest_orbital_elements(
        self, id: str, id_type: str, epoch: datetime
    ) -> OrbitalElements | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_adjacent_orbital_elements(
        self, id: str, id_type: str, epoch: datetime
    ) -> list[OrbitalElements]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, orbital_elements: OrbitalElements):
        raise NotImplementedError


class SqlAlchemyOrbitalElementsRepository(
    OrbitalDataLookupMixin,
    AbstractOrbitalElementsRepository,
):
    _orm_model = OrbitalElementsDb

    def __init__(self, session):
        super().__init__()
        self.session = session

        # Default cache TTL in seconds - can be overridden in tests
        self.cache_ttl = 10800  # 3 hours
        self.cache_enabled = True

    @staticmethod
    def _to_domain(orm) -> OrbitalElements | None:
        if orm is None:
            return None

        if orm.satellite is None:
            logger.warning(
                f"Found orbital elements with ID {orm.id} without a satellite"
            )
            return None

        satellite = SqlAlchemySatelliteRepository._to_domain(orm.satellite)
        if satellite is None:
            logger.warning(
                f"Failed to convert satellite for orbital elements with ID {orm.id}"
            )
            return None

        return OrbitalElements(
            date_collected=orm.date_collected,
            epoch=orm.epoch,
            data_source=orm.data_source,
            satellite=satellite,
            mean_motion=orm.mean_motion,
            eccentricity=orm.eccentricity,
            inclination=orm.inclination,
            ra_of_ascending_node=orm.ra_of_ascending_node,
            arg_of_pericenter=orm.arg_of_pericenter,
            mean_anomaly=orm.mean_anomaly,
            ephemeris_type=orm.ephemeris_type,
            classification_type=orm.classification_type,
            element_set_no=orm.element_set_no,
            rev_at_epoch=orm.rev_at_epoch,
            bstar=orm.bstar,
            mean_motion_dot=orm.mean_motion_dot,
            mean_motion_ddot=orm.mean_motion_ddot,
        )

    @staticmethod
    def _to_orm(domain_orbital_elements) -> OrbitalElementsDb:
        return OrbitalElementsDb(
            date_collected=domain_orbital_elements.date_collected,
            epoch=domain_orbital_elements.epoch,
            data_source=domain_orbital_elements.data_source,
            satellite=SqlAlchemySatelliteRepository._to_orm(
                domain_orbital_elements.satellite
            ),
            mean_motion=domain_orbital_elements.mean_motion,
            eccentricity=domain_orbital_elements.eccentricity,
            inclination=domain_orbital_elements.inclination,
            ra_of_ascending_node=domain_orbital_elements.ra_of_ascending_node,
            arg_of_pericenter=domain_orbital_elements.arg_of_pericenter,
            mean_anomaly=domain_orbital_elements.mean_anomaly,
            ephemeris_type=domain_orbital_elements.ephemeris_type,
            classification_type=domain_orbital_elements.classification_type,
            element_set_no=domain_orbital_elements.element_set_no,
            rev_at_epoch=domain_orbital_elements.rev_at_epoch,
            bstar=domain_orbital_elements.bstar,
            mean_motion_dot=domain_orbital_elements.mean_motion_dot,
            mean_motion_ddot=domain_orbital_elements.mean_motion_ddot,
        )

    @staticmethod
    def batch_serialize_orbital_elements(
        orbital_elements: list[OrbitalElements],
    ) -> list[dict[str, Any]]:
        """
        Efficiently serialize a batch of orbital elements for caching.
        Much faster than serializing one by one, especially for large datasets.

        Args:
            orbital_elements: List of orbital elements to serialize

        Returns:
            List of serialized orbital element dictionaries
        """
        result: list[dict[str, Any]] = []
        result_append = result.append

        for orbital_element in orbital_elements:
            # Get satellite information once to avoid repeated attribute access
            satellite = orbital_element.satellite
            decay_date = satellite.decay_date

            # Create efficient orbital element dictionary with direct attribute access
            orbital_element_dict = {
                "mean_motion": orbital_element.mean_motion,
                "eccentricity": orbital_element.eccentricity,
                "inclination": orbital_element.inclination,
                "ra_of_ascending_node": orbital_element.ra_of_ascending_node,
                "arg_of_pericenter": orbital_element.arg_of_pericenter,
                "mean_anomaly": orbital_element.mean_anomaly,
                "ephemeris_type": orbital_element.ephemeris_type,
                "classification_type": orbital_element.classification_type,
                "element_set_no": orbital_element.element_set_no,
                "rev_at_epoch": orbital_element.rev_at_epoch,
                "bstar": orbital_element.bstar,
                "mean_motion_dot": orbital_element.mean_motion_dot,
                "mean_motion_ddot": orbital_element.mean_motion_ddot,
                "epoch": orbital_element.epoch.isoformat(),
                "date_collected": orbital_element.date_collected.isoformat(),
                "data_source": orbital_element.data_source,
                "satellite": {
                    "sat_name": satellite.sat_name,
                    "sat_number": satellite.sat_number,
                    "decay_date": decay_date.isoformat() if decay_date else None,
                    "has_current_sat_number": getattr(
                        satellite, "has_current_sat_number", True
                    ),
                },
            }
            result_append(orbital_element_dict)

        return result

    @staticmethod
    def deserialize_orbital_elements(
        serialized_orbital_elements: list[dict[str, Any]],
    ) -> list[OrbitalElements]:
        """
        Convert serialized orbital element dictionaries from the cache back into
        domain OrbitalElements objects.

        Args:
            serialized_orbital_elements: List of serialized orbital element
                dictionaries from the cache

        Returns:
            List of OrbitalElements domain objects
        """
        orbital_elements = []

        for orbital_element_dict in serialized_orbital_elements:
            try:
                # Extract satellite data and create Satellite domain object
                sat_data = orbital_element_dict.get("satellite", {})

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
                epoch = datetime.fromisoformat(orbital_element_dict.get("epoch", ""))
                date_collected = datetime.fromisoformat(
                    orbital_element_dict.get("date_collected", "")
                )

                # Create the OrbitalElements domain object
                orbital_element = OrbitalElements(
                    satellite=satellite,
                    mean_motion=orbital_element_dict.get("mean_motion", 0),
                    eccentricity=orbital_element_dict.get("eccentricity", 0),
                    inclination=orbital_element_dict.get("inclination", 0),
                    ra_of_ascending_node=orbital_element_dict.get(
                        "ra_of_ascending_node", 0
                    ),
                    arg_of_pericenter=orbital_element_dict.get("arg_of_pericenter", 0),
                    mean_anomaly=orbital_element_dict.get("mean_anomaly", 0),
                    ephemeris_type=orbital_element_dict.get("ephemeris_type", 0),
                    classification_type=orbital_element_dict.get(
                        "classification_type", ""
                    ),
                    element_set_no=orbital_element_dict.get("element_set_no", 0),
                    rev_at_epoch=orbital_element_dict.get("rev_at_epoch", 0),
                    bstar=orbital_element_dict.get("bstar", 0),
                    mean_motion_dot=orbital_element_dict.get("mean_motion_dot", 0),
                    mean_motion_ddot=orbital_element_dict.get("mean_motion_ddot", 0),
                    epoch=epoch,
                    date_collected=date_collected,
                    data_source=orbital_element_dict.get("data_source", ""),
                )

                orbital_elements.append(orbital_element)
            except Exception as e:
                logger.error(f"Error deserializing orbital elements: {e}")
                raise e

        return orbital_elements

    def _get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> OrbitalElements | None:
        return self._lookup_closest_by_satellite_number(
            satellite_number, epoch, data_source
        )

    def _get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> OrbitalElements | None:
        return self._lookup_closest_by_satellite_name(
            satellite_name, epoch, data_source
        )

    def _get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[OrbitalElements]:
        return self._lookup_all_for_date_range_by_satellite_number(
            satellite_number, start_date, end_date
        )

    def _get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[OrbitalElements]:
        return self._lookup_all_for_date_range_by_satellite_name(
            satellite_name, start_date, end_date
        )

    def _get_all_orbital_elements_at_epoch(
        self,
        epoch_date: datetime,
        page: int,
        per_page: int,
        format: str,
        constellation: str | None = None,
        data_source_limit: str | None = None,
        use_generated_tles: bool = False,
    ) -> tuple[list[OrbitalElements], int, str]:
        # Ensure epoch_date has a timezone if not already set
        if epoch_date.tzinfo is None:
            epoch_date = epoch_date.replace(tzinfo=timezone.utc)

        two_weeks_prior = epoch_date - timedelta(weeks=2)

        # Ensure current_time has the same timezone awareness as epoch_date
        current_time = datetime.now(timezone.utc)
        total_count = 0

        logger.debug(
            f"Fetching orbital elements for epoch {epoch_date} "
            f"(page {page}, per_page {per_page})"
        )
        start_time = time.time()

        try:
            # if the epoch date is in the future, or up to 3 hours ago, use the cache
            if (epoch_date > current_time - timedelta(hours=3)) and self.cache_enabled:
                cached_data = get_cached_data(RECENT_ORBITAL_ELEMENTS_CACHE_KEY)

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
                        # Get serialized orbital elements from cache
                        serialized_orbital_elements = cached_data.get(
                            "orbital_elements", []
                        )

                        # Deserialize the orbital elements
                        orbital_elements = self.deserialize_orbital_elements(
                            serialized_orbital_elements
                        )

                        logger.debug(
                            f"Returning {len(orbital_elements)} orbital elements "
                            "from cache"
                        )
                        execution_time = time.time() - start_time
                        logger.debug(
                            f"Cache retrieval completed in {execution_time:.2f} seconds"
                        )
                        return orbital_elements, total_count, "cache"
            else:
                logger.debug(f"Cache miss for epoch {epoch_date}")

        except Exception as e:
            logger.error(f"Error getting orbital elements from cache: {e}")
            logger.error(
                "Orbital elements cache retrieval failed, loading from database"
            )
            # continue with the database query in case of error

        # If we get here, we need to query the database
        logger.debug("Querying database for orbital elements")
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

            # Then get their latest orbital elements
            orbital_elements_sql = text("""
                WITH latest_orbital_elements AS (
                    SELECT DISTINCT ON (sat_id)
                        id, sat_id, date_collected, epoch, data_source, mean_motion,
                        eccentricity, inclination, ra_of_ascending_node,
                        arg_of_pericenter, mean_anomaly, ephemeris_type,
                        classification_type, element_set_no, rev_at_epoch, bstar,
                        mean_motion_dot, mean_motion_ddot
                    FROM orbital_elements
                    WHERE epoch BETWEEN :start_date AND :end_date
                    AND sat_id = ANY(:satellite_ids)
                    AND (:data_source_limit IS NULL OR data_source = :data_source_limit)
                    AND (
                        (:use_generated_tles AND data_source = 'generated')
                        OR (NOT :use_generated_tles AND data_source != 'generated')
                    )
                    ORDER BY sat_id, epoch DESC
                )
                SELECT * FROM latest_orbital_elements
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

            # Then get orbital elements for those satellites
            orbital_elements_result = self.session.execute(
                orbital_elements_sql,
                {
                    "start_date": two_weeks_prior,
                    "end_date": epoch_date,
                    "satellite_ids": list(valid_satellites.keys()),
                    "data_source_limit": data_source_limit,
                    "use_generated_tles": use_generated_tles,
                },
            )

            # Map results to domain objects
            orbital_elements = []
            for row in orbital_elements_result:
                sat_data = valid_satellites[row.sat_id]
                satellite = Satellite(
                    sat_name=sat_data.sat_name,
                    sat_number=sat_data.sat_number,
                    decay_date=sat_data.decay_date,
                    has_current_sat_number=sat_data.has_current_sat_number,
                    constellation=sat_data.constellation,
                )

                orbital_elements_object = OrbitalElements(
                    satellite=satellite,
                    date_collected=row.date_collected,
                    epoch=row.epoch,
                    data_source=row.data_source,
                    mean_motion=row.mean_motion,
                    eccentricity=row.eccentricity,
                    inclination=row.inclination,
                    ra_of_ascending_node=row.ra_of_ascending_node,
                    arg_of_pericenter=row.arg_of_pericenter,
                    mean_anomaly=row.mean_anomaly,
                    ephemeris_type=row.ephemeris_type,
                    classification_type=row.classification_type,
                    element_set_no=row.element_set_no,
                    rev_at_epoch=row.rev_at_epoch,
                    bstar=row.bstar,
                    mean_motion_dot=row.mean_motion_dot,
                    mean_motion_ddot=row.mean_motion_ddot,
                )
                orbital_elements.append(orbital_elements_object)

            # Handle pagination
            total_count = len(orbital_elements)
            if format != "zip":
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page
                orbital_elements = orbital_elements[start_idx:end_idx]
                logger.debug(
                    f"Pagination: returning {len(orbital_elements)} orbital "
                    f"elements out of {total_count} total"
                )

            execution_time = time.time() - start_time
            logger.debug(f"Database query completed in {execution_time:.2f} seconds")
            return orbital_elements, total_count, "database"

        except Exception as e:
            logger.error(f"Error getting orbital elements: {e}")
            self.session.rollback()
            logger.error("Database query failed, rolling back transaction")
            raise

    def _get_orbital_elements_around_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
        count_before: int,
        count_after: int,
    ) -> list[OrbitalElements]:
        return self._lookup_records_around_epoch(
            id, id_type, epoch, count_before, count_after
        )

    def _get_nearest_orbital_elements(
        self, id: str, id_type: str, epoch: datetime
    ) -> OrbitalElements | None:
        return self._lookup_nearest_at_epoch(id, id_type, epoch)

    def _get_adjacent_orbital_elements(
        self, id: str, id_type: str, epoch: datetime
    ) -> list[OrbitalElements]:
        return self._lookup_adjacent_at_epoch(id, id_type, epoch)

    def _add(self, orbital_elements: OrbitalElements):
        return self._lookup_add_record(orbital_elements)
