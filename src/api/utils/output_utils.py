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
