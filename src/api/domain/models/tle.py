from datetime import datetime

from skyfield.api import EarthSatellite, Timescale

from api.domain.models.orbital_data import OrbitalData
from api.domain.models.satellite import Satellite


class TLE(OrbitalData):
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
        super().__init__(date_collected, epoch, data_source, satellite)
        self.tle_line1 = tle_line1
        self.tle_line2 = tle_line2
        self._is_supplemental = is_supplemental

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

    @property
    def is_supplemental(self) -> bool:
        return self._is_supplemental

    def to_earth_satellite(self, ts: Timescale) -> EarthSatellite:
        return EarthSatellite(self.tle_line1, self.tle_line2, ts=ts)

    def get_satellite(self):
        return self.satellite
