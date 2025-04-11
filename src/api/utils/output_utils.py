from datetime import timezone

import numpy as np
from astropy.time import Time


def position_data_to_json(
    name,
    intl_designator,
    catalog_id,
    date_collected,
    tle_epoch_date,
    data_source,
    results,
    api_source,
    api_version,
    precision_angles=8,
    precision_date=8,
    precision_range=6,
    precision_velocity=12,
):
    """
    Convert API output to JSON format

    Parameters
    ----------
    name: str
        Name of the target satellite
    intl_designator: str
        International Designator/COSPAR ID of the satellite
    catalog_id: str
        Catalog ID of the satellite
    date_collected: datetime
        Date when the data was collected
    tle_epoch_date: datetime
        Date when the TLE was created
    data_source: str
        Source of the data
    results: list
        List of results from the API
    api_source: str
        Source of the API
    version: str
        Version of the API
    precision_angles: int, optional
        Number of digits for angles to be rounded to (default: 8)
    precision_date: int, optional
        Number of digits for Julian Date to be rounded to (default: 8)
    precision_range: int, optional
        Number of digits for range to be rounded to (default: 6)
    precision_velocity: int, optional
        Number of digits for velocity to be rounded to (default: 12)

    Returns
    -------
    dict
        JSON dictionary of the above quantities
    """
    # looking up the numpy round function once instead of multiple times
    # makes things a little faster
    my_round = np.round

    tle_date = format_date(date_collected)

    tle_epoch = format_date(tle_epoch_date)

    fields = [
        "name",
        "catalog_id",
        "julian_date",
        "satellite_gcrs_km",
        "right_ascension_deg",
        "declination_deg",
        "tle_date",
        "dra_cosdec_deg_per_sec",
        "ddec_deg_per_sec",
        "altitude_deg",
        "azimuth_deg",
        "range_km",
        "range_rate_km_per_sec",
        "phase_angle_deg",
        "illuminated",
        "data_source",
        "observer_gcrs_km",
        "international_designator",
        "tle_epoch",
    ]
    data = []
    for result in results:
        (
            ra,
            dec,
            dracosdec,
            ddec,
            alt,
            az,
            r,
            dr,
            phaseangle,
            illuminated,
            satellite_gcrs,
            observer_gcrs,
            time,
        ) = result  # noqa: E501
        data.append(
            [
                name,
                int(catalog_id),
                my_round(time, precision_date) if time is not None else None,
                satellite_gcrs,
                my_round(ra, precision_angles) if ra is not None else None,
                my_round(dec, precision_angles) if dec is not None else None,
                tle_date,
                (
                    my_round(dracosdec, precision_angles)
                    if dracosdec is not None
                    else None
                ),
                my_round(ddec, precision_angles) if ddec is not None else None,
                my_round(alt, precision_angles) if alt is not None else None,
                my_round(az, precision_angles) if az is not None else None,
                my_round(r, precision_range) if r is not None else None,
                my_round(dr, precision_velocity) if dr is not None else None,
                (
                    my_round(phaseangle, precision_angles)
                    if phaseangle is not None
                    else None
                ),
                illuminated,
                data_source,
                observer_gcrs,
                intl_designator,
                tle_epoch,
            ]
        )

    return {
        "count": len(results),
        "fields": fields,
        "data": data,
        "source": api_source,
        "version": api_version,
    }


def fov_data_to_json(
    results: list,
    points_in_fov: int,
    performance_metrics: dict,
    api_source: str,
    api_version: str,
    group_by: str,
    precision_angles=8,
    precision_date=8,
) -> dict:
    """Convert FOV results to JSON format with optional grouping by satellite.

    Args:
        results: List of satellite position results
        points_in_fov: Total number of position points in field of view
        performance_metrics: Dictionary of performance measurements
        api_source: Source of the API
        api_version: Version of the API
        group_by: Grouping strategy ('satellite' or 'time', time by default)
        precision_angles: Decimal precision for angle values
        precision_date: Decimal precision for dates

    Returns:
        dict: Formatted results either grouped by satellite or chronologically
    """
    my_round = np.round

    # Round all results first
    for result in results:
        fields_to_round = list(
            result.items()
        )  # Create a static list of items to iterate
        for field, value in fields_to_round:
            if value is None:
                continue
            if field in ["ra", "dec", "altitude", "azimuth", "angle", "range_km"]:
                result[field] = my_round(value, precision_angles)
            elif field == "julian_date":
                result[field] = my_round(value, precision_date)
                result["date_time"] = format_date(
                    Time(value, format="jd").to_datetime()
                )

    if group_by == "satellite":
        # Group passes by satellite
        # need to account for different satellites with the same name (usually debris)
        # but different NORAD IDs
        satellites = {}
        for result in results:
            sat_name = result["name"]
            sat_norad_id = result["norad_id"]
            sat_key = f"{sat_name} ({sat_norad_id})"

            if sat_key not in satellites:
                # Create base satellite dictionary
                satellite_dict = {
                    "name": sat_name,
                    "norad_id": sat_norad_id,
                    "positions": [],
                }

                # Only add tle_data if it's not null/empty
                tle_data = result.get("tle_data")
                if tle_data is not None and tle_data != {}:
                    satellite_dict["tle_data"] = tle_data

                satellites[sat_key] = satellite_dict
            # Add pass data without redundant satellite info
            pass_data = {
                "ra": result["ra"],
                "dec": result["dec"],
                "altitude": result["altitude"],
                "azimuth": result["azimuth"],
                "julian_date": result["julian_date"],
                "date_time": format_date(result.get("date_time")),
                "angle": result.get("angle"),
                "range_km": result.get("range_km"),
                "tle_epoch": result.get("tle_epoch"),
            }
            satellites[sat_key]["positions"].append(pass_data)

        formatted_results = {
            "data": {
                "satellites": satellites,
                "total_satellites": len(satellites),
                "total_position_results": points_in_fov,
            },
            "performance": performance_metrics,
            "source": api_source,
            "version": api_version,
        }
    else:
        # Original chronological format
        formatted_results = {
            "data": results,
            "count": len(results),
            "performance": performance_metrics,
            "source": api_source,
            "version": api_version,
        }

    return formatted_results


def format_date(date):
    """
    Format a datetime object into a standardized string format.

    Args:
        date: A datetime object to format, or None

    Returns:
        A formatted date string in the format 'YYYY-MM-DD HH:MM:SS TZ' if date is
        provided, otherwise returns None

    Example:
        >>> format_date(datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc))
        '2024-01-01 12:00:00 UTC'
    """
    if date is None:
        return None

    if isinstance(date, str):
        return date

    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)

    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S %Z")

    return formatted_date
