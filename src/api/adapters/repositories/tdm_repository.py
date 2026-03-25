import abc
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import bindparam, text
from sqlalchemy.orm.exc import NoResultFound

from api.adapters.database_orm import SatelliteDb, TdmPredictionDb
from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.domain.models.satellite import Satellite as Satellite
from api.domain.models.tdm_prediction import TdmPrediction
from api.domain.models.tdm_prediction_point import TdmPredictionPoint

# Set up logger
logger = logging.getLogger(__name__)


class AbstractTdmPredictionRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, tdm_prediction: TdmPrediction):
        self._add(tdm_prediction)
        self.seen.add(tdm_prediction)

    def get_all_tdm_predictions_at_epoch(
        self,
        epoch_date: datetime,
        duration: float,
        page: int,
        per_page: int,
        format: str,
        site_name: str,
        constellation: str | None = None,
    ) -> tuple[list[TdmPrediction], int, str]:
        return self._get_all_tdm_predictions_at_epoch(
            epoch_date, duration, page, per_page, format, site_name, constellation
        )

    def get_tdm_prediction_points(
        self,
        tdm_prediction_ids: list[int],
    ) -> list[TdmPredictionPoint]:
        return self._get_tdm_prediction_points(tdm_prediction_ids)

    @abc.abstractmethod
    def _get_all_tdm_predictions_at_epoch(
        self,
        epoch_date: datetime,
        duration: float,
        page: int,
        per_page: int,
        format: str,
        site_name: str,
        constellation: str | None = None,
    ) -> tuple[list[TdmPrediction], int, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_tdm_prediction_points(
        self,
        tdm_prediction_ids: list[int],
    ) -> list[TdmPredictionPoint]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, tdm: TdmPrediction):
        raise NotImplementedError


class SqlAlchemyTdmPredictionRepository(AbstractTdmPredictionRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session
        # Default cache TTL in seconds - can be overridden in tests
        self.cache_ttl = 10800  # 3 hours
        self.cache_enabled = True

    @staticmethod
    def _to_domain(orm_tdm, session) -> TdmPrediction | None:
        # Return None if orm_tdm is None
        if orm_tdm is None:
            return None

        # Return None or raise an exception if satellite is None
        if orm_tdm.norad_id is None:
            logger.warning(
                f"Found TdmPrediction track_id={orm_tdm.track_id} "
                f"{orm_tdm.creation_date} without a norad_id"
            )
            return None

        sat_repository = SqlAlchemySatelliteRepository(session)
        satellite = sat_repository.get_satellite_data_by_id(orm_tdm.norad_id)
        # Only convert if we have a valid satellite
        if satellite is None:
            logger.warning(
                f"Failed to convert satellite for TdmPrediction "
                f"sat_number={orm_tdm.norad_id} {orm_tdm.creation_date}"
            )
            return None

        return TdmPrediction(
            id=orm_tdm.id,
            creation_date=orm_tdm.creation_date,
            time_range_start=orm_tdm.time_range_start,
            time_range_end=orm_tdm.time_range_end,
            site_name=orm_tdm.site_name,
            reference_frame=orm_tdm.reference_frame,
            date_added=orm_tdm.date_added,
            track_id=orm_tdm.track_id,
            folder_name=orm_tdm.folder_name,
            satellite=satellite,
        )

    @staticmethod
    def _to_orm(domain_tdm) -> TdmPredictionDb:
        return TdmPredictionDb(
            creation_date=domain_tdm.creation_date,
            time_range_start=domain_tdm.time_range_start,
            time_range_end=domain_tdm.time_range_end,
            site_name=domain_tdm.site_name,
            reference_frame=domain_tdm.reference_frame,
            date_added=domain_tdm.date_added,
            track_id=domain_tdm.track_id,
            folder_name=domain_tdm.folder_name,
            norad_id=domain_tdm.satellite.sat_number,
        )

    @staticmethod
    def batch_serialize_tdm_predictions(
        tdm_predictions: list[TdmPrediction],
    ) -> list[dict[str, Any]]:
        """
        Efficiently serialize a batch of TdmPredictions for caching.

        Args:
            tdm_predictions: List of TdmPrediction objects to serialize

        Returns:
            List of serialized TdmPrediction dictionaries
        """
        result: list[dict[str, Any]] = []
        result_append = result.append

        for tdm in tdm_predictions:
            # Get satellite information once to avoid repeated attribute access
            satellite = tdm.satellite
            decay_date = satellite.decay_date

            # Create efficient TdmPrediction dictionary with direct attribute access
            tdm_prediction_dict = {
                "creation_date": tdm.creation_date.isoformat(),
                "time_range_start": tdm.time_range_start.isoformat(),
                "time_range_end": tdm.time_range_end.isoformat(),
                "site_name": tdm.site_name,
                "reference_frame": tdm.reference_frame,
                "date_added": tdm.date_added.isoformat(),
                "track_id": tdm.track_id,
                "folder_name": tdm.folder_name,
                "satellite": {
                    "sat_name": satellite.sat_name,
                    "sat_number": satellite.sat_number,
                    "decay_date": decay_date.isoformat() if decay_date else None,
                    "has_current_sat_number": getattr(
                        satellite, "has_current_sat_number", True
                    ),
                },
            }
            result_append(tdm_prediction_dict)

        return result

    @staticmethod
    def deserialize_tdm_predictions(
        serialized_tdm_predictions: list[dict[str, Any]],
    ) -> list[TdmPrediction]:
        """
        Convert serialized TdmPrediction dictionaries from the cache back into domain
        TdmPrediction objects.

        Args:
            serialized_tdm_predictions: List of serialized TdmPrediction dictionaries
            from the cache

        Returns:
            List of TdmPrediction domain objects
        """
        tdm_predictions = []

        for tdm_prediction_dict in serialized_tdm_predictions:
            try:
                # Extract satellite data and create Satellite domain object
                sat_data = tdm_prediction_dict.get("satellite", {})

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

                # Create the TdmPrediction domain object
                tdm_prediction = TdmPrediction(
                    satellite=satellite,
                    creation_date=datetime.fromisoformat(
                        tdm_prediction_dict.get("creation_date", "")
                    ),
                    time_range_start=datetime.fromisoformat(
                        tdm_prediction_dict.get("time_range_start", "")
                    ),
                    time_range_end=datetime.fromisoformat(
                        tdm_prediction_dict.get("time_range_end", "")
                    ),
                    site_name=tdm_prediction_dict.get("site_name", ""),
                    reference_frame=tdm_prediction_dict.get("reference_frame", ""),
                    date_added=datetime.fromisoformat(
                        tdm_prediction_dict.get("date_added", "")
                    ),
                    track_id=tdm_prediction_dict.get("track_id", ""),
                    folder_name=tdm_prediction_dict.get("folder_name", ""),
                )

                tdm_predictions.append(tdm_prediction)
            except Exception as e:
                logger.error(f"Error deserializing TdmPredictions: {e}")
                raise e

        return tdm_predictions

    def _add(self, tdm: TdmPrediction):
        orm_tdm = self._to_orm(tdm)

        try:
            existing_satellite = (
                self.session.query(SatelliteDb)
                .filter(
                    SatelliteDb.sat_number == tdm.satellite.sat_number,
                    SatelliteDb.sat_name == tdm.satellite.sat_name,
                )
                .one()
            )
            orm_tdm.norad_id = existing_satellite.sat_number
        except NoResultFound:
            # Satellite does not exist, so it will be added with the TdmPrediction
            pass

        self.session.add(orm_tdm)

    def _get_all_tdm_predictions_at_epoch(
        self,
        epoch_date: datetime,
        duration: float,
        page: int,
        per_page: int,
        format: str,
        site_name: str,
        constellation: str | None = None,
    ) -> tuple[list[TdmPrediction], int, str]:
        # Ensure epoch_date has a timezone if not already set
        if epoch_date.tzinfo is None:
            epoch_date = epoch_date.replace(tzinfo=timezone.utc)

        range_start = epoch_date
        range_end = epoch_date + timedelta(seconds=duration)

        total_count = 0

        logger.info(
            f"Fetching TdmPredictions for epoch {epoch_date} "
            f"(page {page}, per_page {per_page})"
        )
        start_time = time.time()

        # If we get here, we need to query the database
        logger.info("Querying database for TdmPredictions")
        try:
            # Get predictions for this site and epoch
            tdm_predictions_sql = text("""
                WITH latest_tdm_predictions AS (
                    SELECT DISTINCT ON (norad_id)
                        id, creation_date, time_range_start, time_range_end,
                        site_name, norad_id, reference_frame, track_id, folder_name,
                        date_added
                    FROM tdm_predictions
                    WHERE time_range_start <= :range_end
                    AND time_range_end >= :range_start
                    AND site_name = :site_name
                    ORDER BY norad_id, creation_date DESC
                )
                SELECT * FROM latest_tdm_predictions
                ORDER BY creation_date DESC
            """)  # noqa: E501

            # Get satellite metadata
            satellites_sql = text("""
                SELECT id, sat_name, sat_number, decay_date, has_current_sat_number,
                constellation, launch_date
                FROM satellites s
                WHERE s.launch_date <= :epoch_date
                AND (s.decay_date IS NULL OR s.decay_date > :epoch_date)
                AND sat_number IN :satellite_numbers
                AND (
                    :constellation IS NULL
                    OR (s.constellation IS NOT NULL AND s.constellation
                    ILIKE :constellation || '%')
                )
            """).bindparams(bindparam("satellite_numbers", expanding=True))

            tdm_predictions_result = self.session.execute(
                tdm_predictions_sql,
                {
                    "range_start": range_start,
                    "range_end": range_end,
                    "site_name": site_name,
                },
            )
            all_rows = list(tdm_predictions_result)
            logger.info(
                f"TDM predictions query returned {len(all_rows)} raw rows "
                f"(site={site_name!r}, range_start={range_start}, "
                f"range_end={range_end})"
            )

            rows_with_null_norad = [r for r in all_rows if r.norad_id is None]
            if rows_with_null_norad:
                logger.warning(
                    f"{len(rows_with_null_norad)} rows had NULL norad_id "
                    f"and were excluded"
                )

            satellites_with_passes = {
                row.norad_id: row for row in all_rows if row.norad_id is not None
            }
            logger.info(
                f"Unique satellites with passes in time range: "
                f"{len(satellites_with_passes)} "
                f"(norad_ids={list(satellites_with_passes.keys())[:20]})"
            )

            if not satellites_with_passes:
                logger.warning(
                    f"No TDM predictions found in database for site={site_name!r}, "
                    f"range_start={range_start}, range_end={range_end}. "
                    f"Verify that tdm_predictions rows exist with "
                    f"time_range_start <= {range_start} AND "
                    f"time_range_end >= {range_end} AND site_name = {site_name!r}"
                )
                return [], 0, "database"

            # Get satellite metadata
            satellites_result = self.session.execute(
                satellites_sql,
                {
                    "satellite_numbers": list(satellites_with_passes.keys()),
                    "constellation": constellation,
                    "epoch_date": epoch_date,
                },
            )
            satellites_result_data = {row.sat_number: row for row in satellites_result}

            logger.info(
                f"Satellite metadata query returned {len(satellites_result_data)} rows "
                f"(constellation filter={constellation!r})"
            )
            if len(satellites_result_data) < len(satellites_with_passes):
                missing = set(satellites_with_passes.keys()) - set(
                    satellites_result_data.keys()
                )
                logger.warning(
                    f"{len(missing)} norad_ids from TDM predictions had no matching "
                    f"satellite metadata (or filtered by constellation/launch/decay): "
                    f"missing={list(missing)[:20]}"
                )

            # Map results to domain objects (iterate over all_rows since
            # tdm_predictions_result cursor is already consumed above)
            tdm_predictions = []
            for row in all_rows:
                if row.norad_id is None:
                    continue
                # serves as the constellation filter for now, if the constellation
                # didn't match in the satellites result, it should not be in
                # the end result
                if row.norad_id not in satellites_result_data.keys():
                    continue

                sat_data = satellites_result_data[row.norad_id]
                satellite = Satellite(
                    sat_name=sat_data.sat_name,
                    sat_number=sat_data.sat_number,
                    launch_date=sat_data.launch_date,
                    decay_date=sat_data.decay_date,
                    has_current_sat_number=sat_data.has_current_sat_number,
                    constellation=sat_data.constellation,
                )

                tdm_prediction = TdmPrediction(
                    id=row.id,
                    satellite=satellite,
                    creation_date=row.creation_date,
                    time_range_start=row.time_range_start,
                    time_range_end=row.time_range_end,
                    site_name=row.site_name,
                    reference_frame=row.reference_frame,
                    date_added=row.date_added,
                    track_id=row.track_id,
                    folder_name=row.folder_name,
                )
                tdm_predictions.append(tdm_prediction)

            # Handle pagination
            total_count = len(tdm_predictions)
            logger.info(
                f"Built {total_count} TdmPrediction domain objects after "
                f"satellite metadata join"
            )
            if format != "zip":
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page
                tdm_predictions = tdm_predictions[start_idx:end_idx]
                logger.info(
                    f"Pagination: returning {len(tdm_predictions)} TdmPredictions "
                    f"out of {total_count} total"
                )

            execution_time = time.time() - start_time
            logger.info(f"Database query completed in {execution_time:.2f} seconds")
            return tdm_predictions, total_count, "database"

        except Exception as e:
            logger.error(f"Error getting TdmPredictions: {e}")
            self.session.rollback()
            logger.error("Database query failed, rolling back transaction")
            raise

    def _get_tdm_prediction_points(
        self,
        tdm_prediction_ids: list[int],
    ) -> list[TdmPredictionPoint]:
        logger.info(f"Fetching prediction points " f"for {len(tdm_prediction_ids)}.")

        if not tdm_prediction_ids:
            return []

        try:
            points_sql = text("""
                SELECT
                    prediction_points.tdm_prediction_id,
                    prediction_points.timestamp,
                    prediction_points.right_ascension,
                    prediction_points.declination,
                    prediction_points.apparent_magnitude,
                    predictions.norad_id AS satellite_number,
                    COALESCE(satellites.sat_name, '') AS satellite_name
                FROM tdm_prediction_points prediction_points
                JOIN tdm_predictions predictions
                    ON predictions.id = prediction_points.tdm_prediction_id
                LEFT JOIN satellites satellites
                    ON satellites.sat_number = predictions.norad_id
                    AND satellites.has_current_sat_number
                WHERE prediction_points.tdm_prediction_id IN :tdm_prediction_ids
            """).bindparams(bindparam("tdm_prediction_ids", expanding=True))
            result = self.session.execute(
                points_sql,
                {"tdm_prediction_ids": tdm_prediction_ids},
            )
            return [
                TdmPredictionPoint(
                    tdm_prediction_id=row.tdm_prediction_id,
                    timestamp=row.timestamp,
                    right_ascension=row.right_ascension,
                    declination=row.declination,
                    apparent_magnitude=row.apparent_magnitude,
                    satellite_number=row.satellite_number,
                    satellite_name=row.satellite_name,
                )
                for row in result
            ]

        except Exception as e:
            logger.error(f"Error getting TdmPredictionPoints: {e}")
            self.session.rollback()
            logger.error("Database query failed, rolling back transaction")
            raise
