import csv
import io
import zipfile
from collections.abc import Iterator
from datetime import timezone
from typing import Any

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from astropy.time import Time

from api.domain.models.interpolable_ephemeris import InterpolableEphemeris


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
        "sat_altitude_km",
        "solar_elevation_deg",
        "solar_azimuth_deg",
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
            sat_altitude_km,
            solar_elevation_deg,
            solar_azimuth_deg,
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
                (
                    my_round(sat_altitude_km, precision_range)
                    if sat_altitude_km is not None
                    else None
                ),
                (
                    my_round(solar_elevation_deg, precision_angles)
                    if solar_elevation_deg is not None
                    else None
                ),
                (
                    my_round(solar_azimuth_deg, precision_angles)
                    if solar_azimuth_deg is not None
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
    results: list[dict[str, Any]],
    points_in_fov: int,
    performance_metrics: dict[str, Any],
    api_source: str,
    api_version: str,
    group_by: str,
    precision_angles=8,
    precision_date=8,
) -> dict[str, Any]:
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
            if field in [
                "ra",
                "dec",
                "altitude",
                "azimuth",
                "angle",
                "range_km",
                "apparent_magnitude",
            ]:
                result[field] = my_round(value, precision_angles)
            elif field == "julian_date":
                result[field] = my_round(value, precision_date)
                result["date_time"] = format_date(
                    Time(value, format="jd").to_datetime()
                )
    formatted_results: dict[str, Any]

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
                tle_data = result.get("orbital_data")
                if tle_data is not None and tle_data != {}:
                    satellite_dict["orbital_data"] = tle_data

                satellites[sat_key] = satellite_dict
            # Add pass data without redundant satellite info
            covariance = result.get("covariance")
            if covariance is not None and hasattr(covariance, "tolist"):
                covariance = covariance.tolist()

            pass_data = {
                "ra": result["ra"],
                "dec": result["dec"],
                "covariance": covariance,
                "altitude": result.get("altitude"),
                "azimuth": result.get("azimuth"),
                "julian_date": result.get("julian_date"),
                "date_time": format_date(result.get("date_time")),
                "angle": result.get("angle"),
                "range_km": result.get("range_km"),
                "orbital_data_epoch": result.get("orbital_data_epoch"),
                "orbital_data_source": result.get("orbital_data_source"),
            }
            if "apparent_magnitude" in result:
                pass_data["apparent_magnitude"] = result["apparent_magnitude"]
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
        sorted_results = sorted(results, key=lambda x: x.get("julian_date", 0))

        formatted_results = {
            "data": sorted_results,
            "total_position_results": points_in_fov,
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


def satellite_data_to_json(satellites: list, api_source: str, api_version: str) -> dict:
    """
    Convert satellite data to JSON format

    Args:
        satellites: List of satellites
        api_source: Source of the API
        api_version: Version of the API

    Returns:
        dict: JSON dictionary of the satellite data
    """
    satellite_list = [
        {
            "satellite_name": satellite.sat_name,
            "satellite_id": satellite.sat_number,
            "international_designator": satellite.object_id,
            "rcs_size": satellite.rcs_size,
            "launch_date": (
                satellite.launch_date.strftime("%Y-%m-%d")
                if satellite.launch_date
                else None
            ),
            "decay_date": (
                satellite.decay_date.strftime("%Y-%m-%d")
                if satellite.decay_date
                else None
            ),
            "object_type": satellite.object_type,
        }
        for satellite in satellites
    ]
    return {
        "count": len(satellite_list),
        "data": satellite_list,
        "source": api_source,
        "version": api_version,
    }


# Column order for the flattened CSV output (one row per point) - separate
# from the Parquet schema because CSV can't hold list-valued cells cleanly
EPHEMERIS_CSV_COLUMNS: list[str] = [
    "satellite_name",
    "satellite_id",
    "ephemeris_id",
    "data_source",
    "frame",
    "generated_at",
    "timestamp",
    "x_km",
    "y_km",
    "z_km",
    "vx_km_per_s",
    "vy_km_per_s",
    "vz_km_per_s",
] + [f"cov_{i}_{j}" for i in range(6) for j in range(6)]

# Column order for the Parquet output. This mirrors the on-disk S3 schema
# (position/velocity/covariance as list<double>, native timestamps) so the file
# stays compact - list columns are ~50% smaller than the flattened form - and
# consistent with the stored shards, plus a few satellite identifier columns so
# the file is self-describing outside the database.
EPHEMERIS_PARQUET_COLUMNS: list[str] = [
    "ephemeris_id",
    "satellite_id",
    "satellite_name",
    "data_source",
    "frame",
    "generated_at",
    "timestamp",
    "position",
    "velocity",
    "covariance",
]


def _ephemeris_csv_rows(
    records: list[InterpolableEphemeris],
) -> Iterator[dict[str, Any]]:
    """Yield one flattened row per stored ephemeris point across the given records."""
    for ephemeris in records:
        sat = ephemeris.satellite
        generated_at = format_date(ephemeris.generated_at)
        for point in ephemeris.points:
            pos = np.asarray(point.position, dtype=float).reshape(-1)
            vel = np.asarray(point.velocity, dtype=float).reshape(-1)
            cov = np.asarray(point.covariance, dtype=float).reshape(6, 6)
            row: dict[str, Any] = {
                "satellite_name": sat.sat_name,
                "satellite_id": sat.sat_number,
                "ephemeris_id": ephemeris.id,
                "data_source": ephemeris.data_source,
                "frame": ephemeris.frame,
                "generated_at": generated_at,
                "timestamp": format_date(point.timestamp),
                "x_km": pos[0],
                "y_km": pos[1],
                "z_km": pos[2],
                "vx_km_per_s": vel[0],
                "vy_km_per_s": vel[1],
                "vz_km_per_s": vel[2],
            }
            for i in range(6):
                for j in range(6):
                    row[f"cov_{i}_{j}"] = cov[i, j]
            yield row


def ephemeris_data_to_parquet(records: list[InterpolableEphemeris]) -> io.BytesIO:
    """Serialize ephemeris points into a single zstd-compressed Parquet file.

    Uses the compact S3-aligned schema: position, velocity, and covariance stay as
    ``list<double>`` columns and timestamps keep their native type.
    """
    columns: dict[str, list[Any]] = {name: [] for name in EPHEMERIS_PARQUET_COLUMNS}
    for ephemeris in records:
        sat = ephemeris.satellite
        for point in ephemeris.points:
            columns["ephemeris_id"].append(ephemeris.id)
            columns["satellite_id"].append(sat.sat_number)
            columns["satellite_name"].append(sat.sat_name)
            columns["data_source"].append(ephemeris.data_source)
            columns["frame"].append(ephemeris.frame)
            columns["generated_at"].append(ephemeris.generated_at)
            columns["timestamp"].append(point.timestamp)
            columns["position"].append(
                np.asarray(point.position, dtype=float).reshape(-1).tolist()
            )
            columns["velocity"].append(
                np.asarray(point.velocity, dtype=float).reshape(-1).tolist()
            )
            columns["covariance"].append(
                np.asarray(point.covariance, dtype=float).reshape(-1).tolist()
            )

    table = pa.table(columns)
    buffer = io.BytesIO()
    pq.write_table(table, buffer, compression="zstd")
    buffer.seek(0)
    return buffer


def ephemeris_data_to_zip(records: list[InterpolableEphemeris]) -> io.BytesIO:
    """Serialize ephemeris points into a zip archive with one CSV per satellite."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for ephemeris in records:
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(EPHEMERIS_CSV_COLUMNS)
            for row in _ephemeris_csv_rows([ephemeris]):
                writer.writerow([row[name] for name in EPHEMERIS_CSV_COLUMNS])
            zip_file.writestr(
                f"{ephemeris.satellite.sat_number}.csv", csv_buffer.getvalue()
            )
    zip_buffer.seek(0)
    return zip_buffer
