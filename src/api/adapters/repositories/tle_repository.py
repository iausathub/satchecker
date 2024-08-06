import abc
from datetime import datetime

from sqlalchemy import and_, func
from sqlalchemy.orm.exc import NoResultFound

from src.api.adapters.database_orm import SatelliteDb, TLEDb
from src.api.adapters.repositories.satellite_repository import (
    SqlAlchemySatelliteRepository,
)
from src.api.domain.models.satellite import Satellite as Satellite
from src.api.domain.models.tle import TLE


class AbstractTLERepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, tle: TLE):
        self._add(tle)
        self.seen.add(tle)

    def get_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> TLE:
        satellite = self._get_by_satellite_number(satellite_number, epoch, data_source)
        if satellite:
            self.seen.add(satellite)
        return satellite

    def get_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> TLE:
        satellite = self._get_by_satellite_name(satellite_name, epoch, data_source)
        if satellite:
            self.seen.add(satellite)
        return satellite

    @abc.abstractmethod
    def _get_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> TLE:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> TLE:
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

    def _get_by_satellite_number(
        self, satellite_number: str, epoch: datetime, data_source: str
    ) -> TLE:
        return (
            self.session.query(TLEDb)
            .join(TLEDb.satellite)
            .filter(
                and_(
                    SatelliteDb.sat_number == satellite_number,
                    TLEDb.data_source == data_source,
                )
            )
            .order_by(
                func.abs(
                    func.extract("epoch", TLEDb.epoch) - func.extract("epoch", epoch)
                )
            )
            .first()
        )

    def _get_by_satellite_name(
        self, satellite_name: str, epoch: datetime, data_source: str
    ) -> TLE:
        return (
            self.session.query(TLEDb)
            .join(TLEDb.satellite)
            .filter(
                and_(
                    SatelliteDb.sat_name == satellite_name,
                    TLEDb.data_source == data_source,
                )
            )
            .order_by(
                func.abs(
                    func.extract("epoch", TLEDb.epoch) - func.extract("epoch", epoch)
                )
            )
            .first()
        )

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
