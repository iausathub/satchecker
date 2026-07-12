from abc import ABC, abstractmethod
from datetime import datetime

from skyfield.api import EarthSatellite, Timescale

from api.domain.models.satellite import Satellite


class OrbitalData(ABC):
    def __init__(
        self,
        date_collected: datetime,
        epoch: datetime,
        data_source: str,
        satellite: Satellite,
    ):
        self.date_collected = date_collected
        self.epoch = epoch
        self.data_source = data_source
        self.satellite = satellite

    def get_satellite(self) -> Satellite:
        return self.satellite

    @property
    @abstractmethod
    def is_supplemental(self) -> bool: ...

    @abstractmethod
    def to_earth_satellite(self, ts: Timescale) -> EarthSatellite: ...

    # @abstractmethod
    # def to_tle_lines(self) -> tuple[str, str]:
    #    ...
