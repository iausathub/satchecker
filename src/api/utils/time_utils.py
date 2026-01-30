from datetime import datetime, timezone
from typing import Any

import numpy as np
from astropy.time import Time
from astropy.utils.iers import IERS_Auto


def jd_to_mjd(jd: float) -> float:
    """Convert Julian Day to Modified Julian Day."""
    return jd - 2400000.5


def get_ut1_utc(jd_utc: float) -> float:
    """
    Get UT1-UTC value for a given JD using IERS (Bulletin A/B).

    Uses Astropy's IERS_Auto table, which interpolates from the official
    Earth orientation data (and auto-downloads if needed).

    Args:
        jd_utc (float): Julian Day in UTC

    Returns:
        float: UT1-UTC in seconds
    """
    iers = IERS_Auto.open()
    # returns a Quantity in seconds
    result = iers.ut1_utc(jd_utc, 0.0)
    return float(result.to_value("s"))


def jd_to_gst(jd_utc: float, nutation: float) -> float:
    """
    Convert Julian Day (UTC) to Greenwich Apparent Sidereal Time (GAST).

    Args:
        jd_utc (float): The Julian Day in UTC time scale.
        nutation (float): The equation of the equinoxes in degrees.

    Returns:
        float: The GAST in radians.
    """
    # Get UT1-UTC from Bulletin A
    ut1_utc_seconds = get_ut1_utc(jd_utc)  # Lookup from bulletin

    # Convert UTC to UT1 (for GMST calculation)
    jd_ut1 = jd_utc + ut1_utc_seconds / 86400.0

    # Convert UTC to TT (for the polynomial time parameter)
    delta_t_utc_to_tt = 69.184  # TT - UTC (constant)
    jd_tt = jd_utc + delta_t_utc_to_tt / 86400.0

    # Julian centuries since J2000.0 (in TT)
    t = (jd_tt - 2451545.0) / 36525.0

    # GMST calculation uses UT1
    theta_gmst = (
        280.46061837
        + 360.98564736629 * (jd_ut1 - 2451545.0)  # Use UT1
        + 0.000387933 * t**2  # Higher order terms use TT
        - t**3 / 38710000.0
    )

    # Wrap GMST to [0, 360) range
    theta_gmst = theta_gmst % 360

    # Calculate GAST
    theta_gast = theta_gmst + nutation

    # Wrap GAST to [0, 360) range
    theta_gast = theta_gast % 360

    # Convert to radians
    theta_gast = np.deg2rad(theta_gast)

    return float(theta_gast)


def calculate_lst(longitude: float, jd: float) -> float:
    """
    Calculate Local Sidereal Time (LST) based on longitude and Julian Day (JD).

    This function calculates the Greenwich Sidereal Time (GST) and then adjusts it
    based on the given longitude to calculate the LST.

    Args:
        longitude (float): The longitude in degrees.
        jd (float): The Julian Day.

    Returns:
        float: The LST in radians.
    """
    # Calculate the Julian centuries since J2000.0
    T = (jd - 2451545.0) / 36525.0  # noqa: N806

    # Calculate the GST in degrees
    gst = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * T**2
        - T**3 / 38710000.0
    )

    # Convert GST to range 0-360
    gst = gst % 360

    longitude = longitude * np.pi / 180.0  # Convert longitude to radians
    # Convert longitude to degrees
    longitude_deg = longitude * 180.0 / np.pi

    # Calculate LST in degrees
    lst_deg = gst + longitude_deg

    # Convert LST to range 0-360
    lst_deg = lst_deg % 360

    # Convert LST from degrees to radians
    lst = np.radians(lst_deg)

    # Ensure we return a Python float, not a NumPy type
    return float(lst)


def astropy_time_to_datetime_utc(time_obj: Time) -> datetime:
    """
    Convert an astropy Time object to a timezone-aware Python datetime (UTC).

    Args:
        time_obj: Astropy Time object to convert

    Returns:
        datetime.datetime object with UTC timezone
    """
    # Make sure the time object is in UTC scale before converting
    # to datetime with timezone
    if time_obj.scale != "utc":
        time_obj = time_obj.utc

    # Explicitly cast to datetime to satisfy the type checker
    dt: datetime = time_obj.to_datetime(timezone=timezone.utc)
    return dt


def ensure_datetime(date_value: Any) -> datetime:
    """
    Ensure that the input is a datetime object with timezone info.

    Args:
        date_value: A datetime object, string representing a date/time, or
        Julian date float

    Returns:
        A datetime object with timezone info

    Raises:
        TypeError: If the input cannot be converted to a datetime object
    """
    if isinstance(date_value, (float, np.floating)):
        # Convert Julian date to datetime
        time_obj = Time(date_value, format="jd", scale="utc")
        return astropy_time_to_datetime_utc(time_obj)
    elif isinstance(date_value, str):
        try:
            # Try to parse the string as a datetime in ISO format
            date_value = datetime.fromisoformat(date_value.replace("Z", "+00:00"))
        except ValueError:
            date_value = datetime.strptime(date_value, "%Y-%m-%d")

    # Ensure the result is actually a datetime
    if not isinstance(date_value, datetime):
        raise TypeError(f"Cannot convert {type(date_value)} to datetime")

    # Ensure the datetime has timezone info
    if date_value.tzinfo is None:
        date_value = date_value.replace(tzinfo=timezone.utc)

    return date_value
