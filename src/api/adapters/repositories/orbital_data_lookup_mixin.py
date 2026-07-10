from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, and_, bindparam, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from api.adapters.database_orm import SatelliteDb
from api.utils.time_utils import ensure_datetime


class OrbitalDataLookupMixin:
    """
    Shared epoch-based DB lookups for tables with (sat_id, epoch, data_source)
    joined to satellites. Used by TLE and orbital elements repositories.

    Subclasses must define session, _orm_model, _to_domain, and _to_orm.
    """

    session: Session
    _orm_model: type

    def _lookup_closest_by_satellite_number(
        self,
        satellite_number: str,
        epoch: datetime,
        data_source: str,
    ) -> Any | None:
        """Return the record whose epoch is closest to the given epoch, by NORAD ID."""
        model = self._orm_model

        filter_conditions = [SatelliteDb.sat_number == satellite_number]
        if data_source != "any":
            filter_conditions.append(model.data_source == data_source)

        epoch = ensure_datetime(epoch)
        epoch_param = bindparam("epoch", epoch, type_=DateTime(timezone=True))

        result = (
            self.session.query(model)
            .join(model.satellite)
            .filter(and_(*filter_conditions))
            .order_by(
                func.abs(
                    func.extract("epoch", model.epoch)
                    - func.extract("epoch", epoch_param)
                )
            )
            .first()
        )

        if result is None:
            return None

        return self._to_domain(result)

    def _lookup_closest_by_satellite_name(
        self,
        satellite_name: str,
        epoch: datetime,
        data_source: str,
    ) -> Any | None:
        """Return the record whose epoch is closest to the given epoch, by name."""
        model = self._orm_model

        filter_conditions = [SatelliteDb.sat_name == satellite_name]
        if data_source != "any":
            filter_conditions.append(model.data_source == data_source)

        # Ensure epoch is a datetime object with timezone info
        epoch = ensure_datetime(epoch)
        epoch_param = bindparam("epoch", epoch, type_=DateTime(timezone=True))

        result = (
            self.session.query(model)
            .join(model.satellite)
            .filter(and_(*filter_conditions))
            .order_by(
                func.abs(
                    func.extract("epoch", model.epoch)
                    - func.extract("epoch", epoch_param)
                )
            )
            .first()
        )

        if result is None:
            return None

        return self._to_domain(result)

    def _lookup_all_for_date_range_by_satellite_number(
        self,
        satellite_number: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[Any]:
        """Return all records for a NORAD ID within an optional date range."""
        model = self._orm_model

        query = (
            self.session.query(model)
            .join(model.satellite)
            .filter(SatelliteDb.sat_number == satellite_number)
        )

        if start_date is not None:
            query = query.filter(model.epoch >= start_date)

        if end_date is not None:
            query = query.filter(model.epoch <= end_date)

        results = query.all()
        # Filter out any None values that may result from _to_domain
        return [
            orbital_data
            for orbital_data in (self._to_domain(result) for result in results)
            if orbital_data is not None
        ]

    def _lookup_all_for_date_range_by_satellite_name(
        self,
        satellite_name: str,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[Any]:
        """Return all records for a satellite name within an optional date range."""
        model = self._orm_model

        query = (
            self.session.query(model)
            .join(model.satellite)
            .filter(SatelliteDb.sat_name == satellite_name)
        )
        if start_date is not None:
            query = query.filter(model.epoch >= start_date)

        if end_date is not None:
            query = query.filter(model.epoch <= end_date)

        results = query.all()
        # Filter out any None values that may result from _to_domain
        return [
            orbital_data
            for orbital_data in (self._to_domain(result) for result in results)
            if orbital_data is not None
        ]

    def _lookup_nearest_at_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
    ) -> Any | None:
        """Return the record closest to epoch for the given catalog number or name."""
        model = self._orm_model

        try:
            if epoch.tzinfo is None:
                epoch = epoch.replace(tzinfo=timezone.utc)

            nearest_sat_id = self._lookup_correct_satellite_id_at_epoch(
                id, id_type, epoch
            )
            if nearest_sat_id is None:
                return None

            epoch = ensure_datetime(epoch)
            epoch_param = bindparam("epoch", epoch, type_=DateTime(timezone=True))

            nearest = (
                self.session.query(model)
                .filter(model.sat_id == nearest_sat_id)
                .order_by(
                    func.abs(
                        func.extract("epoch", model.epoch)
                        - func.extract("epoch", epoch_param)
                    )
                )
                .first()
            )

            if nearest is None:
                return None

            return self._to_domain(nearest)

        except NoResultFound:
            return None

        except Exception:
            self.session.rollback()
            raise

    def _lookup_adjacent_at_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
    ) -> list[Any]:
        """Return the records immediately before and after the given epoch."""
        model = self._orm_model

        if epoch.tzinfo is None:
            epoch = epoch.replace(tzinfo=timezone.utc)

        try:
            # Get all satellites with the same catalog number.
            # This is because there are often multiple satellite names
            # associated with the same catalog number, and until the
            # database is updated to have a satellite name history, we
            # need to see which one has the orbital data that is closest to the
            # specified epoch.
            nearest_sat_id = self._lookup_correct_satellite_id_at_epoch(
                id, id_type, epoch
            )
            if nearest_sat_id is None:
                return []

            # Get the orbital data before the specified epoch
            before_orbital_data = (
                self.session.query(model)
                .filter(model.sat_id == nearest_sat_id, model.epoch < epoch)
                .order_by(model.epoch.desc())
                .first()
            )

            # Get the orbital data after the specified epoch
            after_orbital_data = (
                self.session.query(model)
                .filter(model.sat_id == nearest_sat_id, model.epoch > epoch)
                .order_by(model.epoch.asc())
                .first()
            )

            # Convert to domain objects if they exist
            result = []
            if before_orbital_data:
                domain_before = self._to_domain(before_orbital_data)
                if domain_before is not None:
                    result.append(domain_before)

            if after_orbital_data:
                domain_after = self._to_domain(after_orbital_data)
                if domain_after is not None:
                    result.append(domain_after)

            return result

        except NoResultFound:
            return []

        except Exception:
            self.session.rollback()
            raise

    def _lookup_records_around_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
        count_before: int,
        count_after: int,
    ) -> list[Any]:
        """Return count_before records before epoch and count_after records after."""
        model = self._orm_model

        try:
            nearest_sat_id = self._lookup_correct_satellite_id_at_epoch(
                id, id_type, epoch
            )
            if nearest_sat_id is None:
                return []

            # Get the orbital data before the specified epoch
            before_orbital_data = (
                self.session.query(model)
                .filter(model.sat_id == nearest_sat_id, model.epoch < epoch)
                .order_by(model.epoch.desc())
                .limit(count_before)
                .all()
            )

            # Get the orbital data after the specified epoch
            after_orbital_data = (
                self.session.query(model)
                .filter(model.sat_id == nearest_sat_id, model.epoch > epoch)
                .order_by(model.epoch.asc())
                .limit(count_after)
                .all()
            )

            # Convert to domain objects
            result = []
            for orbital_data in before_orbital_data:
                domain_orbital_data = self._to_domain(orbital_data)
                if domain_orbital_data is not None:
                    result.append(domain_orbital_data)

            for orbital_data in after_orbital_data:
                domain_orbital_data = self._to_domain(orbital_data)
                if domain_orbital_data is not None:
                    result.append(domain_orbital_data)

            return result
        except NoResultFound:
            return []

        except Exception:
            self.session.rollback()
            raise

    def _lookup_correct_satellite_id_at_epoch(
        self,
        id: str,
        id_type: str,
        epoch: datetime,
    ) -> int | None:
        """
        When multiple satellites share an identifier, return the sat_id whose
        record is closest to the given epoch.
        """
        model = self._orm_model

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

        # get the closest TLE/orbital elements set for each satellite
        closest_orbital_data = []
        for sat in satellites_with_this_identifier:
            closest_orbital_data.append(
                self.session.query(model)
                .filter(model.sat_id == sat.id)
                .order_by(
                    func.abs(
                        func.extract("epoch", model.epoch)
                        - func.extract("epoch", epoch_param)
                    )
                )
                .first()
            )

        # filter out satellites that have no TLEs in the database
        closest_orbital_data = [
            orbital_data
            for orbital_data in closest_orbital_data
            if orbital_data is not None
        ]
        if not closest_orbital_data:
            return None

        # get the TLE/orbital elements set with the epoch closest to the specified epoch
        nearest_orbital_data = min(
            closest_orbital_data,
            key=lambda orbital_data: abs(orbital_data.epoch - epoch),
        )

        nearest_sat_id = int(
            nearest_orbital_data.sat_id
        )  # Explicitly cast to int for type checker

        return nearest_sat_id

    def _lookup_add_record(self, domain: Any) -> None:
        """Persist a domain record, reusing an existing SatelliteDb row if found."""
        orm_record = self._to_orm(domain)

        try:
            existing_satellite = (
                self.session.query(SatelliteDb)
                .filter(
                    SatelliteDb.sat_number == domain.satellite.sat_number,
                    SatelliteDb.sat_name == domain.satellite.sat_name,
                )
                .one()
            )
            orm_record.satellite = existing_satellite
        except NoResultFound:
            # Satellite does not exist, so it will be added with the record
            pass

        self.session.add(orm_record)
