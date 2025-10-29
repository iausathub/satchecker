from datetime import datetime


class Satellite:
    def __init__(
        self,
        sat_number: int,
        sat_name: str,
        constellation: str | None = None,
        generation: str | None = None,
        rcs_size: str | None = None,
        launch_date: datetime | None = None,
        decay_date: datetime | None = None,
        object_id: str | None = None,
        object_type: str | None = None,
        has_current_sat_number: bool = False,
    ):
        self.sat_number = sat_number
        self.sat_name = sat_name
        self.constellation = constellation
        self.generation = generation
        self.rcs_size = rcs_size
        self.launch_date = launch_date
        self.decay_date = decay_date
        self.object_id = object_id
        self.object_type = object_type
        self.has_current_sat_number = has_current_sat_number

    def __repr__(self):
        return f"<Satellite {self.sat_name}>"

    def __eq__(self, other):
        return self.sat_number == other.sat_number and self.sat_name == other.sat_name

    def __hash__(self):
        return hash((self.sat_number, self.sat_name))
