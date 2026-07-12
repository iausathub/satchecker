from datetime import datetime

from skyfield.api import EarthSatellite, Timescale

from api.domain.models.orbital_data import OrbitalData
from api.domain.models.satellite import Satellite


class OrbitalElements(OrbitalData):
    def __init__(
        self,
        date_collected: datetime,
        epoch: datetime,
        data_source: str,
        satellite: Satellite,
        mean_motion: float,
        eccentricity: float,
        inclination: float,
        ra_of_ascending_node: float,
        arg_of_pericenter: float,
        mean_anomaly: float,
        ephemeris_type: int,
        classification_type: str,
        element_set_no: int,
        rev_at_epoch: int,
        bstar: float,
        mean_motion_dot: float,
        mean_motion_ddot: float,
    ):
        super().__init__(date_collected, epoch, data_source, satellite)
        self.mean_motion = mean_motion
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.ra_of_ascending_node = ra_of_ascending_node
        self.arg_of_pericenter = arg_of_pericenter
        self.mean_anomaly = mean_anomaly
        self.ephemeris_type = ephemeris_type
        # U for unclassified (or GP), or C for supplemental data from Celestrak.
        # Normally C means classified, but all our data is public and Celestrak
        # uses C for supplemental; C will never mean classified here.
        self.classification_type = classification_type
        self.element_set_no = element_set_no
        self.rev_at_epoch = rev_at_epoch
        self.bstar = bstar
        self.mean_motion_dot = mean_motion_dot
        self.mean_motion_ddot = mean_motion_ddot

    def __repr__(self):
        return f"<OrbitalElements {self.satellite}>"

    def __eq__(self, other):
        return (
            self.date_collected == other.date_collected
            and self.epoch == other.epoch
            and self.classification_type == other.classification_type
            and self.mean_motion == other.mean_motion
            and self.eccentricity == other.eccentricity
            and self.inclination == other.inclination
            and self.ra_of_ascending_node == other.ra_of_ascending_node
            and self.arg_of_pericenter == other.arg_of_pericenter
            and self.mean_anomaly == other.mean_anomaly
            and self.bstar == other.bstar
            and self.mean_motion_dot == other.mean_motion_dot
            and self.data_source == other.data_source
            and self.satellite == other.satellite
        )

    def __hash__(self):
        return hash(
            (
                self.date_collected,
                self.epoch,
                self.classification_type,
                self.mean_motion,
                self.eccentricity,
                self.inclination,
                self.ra_of_ascending_node,
                self.arg_of_pericenter,
                self.mean_anomaly,
                self.bstar,
                self.mean_motion_dot,
                self.mean_motion_ddot,
                self.data_source,
                self.satellite,
            )
        )

    def get_satellite(self):
        return self.satellite

    def to_earth_satellite(self, ts: Timescale) -> EarthSatellite:
        # sgp4.omm.initialize() requires these exact CCSDS OMM field names
        element_dict = {
            "OBJECT_NAME": self.satellite.sat_name,
            "OBJECT_ID": self.satellite.object_id or "",
            "EPOCH": self.epoch.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "MEAN_MOTION": self.mean_motion,
            "ECCENTRICITY": self.eccentricity,
            "INCLINATION": self.inclination,
            "RA_OF_ASC_NODE": self.ra_of_ascending_node,
            "ARG_OF_PERICENTER": self.arg_of_pericenter,
            "MEAN_ANOMALY": self.mean_anomaly,
            "EPHEMERIS_TYPE": self.ephemeris_type,
            "CLASSIFICATION_TYPE": self.classification_type,
            "NORAD_CAT_ID": self.satellite.sat_number,
            "ELEMENT_SET_NO": self.element_set_no,
            "REV_AT_EPOCH": self.rev_at_epoch,
            "BSTAR": self.bstar,
            "MEAN_MOTION_DOT": self.mean_motion_dot,
            "MEAN_MOTION_DDOT": self.mean_motion_ddot,
        }

        return EarthSatellite.from_omm(ts=ts, element_dict=element_dict)

    @property
    def is_supplemental(self) -> bool:
        return self.classification_type == "C"
