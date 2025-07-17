from __future__ import annotations

from datetime import datetime

from api.utils.time_utils import ensure_datetime

from .satellite_designation import SatelliteDesignation


class Satellite:
    def __init__(
        self,
        constellation: str | None = None,
        generation: str | None = None,
        rcs_size: str | None = None,
        launch_date: datetime | None = None,
        decay_date: datetime | None = None,
        object_id: str | None = None,
        object_type: str | None = None,
        designations: list[SatelliteDesignation] | None = None,
    ):
        self.constellation = constellation
        self.generation = generation
        self.rcs_size = rcs_size
        self.launch_date = launch_date
        self.decay_date = decay_date
        self.object_id = object_id
        self.object_type = object_type
        self.designations = designations or []

    def add_designation(self, designation: SatelliteDesignation) -> None:
        """Add a designation to this satellite."""
        self.designations.append(designation)

    def get_current_designation(self) -> SatelliteDesignation | None:
        """Get the currently active designation (where valid_to is None)."""
        for designation in self.designations:
            if designation.valid_to is None:
                return designation
        return None

    def get_designation_at_date(self, date: datetime) -> SatelliteDesignation | None:
        """Get the designation that was active at a specific date."""
        # Ensure all datetime objects have timezone info for proper comparison
        date = ensure_datetime(date)

        for designation in self.designations:
            valid_from = ensure_datetime(designation.valid_from)
            valid_to = (
                ensure_datetime(designation.valid_to)
                if designation.valid_to is not None
                else None
            )

            if valid_from <= date and (valid_to is None or valid_to >= date):
                return designation
        return None

    def __repr__(self):
        return f"<Satellite {self.object_id}>"

    def __eq__(self, other):
        return (
            self.object_id == other.object_id
            and self.constellation == other.constellation
            and self.generation == other.generation
            and self.rcs_size == other.rcs_size
            and self.launch_date == other.launch_date
            and self.decay_date == other.decay_date
            and self.object_type == other.object_type
        )

    def __hash__(self):
        return hash(
            (
                self.object_id,
                self.constellation,
                self.generation,
                self.rcs_size,
                self.launch_date,
                self.decay_date,
                self.object_type,
            )
        )
