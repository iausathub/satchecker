import abc
from datetime import datetime
from typing import Optional

from sqlalchemy import and_, func, or_
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

    def get_most_recent_full_tle_set(self):
        return self._get_most_recent_full_tle_set()

    def get_all_tles_at_epoch(
        self, epoch_date: datetime, page: int, per_page: int
    ) -> list[TLE]:
        return self._get_all_tles_at_epoch(epoch_date, page, per_page)

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
    def _get_most_recent_full_tle_set(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_tles_at_epoch(
        self, epoch_date: datetime, page: int, per_page: int
    ) -> list[TLE]:
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
                    func.extract("epoch", TLEDb.epoch) - func.extract("epoch", epoch)
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
                    func.extract("epoch", TLEDb.epoch) - func.extract("epoch", epoch)
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

    def _get_most_recent_full_tle_set(self):
        # get all satellites that have has_current_sat_number = True
        subquery = (
            self.session.query(SatelliteDb.sat_number)
            .filter(SatelliteDb.has_current_sat_number == True)  # noqa: E712
            .subquery()
        )

        # get only most recent TLE for each satellite in the subquery
        query = (
            self.session.query(TLEDb)
            .join(TLEDb.satellite)
            .filter(SatelliteDb.sat_number.in_(subquery))
            .order_by(SatelliteDb.sat_number, TLEDb.epoch.desc())
            .distinct(SatelliteDb.sat_number)
        )

        return query.all()

    def _get_all_tles_at_epoch(
        self, epoch_date: datetime, page: int, per_page: int
    ) -> list[TLE]:
        subquery = (
            self.session.query(
                TLEDb.sat_id,
                func.max(TLEDb.epoch).label("max_epoch")
            )
            .filter(TLEDb.epoch <= epoch_date)
            .group_by(TLEDb.sat_id)
            .subquery()
        )

        query = (
            self.session.query(TLEDb)
            .join(subquery, and_(
                TLEDb.sat_id == subquery.c.sat_id,
                TLEDb.epoch == subquery.c.max_epoch
            ))
            .join(TLEDb.satellite)
            .filter(SatelliteDb.has_current_sat_number == True)  # noqa: E712
            .order_by(TLEDb.epoch)
        )

        paginated_query = query.limit(per_page).offset((page - 1) * per_page)
        return paginated_query.all()

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
