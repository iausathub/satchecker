import abc

from api.adapters.database_orm import SatelliteDb
from api.domain.models.satellite import Satellite


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

    def get_norad_ids_from_satellite_name(self, name):
        return self._get_norad_ids_from_satellite_name(name)

    def get_satellite_names_from_norad_id(self, id):
        return self._get_satellite_names_from_norad_id(id)

    @abc.abstractmethod
    def _get(self, satellite_id: str) -> Satellite:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_norad_ids_from_satellite_name(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_satellite_names_from_norad_id(self, id):
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

    def _get_norad_ids_from_satellite_name(self, name):
        """
        Retrieves the NORAD IDs and the date the satellite was added to SatChecker
        for a given satellite name.

        Args:
            name (str): The name of the satellite.

        Returns:
            list of tuple: A list of tuples, each containing the NORAD ID, date added,
            and a boolean indicating if it has the current satellite number.
        """
        satellite_names_and_dates = (
            self.session.query(
                SatelliteDb.sat_number,
                SatelliteDb.date_added,
                SatelliteDb.has_current_sat_number,
            )
            .filter(
                SatelliteDb.sat_name == name,
            )
            .order_by(SatelliteDb.date_added.desc())
            .all()
        )

        return satellite_names_and_dates

    def _get_satellite_names_from_norad_id(self, id):
        """
        Retrieves the names and dates of satellites associated with a given NORAD ID.

        Args:
            id (int): The NORAD ID of the satellite.

        Returns:
            list of tuple: A list of tuples, each containing the satellite name, date
            added, and a boolean indicating if it has the current satellite number.
        """
        satellite_names_and_dates = (
            self.session.query(
                SatelliteDb.sat_name,
                SatelliteDb.date_added,
                SatelliteDb.has_current_sat_number,
            )
            .filter(
                SatelliteDb.sat_number == id,
            )
            .order_by(SatelliteDb.date_added.desc())
            .all()
        )

        return satellite_names_and_dates

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