# ruff: noqa: S101
from datetime import datetime, timezone

import numpy as np

from api.domain.models.interpolable_ephemeris import (
    EphemerisPoint,
    InterpolableEphemeris,
)


def test_ephemeris_point_equality():
    """Test equality comparison between EphemerisPoints."""
    timestamp = datetime(2024, 1, 1, tzinfo=timezone.utc)
    position = np.array([1.0, 2.0, 3.0])
    velocity = np.array([0.1, 0.2, 0.3])
    covariance = np.eye(6)

    point1 = EphemerisPoint(timestamp, position, velocity, covariance)
    point2 = EphemerisPoint(timestamp, position, velocity, covariance)
    point3 = EphemerisPoint(
        datetime(2024, 1, 2, tzinfo=timezone.utc), position, velocity, covariance
    )

    assert point1 == point2
    assert point1 != point3
    assert point1 != "not an EphemerisPoint"


def test_interpolable_ephemeris_equality():
    """Test equality comparison between InterpolableEphemeris objects."""
    sat_id = 12345
    generated_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    data_source = "test_source"
    frame = "UVW"
    points = [
        EphemerisPoint(
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            np.array([1.0, 2.0, 3.0]),
            np.array([0.1, 0.2, 0.3]),
            np.eye(6),
        )
    ]
    ephemeris_start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    ephemeris_stop = datetime(2024, 1, 2, tzinfo=timezone.utc)
    date_collected = datetime(2024, 1, 1, tzinfo=timezone.utc)

    ephemeris1 = InterpolableEphemeris(
        satellite=sat_id,
        generated_at=generated_at,
        data_source=data_source,
        frame=frame,
        points=points,
        ephemeris_start=ephemeris_start,
        ephemeris_stop=ephemeris_stop,
        date_collected=date_collected,
    )

    ephemeris2 = InterpolableEphemeris(
        satellite=sat_id,
        generated_at=generated_at,
        data_source=data_source,
        frame=frame,
        points=points,
        ephemeris_start=ephemeris_start,
        ephemeris_stop=ephemeris_stop,
        date_collected=date_collected,
    )

    ephemeris3 = InterpolableEphemeris(
        satellite=54321,  # Different sat_id
        generated_at=generated_at,
        data_source=data_source,
        frame=frame,
        points=points,
        ephemeris_start=ephemeris_start,
        ephemeris_stop=ephemeris_stop,
        date_collected=date_collected,
    )

    assert ephemeris1 == ephemeris2
    assert ephemeris1 != ephemeris3
    assert ephemeris1 != "not an InterpolableEphemeris"


def test_interpolable_ephemeris_repr():
    """Test string representation of InterpolableEphemeris."""
    sat_id = 12345
    generated_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    data_source = "test_source"
    frame = "UVW"
    points = [
        EphemerisPoint(
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            np.array([1.0, 2.0, 3.0]),
            np.array([0.1, 0.2, 0.3]),
            np.eye(6),
        )
    ]
    ephemeris_start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    ephemeris_stop = datetime(2024, 1, 2, tzinfo=timezone.utc)

    ephemeris = InterpolableEphemeris(
        satellite=sat_id,
        generated_at=generated_at,
        data_source=data_source,
        frame=frame,
        points=points,
        ephemeris_start=ephemeris_start,
        ephemeris_stop=ephemeris_stop,
    )

    expected_repr = (
        f"<InterpolableEphemeris satellite={sat_id} generated_at={generated_at}>"
    )
    assert repr(ephemeris) == expected_repr


def test_interpolable_ephemeris_default_date_collected():
    """Test that date_collected defaults to current UTC time if not provided."""
    sat_id = 12345
    generated_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    data_source = "test_source"
    frame = "UVW"
    points = [
        EphemerisPoint(
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            np.array([1.0, 2.0, 3.0]),
            np.array([0.1, 0.2, 0.3]),
            np.eye(6),
        )
    ]
    ephemeris_start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    ephemeris_stop = datetime(2024, 1, 2, tzinfo=timezone.utc)

    ephemeris = InterpolableEphemeris(
        satellite=sat_id,
        generated_at=generated_at,
        data_source=data_source,
        frame=frame,
        points=points,
        ephemeris_start=ephemeris_start,
        ephemeris_stop=ephemeris_stop,
    )

    assert isinstance(ephemeris.date_collected, datetime)
    assert ephemeris.date_collected.tzinfo == timezone.utc
    assert ephemeris.date_collected <= datetime.now(timezone.utc)
