from datetime import datetime

from api.domain.models.satellite import Satellite


class TdmPrediction:
    def __init__(
        self,
        creation_date: datetime,
        time_range_start: datetime,
        time_range_end: datetime,
        site_name: str,
        satellite: Satellite,
        reference_frame: str,
        date_added: datetime,
        track_id: str,
        folder_name: str,
        id: int | None = None,
    ):
        self.id = id
        self.creation_date = creation_date
        self.time_range_start = time_range_start
        self.time_range_end = time_range_end
        self.site_name = site_name
        self.satellite = satellite
        self.reference_frame = reference_frame
        self.date_added = date_added
        self.track_id = track_id
        self.folder_name = folder_name

    def __repr__(self):
        return f"<TdmPrediction {self.site_name} {self.satellite} {self.creation_date}>"

    def __eq__(self, other):
        return (
            self.creation_date == other.creation_date
            and self.time_range_start == other.time_range_start
            and self.time_range_end == other.time_range_end
            and self.site_name == other.site_name
            and self.satellite == other.satellite
            and self.reference_frame == other.reference_frame
            and self.date_added == other.date_added
            and self.track_id == other.track_id
            and self.folder_name == other.folder_name
        )

    def __hash__(self):
        return hash(
            (
                self.creation_date,
                self.time_range_start,
                self.time_range_end,
                self.site_name,
                self.satellite,
                self.reference_frame,
                self.date_added,
                self.track_id,
                self.folder_name,
            )
        )
