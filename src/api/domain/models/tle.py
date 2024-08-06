from datetime import datetime

from src.api.domain.models.satellite import Satellite


class TLE:
    def __init__(
        self,
        date_collected: datetime,
        tle_line1: str,
        tle_line2: str,
        epoch: datetime,
        is_supplemental: bool,
        data_source: str,
        satellite: Satellite,
    ):
        self.date_collected = date_collected
        self.tle_line1 = tle_line1
        self.tle_line2 = tle_line2
        self.epoch = epoch
        self.is_supplemental = is_supplemental
        self.data_source = data_source
        self.satellite = satellite

    def __repr__(self):
        return f"<TLE {self.satellite}>"

    def __eq__(self, other):
        return (
            self.date_collected == other.date_collected
            and self.tle_line1 == other.tle_line1
            and self.tle_line2 == other.tle_line2
            and self.epoch == other.epoch
            and self.is_supplemental == other.is_supplemental
            and self.data_source == other.data_source
            and self.satellite == other.satellite
        )

    def __hash__(self):
        return hash(
            (
                self.date_collected,
                self.tle_line1,
                self.tle_line2,
                self.epoch,
                self.is_supplemental,
                self.data_source,
            )
        )

    def get_satellite(self):
        return self.satellite
