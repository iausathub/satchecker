from datetime import datetime, timezone

import numpy as np

from api.domain.models.satellite import Satellite


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
        try:
            return (
                self.timestamp == other.timestamp
                and np.array_equal(self.position, other.position)
                and np.array_equal(self.velocity, other.velocity)
                and np.array_equal(self.covariance, other.covariance)
            )
        except AttributeError:
            return False

    def __repr__(self):
        return (
            f"<EphemerisPoint timestamp={self.timestamp} "
            f"position={self.position} velocity={self.velocity}>"
        )


class InterpolableEphemeris:
    def __init__(
        self,
        satellite: Satellite,
        generated_at: datetime,
        data_source: str,
        frame: str,
        points: list[EphemerisPoint],
        ephemeris_start: datetime,
        ephemeris_stop: datetime,
        file_reference: str | None = None,
        date_collected: datetime | None = None,
        id: int | None = None,
    ):
        self.id = id
        self.satellite = satellite
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
            f"<InterpolableEphemeris satellite={self.satellite} "
            f"generated_at={self.generated_at}>"
        )

    def __eq__(self, other):
        try:
            return (
                self.satellite == other.satellite
                and self.generated_at == other.generated_at
                and self.data_source == other.data_source
                and self.file_reference == other.file_reference
                and self.frame == other.frame
                and self.date_collected == other.date_collected
                and self.ephemeris_start == other.ephemeris_start
                and self.ephemeris_stop == other.ephemeris_stop
                and len(self.points) == len(other.points)
                and all(
                    p1 == p2 for p1, p2 in zip(self.points, other.points, strict=True)
                )
            )
        except AttributeError:
            return False

    def __hash__(self):
        point_tuples = []
        for point in self.points:
            # Convert numpy arrays to tuples of native Python types
            position_tuple = tuple(float(x) for x in point.position)
            velocity_tuple = tuple(float(x) for x in point.velocity)
            covariance_tuple = tuple(
                tuple(float(x) for x in row) for row in point.covariance
            )

            point_tuple = (
                point.timestamp,
                position_tuple,
                velocity_tuple,
                covariance_tuple,
            )
            point_tuples.append(point_tuple)

        point_tuples_tuple = tuple(point_tuples)

        hash_tuple = (
            self.id,
            self.satellite,
            self.generated_at,
            self.data_source,
            self.file_reference,
            self.frame,
            self.date_collected,
            self.ephemeris_start,
            self.ephemeris_stop,
            point_tuples_tuple,
        )

        return hash(hash_tuple)
