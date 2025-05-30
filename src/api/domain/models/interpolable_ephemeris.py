from datetime import datetime, timezone
from typing import Optional

import numpy as np


class EphemerisPoint:
    def __init__(
        self,
        timestamp: datetime,
        position: np.ndarray,
        velocity: np.ndarray,
        covariance: np.ndarray,
    ):
        self.timestamp = timestamp
        self.position = position
        self.velocity = velocity
        self.covariance = covariance

    def __eq__(self, other):
        if not isinstance(other, EphemerisPoint):
            return False
        return (
            self.timestamp == other.timestamp
            and np.array_equal(self.position, other.position)
            and np.array_equal(self.velocity, other.velocity)
            and np.array_equal(self.covariance, other.covariance)
        )


class InterpolableEphemeris:
    def __init__(
        self,
        sat_id: int,
        generated_at: datetime,
        data_source: str,
        frame: str,
        points: list[EphemerisPoint],
        ephemeris_start: datetime,
        ephemeris_stop: datetime,
        file_reference: Optional[str] = None,
        date_collected: Optional[datetime] = None,
    ):
        self.sat_id = sat_id
        self.date_collected = date_collected or datetime.now(timezone.utc)
        self.generated_at = generated_at
        self.data_source = data_source
        self.file_reference = file_reference
        self.frame = frame
        self.points = points
        self.ephemeris_start = ephemeris_start
        self.ephemeris_stop = ephemeris_stop

    def __repr__(self):
        return (
            f"<InterpolableEphemeris sat_id={self.sat_id} "
            f"generated_at={self.generated_at}>"
        )

    def __eq__(self, other):
        if not isinstance(other, InterpolableEphemeris):
            return False

        return (
            self.sat_id == other.sat_id
            and self.generated_at == other.generated_at
            and self.data_source == other.data_source
            and self.file_reference == other.file_reference
            and self.frame == other.frame
            and self.date_collected == other.date_collected
            and self.ephemeris_start == other.ephemeris_start
            and self.ephemeris_stop == other.ephemeris_stop
            and len(self.points) == len(other.points)
            and all(p1 == p2 for p1, p2 in zip(self.points, other.points))
        )
