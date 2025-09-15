# pragma: no cover
import pickle
from datetime import datetime
from typing import Any, Optional, TypedDict

from attr import dataclass
from scipy.interpolate import KroghInterpolator

from api.utils.interpolation_utils import InterpolatedSplinesDict


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


@dataclass(eq=False, unsafe_hash=False)
class InterpolatorSplines:
    """
    Domain model for cached interpolator splines.

    This model represents the complete interpolator structure that can be
    directly used by the interpolation_utils functions without any reconstruction.
    """

    # Core identifiers
    sat_id: int
    ephemeris_id: int
    time_range_start: datetime
    time_range_end: datetime
    generated_at: datetime
    data_source: str

    # The actual interpolator data structure
    interpolated_splines: InterpolatedSplinesDict

    # Optional metadata
    method: str = "krogh_chunked"
    chunk_size: int = 14
    overlap: int = 8
    n_sigma_points: int = 13
    date_collected: Optional[datetime] = None

    def __post_init__(self):
        """Validate the interpolated_splines structure."""
        if not isinstance(self.interpolated_splines, dict):
            raise ValueError("interpolated_splines must be a dictionary")

        required_keys = ["positions", "velocities", "time_range"]
        for key in required_keys:
            if key not in self.interpolated_splines:
                raise ValueError(f"interpolated_splines missing required key: {key}")

        # Validate structure matches expected format
        positions = self.interpolated_splines["positions"]
        velocities = self.interpolated_splines["velocities"]
        time_range = self.interpolated_splines["time_range"]

        if len(positions) != self.n_sigma_points:
            raise ValueError(
                f"Expected {self.n_sigma_points} sigma points, got {len(positions)}"
            )

        if len(velocities) != self.n_sigma_points:
            raise ValueError(
                f"Expected {self.n_sigma_points} sigma points, got {len(velocities)}"
            )

        if not isinstance(time_range, tuple) or len(time_range) != 2:
            raise ValueError("time_range must be a tuple of (start_time, end_time)")

        # Validate each sigma point has 3 components (x, y, z)
        for i, pos_splines in enumerate(positions):
            if len(pos_splines) != 3:
                raise ValueError(
                    f"Sigma point {i} positions should have 3 components, "
                    f"got {len(pos_splines)}"
                )

        for i, vel_splines in enumerate(velocities):
            if len(vel_splines) != 3:
                raise ValueError(
                    f"Sigma point {i} velocities should have 3 components, "
                    f"got {len(vel_splines)}"
                )

    def get_interpolated_splines(self) -> dict[str, Any]:
        """
        Get the interpolated splines structure for direct use with interpolation_utils.

        Returns:
            The exact structure expected by get_interpolated_sigma_points_KI()
        """
        return self.interpolated_splines

    def serialize_for_storage(self) -> bytes:
        """
        Serialize the interpolated_splines for database storage.

        Returns:
            Pickled bytes ready for LargeBinary storage
        """
        return pickle.dumps(self.interpolated_splines)

    def __eq__(self, other):
        """Check equality of InterpolatorSplines objects."""
        if not isinstance(other, InterpolatorSplines):
            return False
        return (
            self.sat_id == other.sat_id
            and self.ephemeris_id == other.ephemeris_id
            and self.time_range_start == other.time_range_start
            and self.time_range_end == other.time_range_end
            and self.generated_at == other.generated_at
            and self.data_source == other.data_source
            and self.method == other.method
            and self.chunk_size == other.chunk_size
            and self.overlap == other.overlap
            and self.n_sigma_points == other.n_sigma_points
        )

    def __hash__(self):
        """Make InterpolatorSplines hashable for use in sets."""
        # Hash all fields that are used in __eq__ to ensure consistency
        return hash(
            (
                self.sat_id,
                self.ephemeris_id,
                self.time_range_start,
                self.time_range_end,
                self.generated_at,
                self.data_source,
                self.method,
                self.chunk_size,
                self.overlap,
                self.n_sigma_points,
            )
        )
