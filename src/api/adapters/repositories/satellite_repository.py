import abc
from datetime import datetime
from typing import Optional

from sqlalchemy import func

from api.adapters.database_orm import SatelliteDb, SatelliteDesignationDb
from api.domain.models.satellite import Satellite
from api.domain.models.satellite_designation import SatelliteDesignation


class AbstractSatelliteRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, satellite: Satellite):
        self._add(satellite)
        self.seen.add(satellite)

    def get(self, satellite_id: str) -> Optional[Satellite]:
        satellite = self._get(satellite_id)
        if satellite:
            self.seen.add(satellite)
        return satellite

    def get_norad_ids_from_satellite_name(self, name):
        return self._get_norad_ids_from_satellite_name(name)

    def get_satellite_names_from_norad_id(self, id):
        return self._get_satellite_names_from_norad_id(id)

    def get_satellite_data_by_id(self, id):
        return self._get_satellite_data_by_id(id)

    def get_satellite_data_by_name(self, name):
        return self._get_satellite_data_by_name(name)

    def get_starlink_generations(self):
        return self._get_starlink_generations()

    def get_active_satellites(self, object_type: Optional[str] = None):
        return self._get_active_satellites(object_type)

    @abc.abstractmethod
    def _get(self, satellite_id: str) -> Optional[Satellite]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_norad_ids_from_satellite_name(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_satellite_names_from_norad_id(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_satellite_data_by_id(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_satellite_data_by_name(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, satellite: Satellite):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_starlink_generations(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_active_satellites(self, object_type: Optional[str] = None):
        raise NotImplementedError


class SqlAlchemySatelliteRepository(AbstractSatelliteRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _get(self, satellite_id: str) -> Optional[Satellite]:
        orm_satellite = (
            self.session.query(SatelliteDb)
            .join(SatelliteDesignationDb)
            .filter(SatelliteDesignationDb.sat_number == satellite_id)
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
        satellite_numbers_and_dates = (
            self.session.query(
                SatelliteDesignationDb.sat_number,
                SatelliteDesignationDb.date_added,
                SatelliteDesignationDb.valid_from,
                SatelliteDesignationDb.valid_to,
            )
            .filter(
                SatelliteDesignationDb.sat_name == name,
            )
            .order_by(SatelliteDesignationDb.date_added.desc())
            .all()
        )

        return satellite_numbers_and_dates

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
                SatelliteDesignationDb.sat_name,
                SatelliteDesignationDb.date_added,
                SatelliteDesignationDb.valid_from,
                SatelliteDesignationDb.valid_to,
            )
            .filter(
                SatelliteDesignationDb.sat_number == id,
            )
            .order_by(SatelliteDesignationDb.date_added.desc())
            .all()
        )

        return satellite_names_and_dates

    def _get_satellite_data_by_id(self, id, epoch: Optional[datetime] = None):
        """
        Retrieves satellite data (rcs_size, launch date, etc. ) for a given NORAD ID.

        This method queries the database to find a satellite with the specified
        NORAD ID that also has the current satellite number.

        Args:
            id (int): The NORAD ID of the satellite.
            epoch (datetime): The date/time to check designation validity against.
                             If None, gets the currently active designation.

        Returns:
            Satellite: The satellite data if found, otherwise None.
        """
        query = (
            self.session.query(SatelliteDb)
            .join(SatelliteDesignationDb)
            .filter(SatelliteDesignationDb.sat_number == id)
        )

        if epoch is not None:
            query = query.filter(
                SatelliteDesignationDb.valid_from <= epoch,
                (
                    SatelliteDesignationDb.valid_to.is_(None)
                    | (SatelliteDesignationDb.valid_to > epoch)
                ),
            )
        else:
            # If epoch is None, get the currently active designation
            current_time = datetime.now()
            query = query.filter(
                SatelliteDesignationDb.valid_from <= current_time,
                (
                    SatelliteDesignationDb.valid_to.is_(None)
                    | (SatelliteDesignationDb.valid_to > current_time)
                ),
            )

        data = query.first()
        return self._to_domain(data)

    def _get_satellite_data_by_name(self, name, epoch: Optional[datetime] = None):
        """
        Retrieves satellite data (rcs_size, launch date, etc. ) for a given satellite
        name.

        This method queries the database to find a satellite with the specified
        name that also has the current satellite number.

        Args:
            name (str): The name of the satellite.
            epoch (datetime): The date/time to check designation validity against.
                             If None, gets the currently active designation.

        Returns:
            Satellite: The satellite data if found, otherwise None.
        """
        query = (
            self.session.query(SatelliteDb)
            .join(SatelliteDesignationDb)
            .filter(SatelliteDesignationDb.sat_name == name)
        )

        if epoch is not None:
            query = query.filter(
                SatelliteDesignationDb.valid_from <= epoch,
                (
                    SatelliteDesignationDb.valid_to.is_(None)
                    | (SatelliteDesignationDb.valid_to > epoch)
                ),
            )
        else:
            # If epoch is None, get the currently active designation
            current_time = datetime.now()
            query = query.filter(
                SatelliteDesignationDb.valid_from <= current_time,
                (
                    SatelliteDesignationDb.valid_to.is_(None)
                    | (SatelliteDesignationDb.valid_to > current_time)
                ),
            )

        satellite = query.first()
        return self._to_domain(satellite)

    def _get_starlink_generations(self):
        """
        Retrieves unique Starlink generations with their earliest and most recent
        launch dates.

        Args:
            None

        Returns:
            List[tuple]: A list of tuples containing (generation, earliest_launch_date,
            latest_launch_date)
        """
        query = (
            self.session.query(
                SatelliteDb.generation,
                func.min(SatelliteDb.launch_date).label("earliest_launch"),
                func.max(SatelliteDb.launch_date).label("latest_launch"),
            )
            .join(SatelliteDesignationDb)
            .filter(
                func.lower(SatelliteDesignationDb.sat_name).like("%starlink%"),
                SatelliteDb.generation.isnot(None),
            )
            .group_by(SatelliteDb.generation)
            .order_by(SatelliteDb.generation)
        )

        return query.all()

    def _get_active_satellites(self, object_type: Optional[str] = None):
        """
        Retrieves active satellites based on the provided object type (optional).
        Returns satellites that are active (no decay date) with all their designations
        (both historical and current).

        Args:
            object_type (str): The type of the object, either "payload", "debris",
            "rocket body", "tba", or "unknown".

        Returns:
            List[Satellite]: A list of active satellites with all their designations.
        """
        query = (
            self.session.query(SatelliteDb)
            .join(SatelliteDesignationDb)
            .filter(SatelliteDb.decay_date.is_(None))
        )

        if object_type:
            query = query.filter(
                func.lower(SatelliteDb.object_type) == func.lower(object_type)
            )

        satellite_results = query.all()

        satellites = []
        for satellite_result in satellite_results:
            satellites.append(self._to_domain(satellite_result))

        return satellites

    def _add(self, satellite: Satellite):
        orm_satellite = self._to_orm(satellite)
        self.session.add(orm_satellite)

    # SQLAlchemyRepository-specific methods
    @staticmethod
    def _designation_to_domain(orm_designation) -> SatelliteDesignation:
        return SatelliteDesignation(
            sat_name=orm_designation.sat_name,
            sat_number=orm_designation.sat_number,
            valid_from=orm_designation.valid_from,
            valid_to=orm_designation.valid_to,
        )

    @staticmethod
    def _designation_to_orm(domain_designation):
        return SatelliteDesignationDb(
            sat_name=domain_designation.sat_name,
            sat_number=domain_designation.sat_number,
            valid_from=domain_designation.valid_from,
            valid_to=domain_designation.valid_to,
        )

    @staticmethod
    def _to_domain(orm_satellite) -> Optional[Satellite]:
        if orm_satellite is None:
            return None

        # Convert designations from ORM to domain
        designations = [
            SqlAlchemySatelliteRepository._designation_to_domain(orm_designation)
            for orm_designation in orm_satellite.designations
        ]

        return Satellite(
            constellation=orm_satellite.constellation,
            generation=orm_satellite.generation,
            rcs_size=orm_satellite.rcs_size,
            launch_date=orm_satellite.launch_date,
            decay_date=orm_satellite.decay_date,
            object_id=orm_satellite.object_id,
            object_type=orm_satellite.object_type,
            designations=designations,
        )

    @staticmethod
    def _to_orm(domain_satellite):
        if domain_satellite is None:
            return None

        # Convert designations from domain to ORM
        designations = [
            SqlAlchemySatelliteRepository._designation_to_orm(designation)
            for designation in domain_satellite.designations
        ]
        return SatelliteDb(
            constellation=domain_satellite.constellation,
            generation=domain_satellite.generation,
            rcs_size=domain_satellite.rcs_size,
            launch_date=domain_satellite.launch_date,
            decay_date=domain_satellite.decay_date,
            object_id=domain_satellite.object_id,
            object_type=domain_satellite.object_type,
            designations=designations,
        )
