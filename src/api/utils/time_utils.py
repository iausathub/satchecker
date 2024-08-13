import numpy as np


def jd_to_gst(jd: float, nutation: float) -> float:
    """
    Convert Julian Day (JD) to Greenwich Apparent Sidereal Time (GAST).

    This function calculates the GAST based on the JD and nutation.

    Args:
        jd (float): The Julian Day.
        nutation (float): The nutation in degrees.

    Returns:
        float: The GAST in radians.
    """
    # Approximate Delta T (in days)
    delta_t_days = 32.184 / (24 * 60 * 60)

    # Convert JD(UT) to JD(TT)
    jd_tt = jd + delta_t_days
    # Julian centuries since J2000.0
    t = (jd_tt - 2451545.0) / 36525.0

    # Greenwich Mean Sidereal Time (GMST) at 0h UT
    theta_gmst = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * t**2
        - t**3 / 38710000.0
    )

    # Wrap GMST to [0, 360) range
    theta_gmst = theta_gmst % 360

    # Convert nutation from arcseconds to degrees
    # nutation = nutation / 3600

    # Calculate Greenwich Apparent Sidereal Time (GAST)
    theta_gast = theta_gmst + nutation

    # Wrap GAST to [0, 360) range
    theta_gast = theta_gast % 360

    # Convert to radians
    theta_gast = np.deg2rad(theta_gast)

    return theta_gast


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

    return lst
