import abc

from src.api.adapters.database_orm import SatelliteDb
from src.api.domain.models.satellite import Satellite


class AbstractSatelliteRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, satellite: Satellite):
        self._add(satellite)
        self.seen.add(satellite)

    def get(self, satellite_id: str) -> Satellite:
        satellite = self._get(satellite_id)
        if satellite:
            self.seen.add(satellite)
        return satellite

    @abc.abstractmethod
    def _get(self, satellite_id: str) -> Satellite:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, satellite: Satellite):
        raise NotImplementedError


class SqlAlchemySatelliteRepository(AbstractSatelliteRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _get(self, satellite_id: str) -> Satellite:
        orm_satellite = (
            self.session.query(SatelliteDb)
            .filter(SatelliteDb.sat_number == satellite_id)
            .first()
        )  # noqa: E501
        return self._to_domain(orm_satellite)

    def _add(self, satellite: Satellite):
        orm_satellite = self._to_orm(satellite)
        self.session.add(orm_satellite)

    @staticmethod
    def _to_domain(orm_satellite):
        if orm_satellite is None:
            return None
        return Satellite(
            sat_number=orm_satellite.sat_number,
            sat_name=orm_satellite.sat_name,
            constellation=orm_satellite.constellation,
            rcs_size=orm_satellite.rcs_size,
            launch_date=orm_satellite.launch_date,
            decay_date=orm_satellite.decay_date,
            object_id=orm_satellite.object_id,
            object_type=orm_satellite.object_type,
            has_current_sat_number=orm_satellite.has_current_sat_number,
        )

    @staticmethod
    def _to_orm(domain_satellite):
        return SatelliteDb(
            sat_number=domain_satellite.sat_number,
            sat_name=domain_satellite.sat_name,
            constellation=domain_satellite.constellation,
            rcs_size=domain_satellite.rcs_size,
            launch_date=domain_satellite.launch_date,
            decay_date=domain_satellite.decay_date,
            object_id=domain_satellite.object_id,
            object_type=domain_satellite.object_type,
            has_current_sat_number=domain_satellite.has_current_sat_number,
        )
