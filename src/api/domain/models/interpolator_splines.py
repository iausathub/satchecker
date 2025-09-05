# pragma: no cover
from datetime import datetime
from typing import Optional, TypedDict

from attr import dataclass
from scipy.interpolate import KroghInterpolator


class InterpolatorChunk(TypedDict):
    interpolator: KroghInterpolator
    range: tuple[float, float]


"""
class InterpolatorChunk:
    def __init__(
        self,
        coefficients: list[float],
        valid_range: tuple[float, float],  # (start_time, end_time) in Julian dates
    ):
        self.coefficients = coefficients
        self.valid_range = valid_range

    def __eq__(self, other):
        if not isinstance(other, InterpolatorChunk):
            return False
        return (
            np.array_equal(self.coefficients, other.coefficients)
            and self.valid_range == other.valid_range
        )


class ComponentSplines:
    def __init__(
        self,
        chunks: list[InterpolatorChunk],
    ):
        self.chunks = chunks

    def __eq__(self, other):
        if not isinstance(other, ComponentSplines):
            return False
        return len(self.chunks) == len(other.chunks) and all(
            c1 == c2 for c1, c2 in zip(self.chunks, other.chunks)
        )


class SigmaPointSplines:
    def __init__(
        self,
        position_splines: list[ComponentSplines],  # [x, y, z]
        velocity_splines: list[ComponentSplines],  # [vx, vy, vz]
    ):
        self.position_splines = position_splines
        self.velocity_splines = velocity_splines

    def __eq__(self, other):
        if not isinstance(other, SigmaPointSplines):
            return False
        return (
            len(self.position_splines) == len(other.position_splines)
            and len(self.velocity_splines) == len(other.velocity_splines)
            and all(
                p1 == p2
                for p1, p2 in zip(self.position_splines, other.position_splines)
            )
            and all(
                v1 == v2
                for v1, v2 in zip(self.velocity_splines, other.velocity_splines)
            )
        )
        """


@dataclass
class InterpolatorSplines:

    sat_id: int
    ephemeris_id: int
    time_range_start: datetime
    time_range_end: datetime
    generated_at: datetime
    data_source: str
    sigma_point_splines: list[list[InterpolatorChunk]]  # [13 sigma points] TODO: FIX!
    date_collected: Optional[datetime] = None
