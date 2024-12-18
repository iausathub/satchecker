import abc
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import DateTime, and_, func, or_
from sqlalchemy.orm.exc import NoResultFound

from api.adapters.database_orm import SatelliteDb, TLEDb
from api.adapters.repositories.satellite_repository import SqlAlchemySatelliteRepository
from api.domain.models.satellite import Satellite as Satellite
from api.domain.models.tle import TLE


class AbstractTLERepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, tle: TLE):
        self._add(tle)
        self.seen.add(tle)

    def get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> TLE:
        satellite = self._get_closest_by_satellite_number(
            satellite_number, epoch, data_source
        )
        if satellite:
            self.seen.add(satellite)
        return satellite

    def get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> TLE:
        satellite = self._get_closest_by_satellite_name(
            satellite_name, epoch, data_source
        )
        if satellite:
            self.seen.add(satellite)
        return satellite

    def get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> TLE:
        return self._get_all_for_date_range_by_satellite_number(
            satellite_number, start_date, end_date
        )

    def get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> TLE:
        return self._get_all_for_date_range_by_satellite_name(
            satellite_name, start_date, end_date
        )

    def get_all_tles_at_epoch(
        self, epoch_date: datetime, page: int, per_page: int, format: str
    ) -> tuple[list[TLE], int]:
        return self._get_all_tles_at_epoch(epoch_date, page, per_page, format)

    @abc.abstractmethod
    def _get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> TLE:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_closest_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> TLE:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> TLE:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> TLE:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_tles_at_epoch(self, epoch_date, page, per_page, format):
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, satellite: TLE):
        raise NotImplementedError


class SqlAlchemyTLERepository(AbstractTLERepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    @staticmethod
    def _to_domain(orm_tle):
        return TLE(
            date_collected=orm_tle.date_collected,
            tle_line1=orm_tle.tle_line1,
            tle_line2=orm_tle.tle_line2,
            epoch=orm_tle.epoch,
            is_supplemental=orm_tle.is_supplemental,
            data_source=orm_tle.data_source,
            satellite=SqlAlchemySatelliteRepository._to_domain(orm_tle.satellite),
        )

    @staticmethod
    def _to_orm(domain_tle):
        return TLEDb(
            date_collected=domain_tle.date_collected,
            tle_line1=domain_tle.tle_line1,
            tle_line2=domain_tle.tle_line2,
            epoch=domain_tle.epoch,
            is_supplemental=domain_tle.is_supplemental,
            data_source=domain_tle.data_source,
            satellite=SqlAlchemySatelliteRepository._to_orm(domain_tle.satellite),
        )

    def _get_closest_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> TLE:
        return (
            (
                self.session.query(TLEDb)
                .join(TLEDb.satellite)
                .filter(
                    and_(
                        SatelliteDb.sat_number == satellite_number,
                        or_(TLEDb.data_source == data_source, data_source == "any"),
                    )
                )
            )
            .order_by(
                func.abs(
                    func.extract("epoch", TLEDb.epoch)
                    - func.extract("epoch", func.cast(epoch, DateTime(timezone=True)))
                )
            )
            .first()
        )

    def _get_closest_by_satellite_name(
        self,
        satellite_name: str,
        epoch: datetime,
        data_source: str,
    ) -> TLE:
        return (
            (
                self.session.query(TLEDb)
                .join(TLEDb.satellite)
                .filter(
                    and_(
                        SatelliteDb.sat_name == satellite_name,
                        or_(TLEDb.data_source == data_source, data_source == "any"),
                    )
                )
            )
            .order_by(
                func.abs(
                    func.extract("epoch", TLEDb.epoch)
                    - func.extract("epoch", func.cast(epoch, DateTime(timezone=True)))
                )
            )
            .first()
        )

    def _get_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> TLE:
        query = (
            self.session.query(TLEDb)
            .join(TLEDb.satellite)
            .filter(SatelliteDb.sat_number == satellite_number)
        )

        if start_date is not None:
            query = query.filter(TLEDb.epoch >= start_date)

        if end_date is not None:
            query = query.filter(TLEDb.epoch <= end_date)

        return query.all()

    def _get_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> TLE:
        query = (
            self.session.query(TLEDb)
            .join(TLEDb.satellite)
            .filter(SatelliteDb.sat_name == satellite_name)
        )
        if start_date is not None:
            query = query.filter(TLEDb.epoch >= start_date)

        if end_date is not None:
            query = query.filter(TLEDb.epoch <= end_date)

        return query.all()

    def _get_all_tles_at_epoch(
        self, epoch_date: datetime, page: int, per_page: int, format: str
    ) -> tuple[list[TLE], int]:
        two_weeks_prior = epoch_date - timedelta(weeks=2)

        # Fast count query
        count_sql = """
        SELECT COUNT(DISTINCT t.sat_id)
        FROM tle_partitioned t
        JOIN satellites s ON t.sat_id = s.id
        WHERE t.epoch BETWEEN :start_date AND :end_date
        AND (s.decay_date IS NULL OR s.decay_date > :epoch_date)
        AND NOT (t.epoch < :start_date AND s.sat_name = 'TBA - TO BE ASSIGNED')
        """

        total_count = self.session.execute(
            count_sql,
            {
                "start_date": two_weeks_prior,
                "end_date": epoch_date,
                "epoch_date": epoch_date,
            },
        ).scalar()

        # Main data query with all needed fields
        data_sql = """
        WITH latest_tles AS (
            SELECT t.*, s.sat_name, s.sat_number, s.decay_date, s.has_current_sat_number,
                   ROW_NUMBER() OVER (PARTITION BY t.sat_id ORDER BY t.epoch DESC) as rn
            FROM tle_partitioned t
            JOIN satellites s ON t.sat_id = s.id
            WHERE t.epoch BETWEEN :start_date AND :end_date
            AND (s.decay_date IS NULL OR s.decay_date > :epoch_date)
            AND NOT (t.epoch < :start_date AND s.sat_name = 'TBA - TO BE ASSIGNED')
        )
        SELECT id, sat_id, date_collected, tle_line1, tle_line2, epoch,
               is_supplemental, data_source, sat_name, sat_number,
               decay_date, has_current_sat_number
        FROM latest_tles
        WHERE rn = 1
        ORDER BY epoch DESC
        """  # noqa: E501

        if format != "zip":
            data_sql += " LIMIT :limit OFFSET :offset"
            params = {
                "start_date": two_weeks_prior,
                "end_date": epoch_date,
                "epoch_date": epoch_date,
                "limit": per_page,
                "offset": (page - 1) * per_page,
            }
        else:
            params = {
                "start_date": two_weeks_prior,
                "end_date": epoch_date,
                "epoch_date": epoch_date,
            }

        rows = self.session.execute(data_sql, params).fetchall()

        # Map results to domain objects
        tles = []
        for row in rows:
            satellite = Satellite(
                sat_name=row.sat_name,
                sat_number=row.sat_number,
                decay_date=row.decay_date,
                has_current_sat_number=row.has_current_sat_number,
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

        return tles, total_count

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
