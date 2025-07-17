from datetime import datetime
from typing import Optional


class SatelliteDesignation:
    def __init__(
        self,
        sat_name: str,
        sat_number: int,
        valid_from: datetime,
        valid_to: Optional[datetime] = None,
    ):
        self.sat_name = sat_name
        self.sat_number = sat_number
        self.valid_from = valid_from
        self.valid_to = valid_to

    def __repr__(self):
        return f"<SatelliteDesignation {self.sat_name} - {self.sat_number}>"

    def __eq__(self, other):
        return (
            self.sat_number == other.sat_number
            and self.sat_name == other.sat_name
            and self.valid_from == other.valid_from
            and self.valid_to == other.valid_to
        )

    def __hash__(self):
        return hash(
            (
                self.sat_number,
                self.sat_name,
                self.valid_from,
                self.valid_to,
            )
        )
