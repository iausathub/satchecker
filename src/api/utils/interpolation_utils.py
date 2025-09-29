from typing import Any, TypedDict

import julian
import numpy as np
from scipy.interpolate import KroghInterpolator
from scipy.linalg import sqrtm

from api.domain.models.interpolable_ephemeris import InterpolableEphemeris


class InterpolatorChunk(TypedDict):
    interpolator: KroghInterpolator
    range: tuple[float, float]


def serialize_interpolator_chunk(chunk: InterpolatorChunk) -> dict:
    """
    Serialize an InterpolatorChunk to a compact format storing only coefficients.

    Args:
        chunk: InterpolatorChunk containing KroghInterpolator and range

    Returns:
        dict: Compact representation with coefficients instead of full interpolator
    """
    return {
        "coefficients": chunk["interpolator"].c.tolist(),  # Extract coefficients
        "x_points": chunk[
            "interpolator"
        ].xi.tolist(),  # Store x points for reconstruction
        "range": chunk["range"],
        "degree": len(chunk["interpolator"].c) - 1,
    }


def deserialize_interpolator_chunk(data: dict) -> InterpolatorChunk:
    """
    Deserialize a compact InterpolatorChunk back to full format.

    Args:
        data: Compact representation with coefficients

    Returns:
        InterpolatorChunk: Full InterpolatorChunk with reconstructed KroghInterpolator
    """
    # Reconstruct the KroghInterpolator from coefficients
    x_points = np.array(data["x_points"])
    coefficients = np.array(data["coefficients"])

    interpolator = KroghInterpolator(x_points, np.zeros_like(x_points))
    interpolator.c = coefficients

    return {"interpolator": interpolator, "range": data["range"]}


class InterpolatedSplinesDict(TypedDict):
    """Type definition for the return value of interpolate_sigma_pointsKI."""

    positions: list[list[list[InterpolatorChunk] | None]]
    velocities: list[list[list[InterpolatorChunk] | None]]
    time_range: tuple[float, float]


def generate_and_propagate_sigma_points(ephemeris: InterpolableEphemeris) -> dict:
    """
    Generate and propagate sigma points using the Unscented Transform for improved
    numerical stability.

    This method implements the Unscented Transform to generate sigma points from
    the state vectors and covariance matrices in the ephemeris data. The sigma
    points are used to capture the mean and covariance of the state distribution
    more accurately than linearization methods.

    The method uses optimized parameters for the Unscented Transform:
    - alpha = 0.001 (reduced for better numerical stability)
    - beta = 2.0 (optimal for Gaussian distributions)
    - kappa = 3-n (modified for better stability)

    Args:
        ephemeris (InterpolableEphemeris): The ephemeris data containing state
        vectors and covariance matrices.

    Returns:
        dict: A dictionary mapping Julian dates to sigma point information:
            - sigma_points (np.ndarray): Array of 13 sigma points (6D state vectors)
            - weights (dict): Dictionary containing mean and covariance weights
            - epoch (datetime): Timestamp for these sigma points
            - state_vector (np.ndarray): Original state vector
            - covariance (np.ndarray): Original covariance matrix

    Raises:
        ValueError: If no sigma points could be generated successfully
        np.linalg.LinAlgError: If covariance matrix is not positive definite

    Note:
        The method uses Cholesky decomposition for numerical stability,
        falling back to matrix square root if Cholesky fails. Each sigma
        point set contains 13 points:
        - 1 mean state point
        - 6 points from positive Cholesky decomposition
        - 6 points from negative Cholesky decomposition
    """
    try:
        # Use high precision for Julian date conversion with pre-allocation
        n_points = len(ephemeris.points)
        julian_dates = np.empty(n_points, dtype=np.float64)
        for i, point in enumerate(ephemeris.points):
            julian_dates[i] = float(julian.to_jd(point.timestamp))

        # Stack positions and velocities into state vectors
        state_vectors = np.hstack(
            (
                np.array(
                    [point.position for point in ephemeris.points], dtype=np.float64
                ),
                np.array(
                    [point.velocity for point in ephemeris.points], dtype=np.float64
                ),
            )
        )
        covariances = np.array(
            [point.covariance for point in ephemeris.points], dtype=np.float64
        )

        sigma_points_dict = {}

        # Optimized Unscented Transform parameters
        n = 6
        alpha = np.float64(0.001)  # Reduced alpha for better numerical stability
        beta = np.float64(2.0)  # Optimal for Gaussian
        kappa = np.float64(3 - n)  # Modified for better stability
        lambda_param = alpha * alpha * (n + kappa) - n

        # Precompute weights for efficiency and precision
        w0_m = lambda_param / (n + lambda_param)
        wn_m = np.float64(0.5) / (n + lambda_param)
        w0_c = w0_m + (1 - alpha * alpha + beta)
        wn_c = wn_m

        weights = {
            "mean": {"w0": w0_m, "wn": wn_m},
            "covariance": {"w0": w0_c, "wn": wn_c},
        }

        for idx, (jd, point) in enumerate(zip(julian_dates, ephemeris.points)):
            try:
                state_vector = state_vectors[idx]
                covariance = covariances[idx]

                # Ensure symmetry of covariance matrix
                covariance = (covariance + covariance.T) / 2

                # Scale covariance with improved numerical stability
                scaled_cov = (n + lambda_param) * covariance

                # Try Cholesky first, fall back to modified sqrtm if needed
                try:
                    L = np.linalg.cholesky(scaled_cov)  # noqa: N806
                except np.linalg.LinAlgError:
                    L = sqrtm(scaled_cov)  # noqa: N806

                sigma_0 = state_vector
                sigma_n = sigma_0[:, np.newaxis] + L
                sigma_2n = sigma_0[:, np.newaxis] - L

                all_sigma_points = np.vstack([sigma_0, sigma_n.T, sigma_2n.T])

                sigma_points_dict[float(jd)] = {  # Ensure jd is a float
                    "sigma_points": all_sigma_points,
                    "weights": weights,
                    "epoch": point.timestamp,
                    "state_vector": state_vector,
                    "covariance": covariance,
                }

            except Exception as e:
                print(
                    f"Warning: Failed to process timestamp "
                    f"{point.timestamp}: {str(e)}"
                )
                continue

        if not sigma_points_dict:
            raise ValueError("No sigma points could be generated successfully")

        return sigma_points_dict

    except Exception as e:
        raise ValueError(f"Failed to generate sigma points: {str(e)}") from e


def create_chunked_krogh_interpolator(
    x: np.ndarray, y: np.ndarray, chunk_size: int = 14, overlap: int = 8
) -> list[InterpolatorChunk]:
    """
    Create a series of overlapping Krogh interpolators to handle large datasets
    with improved stability.

    This function splits the input data into overlapping chunks and creates a Krogh
    interpolator for each chunk. This approach helps avoid numerical instability
    that can occur when interpolating over many points using a single interpolator.

    The method uses a sliding window approach with overlap to ensure smooth
    transitions between chunks. For each chunk:
    - First chunk: Valid from start to just before end
    - Middle chunks: Valid in middle portion, leaving overlap areas for
    adjacent chunks
    - Last chunk: Valid from just after start to end

    Args:
        x (np.ndarray): Independent variable values (e.g., times)
        y (np.ndarray): Dependent variable values to interpolate
        chunk_size (int, optional): Number of points to use in each interpolation
        chunk. Defaults to 14.
        overlap (int, optional): Number of points to overlap between chunks.
            Defaults to 8.

    Returns:
        list[InterpolatorChunk]: List of InterpolatorChunk objects, each containing:
            - interpolator (KroghInterpolator): The interpolator for this chunk
            - range (tuple[float, float]): Valid range for this interpolator
            (lower, upper)

    Note:
        - If input data length is less than chunk_size, returns a single
        interpolator
        - Overlap should be less than chunk_size to ensure progress
        - The valid ranges are slightly narrower than the actual chunks to ensure
          smooth transitions between interpolators
    """
    if len(x) <= chunk_size:
        interp = KroghInterpolator(x, y)
        return [{"interpolator": interp, "range": (x[0], x[-1])}]

    # Split data into overlapping chunks
    interpolators: list[InterpolatorChunk] = []
    i = 0
    while i < len(x):
        end_idx = min(i + chunk_size, len(x))
        chunk_x = x[i:end_idx]
        chunk_y = y[i:end_idx]

        # Create interpolator for this chunk
        interp = KroghInterpolator(chunk_x, chunk_y)

        # Record the valid range for this chunk (slightly narrower than the
        # actual chunk) to ensure smooth transitions between chunks
        if i == 0:
            # First chunk - use from beginning to just before end
            valid_range = (
                chunk_x[0],
                chunk_x[-2] if len(chunk_x) > 2 else chunk_x[-1],
            )
        elif end_idx == len(x):
            # Last chunk - use from just after start to end
            valid_range = (
                chunk_x[1] if len(chunk_x) > 1 else chunk_x[0],
                chunk_x[-1],
            )
        else:
            # Middle chunks - use middle portion, leaving overlap areas
            # for adjacent chunks
            valid_range = (
                chunk_x[1] if len(chunk_x) > 1 else chunk_x[0],
                chunk_x[-2] if len(chunk_x) > 2 else chunk_x[-1],
            )

        interpolators.append({"interpolator": interp, "range": valid_range})

        # Move to next chunk with overlap, ensuring we make progress
        i = max(end_idx - overlap, i + 1)

    return interpolators


def interpolate_sigma_pointsKI(  # noqa: N802
    sigma_points_dict: dict,
) -> InterpolatedSplinesDict:
    """
    Create high-precision interpolation splines for sigma point trajectories using
    chunked Krogh interpolation.

    This function processes the sigma points dictionary to create interpolators for
    each component of the position and velocity vectors. It handles 13 sigma
    points (1 mean + 6 positive + 6 negative Cholesky points) and creates separate
    interpolators for each component (x, y, z) of both position and velocity.

    The function uses chunked Krogh interpolation to maintain numerical stability when
    dealing with long time series. Each component is interpolated independently, and
    invalid or non-finite values are handled gracefully.

    Args:
        sigma_points_dict (dict[str, dict[str, np.ndarray]]): Dictionary mapping
        Julian dates to sigma point
            information:
            - sigma_points (np.ndarray): Array of 13 sigma points (6D state vectors)
            - weights (dict): Dictionary containing mean and covariance weights
            - epoch (datetime): Timestamp for these sigma points
            - state_vector (np.ndarray): Original state vector
            - covariance (np.ndarray): Original covariance matrix

    Returns:
        Dictionary containing interpolation splines and time range:
            - positions: List of lists of position interpolators:
                - Outer list: One entry per sigma point (13 total)
                - Inner list: One entry per component (x, y, z)
                - Each entry: List of chunked Krogh interpolators (can contain None
                for invalid components)
            - velocities: List of lists of velocity interpolators:
                - Outer list: One entry per sigma point (13 total)
                - Inner list: One entry per component (x, y, z)
                - Each entry: List of chunked Krogh interpolators (can contain None
                for invalid components)
            - time_range: (start_time, end_time) in Julian dates

    Note:
        - Each component (x, y, z) of position and velocity has its own set of
          interpolators
        - Interpolators are created only for valid (finite) data points
        - The chunking parameters (chunk_size=14, overlap=8) are optimized
        for stability
        - None is returned for components with no valid data points
    """
    julian_dates = np.array(sorted(sigma_points_dict.keys()), dtype=np.float64)
    n_sigma_points = 13

    positions_by_point: list[list[np.ndarray]] = [[] for _ in range(n_sigma_points)]
    velocities_by_point: list[list[np.ndarray]] = [[] for _ in range(n_sigma_points)]

    for jd in julian_dates:
        sigma_points = sigma_points_dict[jd]["sigma_points"].astype(np.float64)
        for i in range(n_sigma_points):
            positions_by_point[i].append(sigma_points[i][:3])
            velocities_by_point[i].append(sigma_points[i][3:])

    # Convert lists to numpy arrays
    positions_array: list[np.ndarray] = [
        np.array(pos, dtype=np.float64) for pos in positions_by_point
    ]
    velocities_array: list[np.ndarray] = [
        np.array(vel, dtype=np.float64) for vel in velocities_by_point
    ]

    position_splines = []
    velocity_splines = []

    for i in range(n_sigma_points):
        # Position splines
        pos_splines_i: list[list[InterpolatorChunk] | None] = []
        for j in range(3):
            pos_data = positions_array[i][:, j]
            valid_mask = np.isfinite(pos_data)
            if np.any(valid_mask):
                # Use not-a-knot cubic splines for better accuracy
                spline = create_chunked_krogh_interpolator(
                    julian_dates[valid_mask],
                    pos_data[valid_mask],
                    chunk_size=14,
                    overlap=8,
                )
                pos_splines_i.append(spline)
            else:
                pos_splines_i.append(None)
        position_splines.append(pos_splines_i)

        vel_splines_i: list[list[InterpolatorChunk] | None] = []
        for j in range(3):
            vel_data = velocities_array[i][:, j]
            valid_mask = np.isfinite(vel_data)
            if np.any(valid_mask):
                spline = create_chunked_krogh_interpolator(
                    julian_dates[valid_mask],
                    vel_data[valid_mask],
                    chunk_size=14,
                    overlap=8,
                )
                vel_splines_i.append(spline)
            else:
                vel_splines_i.append(None)
        velocity_splines.append(vel_splines_i)

    return {
        "positions": position_splines,
        "velocities": velocity_splines,
        "time_range": (julian_dates[0], julian_dates[-1]),
    }


def get_interpolated_sigma_points_KI(  # noqa: N802
    interpolated_splines: dict[str, Any], julian_date: float
) -> np.ndarray:
    """
    Get interpolated sigma points at a specific Julian date using optimal
    chunk selection.

    This function interpolates the position and velocity components of all
    13 sigma points at the requested Julian date. It uses a sophisticated
    chunk selection algorithm that prefers interpolators where the requested
    time is in the middle of their valid range, rather than at the edges,
    to minimize interpolation errors.

    The function handles both position and velocity components (x, y, z) for each
    sigma point, selecting the most appropriate interpolator chunk for each
    component based on the requested time's position within the chunk's valid range.

    Args:
        interpolated_splines: Dictionary containing interpolation splines:
            - positions: List of lists of position interpolators (can contain None
            for invalid components)
            - velocities: List of lists of velocity interpolators (can contain None
            for invalid components)
            - time_range: (start_time, end_time) in Julian dates
        julian_date (float): The Julian date at which to interpolate the sigma
        points

    Returns:
        np.ndarray: Array of shape (13, 6) containing the interpolated sigma points:
            - First 13 rows: One row per sigma point
            - 6 columns: [x, y, z, vx, vy, vz] for each point
            - dtype: np.float64 for high precision

    Raises:
        ValueError: If the requested Julian date is outside the interpolation range

    Note:
        - The function uses a centrality score to select the best interpolator chunk
        - For times outside any chunk's range, the nearest chunk is used
        - All calculations are performed in double precision (np.float64)
        - The function assumes the input splines are valid and properly structured
    """
    start_time, end_time = interpolated_splines["time_range"]
    if not (start_time <= julian_date <= end_time):
        raise ValueError(
            f"Requested time {julian_date} is outside the interpolation range "
            f"[{start_time}, {end_time}]"
        )

    n_sigma_points = 13
    interpolated_points = np.zeros((n_sigma_points, 6), dtype=np.float64)

    for i in range(n_sigma_points):
        # Interpolate positions
        for j in range(3):
            if interpolated_splines["positions"][i][j] is not None:
                splines = interpolated_splines["positions"][i][j]
                applicable_splines = []
                for idx, spline_info in enumerate(splines):
                    pos_lower: float
                    pos_upper: float
                    pos_lower, pos_upper = spline_info["range"]
                    if pos_lower <= julian_date <= pos_upper:
                        # Calculate how central the point is within this
                        # spline's range (0.5 means it's in the middle, 0
                        # or 1 means it's at an edge)
                        centrality = (julian_date - pos_lower) / (pos_upper - pos_lower)

                        # Prefer points that are more central (closer to 0.5)
                        # Converts to 0-1 scale where 1 is most central
                        score = 1 - abs(centrality - 0.5) * 2
                        applicable_splines.append((idx, score, spline_info))

                # If we found applicable splines, use the most central one
                if applicable_splines:
                    applicable_splines.sort(key=lambda x: x[1], reverse=True)
                    best_spline = applicable_splines[0][2]
                    interpolated_points[i, j] = best_spline["interpolator"](julian_date)
                else:
                    # If no spline's range contains this point, use the closest one
                    if julian_date < start_time:
                        interpolated_points[i, j] = splines[0]["interpolator"](
                            julian_date
                        )
                    else:
                        interpolated_points[i, j] = splines[-1]["interpolator"](
                            julian_date
                        )

        # Interpolate velocities
        for j in range(3):
            if interpolated_splines["velocities"][i][j] is not None:
                splines = interpolated_splines["velocities"][i][j]
                applicable_splines = []

                for idx, spline_info in enumerate(splines):
                    vel_lower: float
                    vel_upper: float
                    vel_lower, vel_upper = spline_info["range"]
                    if vel_lower <= julian_date <= vel_upper:
                        centrality = (julian_date - vel_lower) / (vel_upper - vel_lower)
                        # Prefer points that are more central
                        score = 1 - abs(centrality - 0.5) * 2
                        applicable_splines.append((idx, score, spline_info))

                # If we found applicable splines, use the most central one
                if applicable_splines:
                    applicable_splines.sort(key=lambda x: x[1], reverse=True)
                    best_spline = applicable_splines[0][2]
                    interpolated_points[i, j + 3] = best_spline["interpolator"](
                        julian_date
                    )
                else:
                    # If no spline's range contains this point, use the closest one
                    if julian_date < start_time:
                        interpolated_points[i, j + 3] = splines[0]["interpolator"](
                            julian_date
                        )
                    else:
                        interpolated_points[i, j + 3] = splines[-1]["interpolator"](
                            julian_date
                        )

    return interpolated_points


def reconstruct_covariance_at_time(interpolated_points: np.ndarray) -> tuple:
    """
    Reconstruct the mean state and covariance matrix from interpolated
    sigma points using the Unscented Transform.

    This function implements the Unscented Transform to reconstruct the mean state
    and covariance matrix from a set of interpolated sigma points. It uses
    optimized parameters for numerical stability and accuracy in the presence
    of non-linear transformations.

    The function uses the following Unscented Transform parameters:
    - alpha = 0.001: Reduced for better numerical stability
    - beta = 2.0: Optimal for Gaussian distributions
    - kappa = 3-n: Modified for better stability
    - lambda = alpha²(n+kappa) - n: Scaling parameter

    Args:
        interpolated_points (np.ndarray): Array of shape (13, 6) containing
        the interpolated sigma points, where:
            - 13 rows: One row per sigma point (1 mean + 6 positive + 6
            negative Cholesky points)
            - 6 columns: [x, y, z, vx, vy, vz] state components
            - dtype: np.float64 for high precision

    Returns:
        tuple: (mean_state, covariance) where:
            - mean_state (np.ndarray): Array of shape (6,) containing the
            mean state vector
            - covariance (np.ndarray): Array of shape (6, 6) containing the
            symmetric covariance matrix

    Note:
        - The mean state is taken directly from the first sigma point for stability
        - The covariance matrix is computed using weighted outer products
        - The final covariance matrix is symmetrized to ensure numerical stability
        - All calculations are performed in double precision (np.float64)
    """
    # Optimized Unscented Transform parameters
    n = 6
    alpha = np.float64(0.001)  # Reduced alpha for better numerical stability
    beta = np.float64(2.0)  # Optimal for Gaussian
    kappa = np.float64(3 - n)  # Modified for better stability
    lambda_param = alpha * alpha * (n + kappa) - n

    w0_m = lambda_param / (n + lambda_param)
    wn_m = np.float64(0.5) / (n + lambda_param)
    w0_c = w0_m + (1 - alpha * alpha + beta)
    wn_c = wn_m

    mean_state = interpolated_points[0].copy()  # Copy to ensure it's a new array

    # Calculate covariance with improved numerical stability
    diff_0 = interpolated_points[0] - mean_state
    covariance = w0_c * np.outer(diff_0, diff_0)

    for i in range(1, len(interpolated_points)):
        diff = interpolated_points[i] - mean_state
        covariance += wn_c * np.outer(diff, diff)

    covariance = (covariance + covariance.T) / 2

    return mean_state, covariance
