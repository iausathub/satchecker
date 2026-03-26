from datetime import datetime


class TdmPredictionPoint:
    def __init__(
        self,
        tdm_prediction_id: int,
        timestamp: datetime,
        right_ascension: float,
        declination: float,
        apparent_magnitude: float,
        satellite_number: int,
        satellite_name: str,
    ):
        self.tdm_prediction_id = tdm_prediction_id
        self.timestamp = timestamp
        self.right_ascension = right_ascension
        self.declination = declination
        self.apparent_magnitude = apparent_magnitude
        self.satellite_number = satellite_number
        self.satellite_name = satellite_name

    def __repr__(self):
        return (
            f"<TdmPredictionPoint {self.tdm_prediction_id} {self.timestamp} "
            f"{self.satellite_number} {self.satellite_name} "
            f"{self.right_ascension} {self.declination} {self.apparent_magnitude}>"
        )

    def __eq__(self, other):
        return (
            self.tdm_prediction_id == other.tdm_prediction_id
            and self.timestamp == other.timestamp
            and self.right_ascension == other.right_ascension
            and self.declination == other.declination
            and self.apparent_magnitude == other.apparent_magnitude
            and self.satellite_number == other.satellite_number
            and self.satellite_name == other.satellite_name
        )

    def __hash__(self):
        return hash(
            (
                self.tdm_prediction_id,
                self.timestamp,
                self.right_ascension,
                self.declination,
                self.apparent_magnitude,
                self.satellite_number,
                self.satellite_name,
            )
        )
