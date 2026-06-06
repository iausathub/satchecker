"""Frame conversions for operator ephemeris used in TLE fitting."""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np
from astropy import units as u
from astropy.coordinates import (
    GCRS,
    TEME,
    CartesianRepresentation,
)
from astropy.time import Time

# Inertial position-frame labels for operator ephemeris data. SGP4 propagators
# output TEME, so vectors in these frames are rotated GCRS→TEME before TLE
# least-squares residuals are evaluated.
OPERATOR_POSITION_FRAMES = frozenset({"MEME", "GCRS", "ICRF"})
TEME_FRAME_LABELS = frozenset({"TEME"})

# Known frame labels that are NOT inertial Cartesian (Earth-fixed, covariance,
# etc.).  Passing one of these to needs_operator_to_teme_conversion raises
# rather than silently applying the wrong rotation.
_UNSUPPORTED_FRAMES = frozenset({"ITRF", "ECEF", "IERS", "UVW"})


def operator_position_frame_from_filename(filename: str) -> str:
    """Infer stored position frame from a Starlink operator ephemeris filename.

    MEME-labeled files carry inertial Cartesian positions compatible with
    GCRS.  All other operator files are also treated as GCRS (the UVW label
    in line 4 identifies the *covariance* frame, not the position frame).
    """
    upper = filename.upper()
    if "MEME_" in upper or upper.startswith("MEME"):
        return "MEME"
    return "GCRS"


def needs_operator_to_teme_conversion(frame: str | None) -> bool:
    """Return True when positions must be rotated into SGP4 TEME before fitting.

    Args:
        frame: Stored frame label.  ``None`` is treated as GCRS/inertial
            (caller did not record the frame; assume operator default).

    Raises:
        ValueError: If *frame* is a known but unsupported label (e.g. an
            Earth-fixed or covariance frame) that cannot be handled by the
            GCRS→TEME path.
    """
    if frame is None:
        return True
    normalized = frame.strip().upper()
    if normalized in TEME_FRAME_LABELS:
        return False
    if normalized in _UNSUPPORTED_FRAMES:
        raise ValueError(
            f"Frame '{frame}' is not supported for TEME conversion. "
            "Earth-fixed and covariance frames (ITRF, ECEF, UVW, RIC, RTN) "
            "require a separate transformation path."
        )
    if normalized in OPERATOR_POSITION_FRAMES:
        return True
    raise ValueError(
        f"Unrecognized frame label '{frame}'. Expected one of "
        f"{sorted(OPERATOR_POSITION_FRAMES | TEME_FRAME_LABELS)} or None."
    )


def _as_utc_datetime(timestamp: datetime) -> datetime:
    """Return *timestamp* as a UTC-aware datetime.

    The caller is responsible for ensuring that naive datetimes genuinely
    represent UTC.  A naive timestamp is *not* assumed to be local time.
    """
    if timestamp.tzinfo is None:
        # Treat as UTC — the caller must guarantee this.
        return timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc)


def operator_position_km_to_teme(
    position_km: np.ndarray,
    timestamp: datetime,
) -> np.ndarray:
    """
    Convert one operator position vector into Vallado/astropy TEME (km).

    Starlink MEME-file positions are treated as GCRS/ICRF-compatible inertial
    Cartesian coordinates, then transformed to TEME to match ``sgp4`` output.
    """
    pos = np.asarray(position_km, dtype=np.float64).reshape(3)
    obstime = Time(_as_utc_datetime(timestamp), format="datetime", scale="utc")
    gcrs = GCRS(CartesianRepresentation(pos * u.km), obstime=obstime)
    teme = gcrs.transform_to(TEME(obstime=obstime))
    return np.asarray(teme.cartesian.xyz.to(u.km).value, dtype=np.float64)


def operator_positions_km_to_teme(
    positions_km: np.ndarray,
    timestamps: list[datetime],
    *,
    frame: str | None,
) -> np.ndarray:
    """
    Convert a stack of operator positions for TLE least-squares residuals.

    Args:
        positions_km: Shape ``(N, 3)`` in the operator/stored frame (km).
        timestamps: UTC timestamps, one per row.  Naive datetimes are assumed
            to be UTC.
        frame: Stored frame label (``MEME``, ``GCRS``, ``ICRF``, or ``TEME``).

    Returns:
        Shape ``(N, 3)`` positions in TEME (km).

    Raises:
        ValueError: On shape mismatch, length mismatch, or an unsupported /
            unrecognized frame label.
    """
    if positions_km.ndim != 2 or positions_km.shape[1] != 3:
        raise ValueError("positions_km must have shape (N, 3)")
    if len(timestamps) != len(positions_km):
        raise ValueError("timestamps length must match positions_km rows")
    if not needs_operator_to_teme_conversion(frame):
        return np.asarray(positions_km, dtype=np.float64)

    obstimes = Time(
        [_as_utc_datetime(ts) for ts in timestamps],
        format="datetime",
        scale="utc",
    )
    pos_arr = np.asarray(positions_km, dtype=np.float64)

    # Vectorised GCRS → TEME: one astropy call for the whole arc.
    cartesian = CartesianRepresentation(pos_arr.T * u.km)
    gcrs = GCRS(cartesian, obstime=obstimes)
    teme = gcrs.transform_to(TEME(obstime=obstimes))
    return np.asarray(teme.cartesian.xyz.to(u.km).value, dtype=np.float64).T
