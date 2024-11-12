import numpy as np


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

    tle_date = (
        date_collected.strftime("%Y-%m-%d %H:%M:%S %Z")
        if date_collected is not None
        else date_collected
    )

    tle_epoch = (
        tle_epoch_date.strftime("%Y-%m-%d %H:%M:%S %Z")
        if tle_epoch_date is not None
        else tle_epoch_date
    )

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
    satellites_processed: int,
    total_satellites: int,
    points_in_fov: int,
    performance_metrics: dict,
    api_source: str,
    api_version: str,
    group_by: str,
    precision_angles=8,
    precision_date=8,
) -> dict:
    """Convert FOV results to JSON format with optional grouping by satellite."""
    my_round = np.round

    if group_by == "satellite":
        # Group passes by satellite
        satellites = {}
        for result in results:
            sat_name = result["name"]
            if sat_name not in satellites:
                satellites[sat_name] = {"norad_id": result["norad_id"], "positions": []}
            # Add pass data without redundant satellite info
            pass_data = {
                "ra": (
                    my_round(result["ra"], precision_angles)
                    if result["ra"] is not None
                    else None
                ),
                "dec": (
                    my_round(result["dec"], precision_angles)
                    if result["dec"] is not None
                    else None
                ),
                "altitude": (
                    my_round(result["altitude"], precision_angles)
                    if result["altitude"] is not None
                    else None
                ),
                "azimuth": (
                    my_round(result["azimuth"], precision_angles)
                    if result["azimuth"] is not None
                    else None
                ),
                "julian_date": (
                    my_round(result["julian_date"], precision_date)
                    if result["julian_date"] is not None
                    else None
                ),
                "angle": (
                    my_round(result["angle"], precision_angles)
                    if result["angle"] is not None
                    else None
                ),
            }
            satellites[sat_name]["positions"].append(pass_data)

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
