from datetime import datetime

from api.adapters.repositories.satellite_repository import AbstractSatelliteRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository


def get_tle_data(
    tle_repo: AbstractTLERepository,
    id: str,
    id_type: str,
    start_date: datetime,
    end_date: datetime,
    api_source: str,
    api_version: str,
):
    """
    Fetches Two-Line Element set (TLE) data for a given satellite.

    This function retrieves TLE data from either the NORAD ID or satellite name
    provided. It allows for a date range to be specified for the TLE data, and if
    not provided, it will return all TLE data for the satellite.

    Parameters:
        tle_repo (AbstractTLERepository):
            The repository instance used to fetch TLE data.
        id (str):
            The identifier for the satellite.
        id_type (str):
            The type of the ID, either 'catalog' (NORAD ID) or 'name'.
        start_date (datetime):
            The start date of the date range for the TLE data.
        end_date (datetime):
            The end date of the date range for the TLE data.

    Returns:
        List[dict]:
            A list containing the TLE data for the specified
            satellite and date range. Each data point includes the satellite
            name, satellite ID, TLE lines, epoch, date collected, and data source.
    """

    tles = (
        tle_repo.get_all_for_date_range_by_satellite_number(id, start_date, end_date)
        if id_type == "catalog"
        else tle_repo.get_all_for_date_range_by_satellite_name(id, start_date, end_date)
    )

    # Extract the TLE data from the result set
    tle_data = [
        {
            "satellite_name": tle.satellite.sat_name,
            "satellite_id": tle.satellite.sat_number,
            "tle_line1": tle.tle_line1,
            "tle_line2": tle.tle_line2,
            "epoch": tle.epoch.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "date_collected": tle.date_collected.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "data_source": tle.data_source,
        }
        for tle in tles
    ]
    return tle_data


def get_satellite_data(
    sat_repo: AbstractSatelliteRepository,
    id: str,
    id_type: str,
    api_source: str,
    api_version: str,
):
    satellite = (
        sat_repo.get_satellite_data_by_id(id)
        if id_type == "catalog"
        else sat_repo.get_satellite_data_by_name(id)
    )

    if satellite is None:
        return []

    satellite_data = [
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
    ]

    return satellite_data


def get_recent_tle_set(
    tle_repo: AbstractTLERepository, api_source: str, api_version: str
):
    tles = tle_repo.get_most_recent_full_tle_set()

    # Extract the TLE data from the result set
    tle_data = [
        {
            "satellite_name": tle.satellite.sat_name,
            "satellite_id": tle.satellite.sat_number,
            "tle_line1": tle.tle_line1,
            "tle_line2": tle.tle_line2,
            "epoch": tle.epoch.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "date_collected": tle.date_collected.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "data_source": tle.data_source,
        }
        for tle in tles
    ]

    json_results = [
        {
            "count": len(tles),
            "data": tle_data,
            "source": api_source,
            "version": api_version,
        }
    ]
    return json_results


def get_ids_for_satellite_name(
    sat_repo: AbstractSatelliteRepository,
    satellite_name: str,
    api_source: str,
    api_version: str,
):
    """
    Fetches NORAD IDs associated with a given satellite name.

    Parameters:
        sat_repo (AbstractSatelliteRepository):
            The repository instance used to fetch satellite data.
        satellite_name (str):
            The name of the satellite.

    Returns:
        List[dict]:
            A list of dictionaries containing the satellite name, NORAD ID,
            date added, and whether it is the current version. Each dictionary
            includes the following keys:
                - "name": The name of the satellite.
                - "norad_id": The NORAD ID of the satellite.
                - "date_added": The date the NORAD ID was added.
                - "is_current_version": A boolean indicating if it is the current
                    version.
    """

    satellite_ids_dates = sat_repo.get_norad_ids_from_satellite_name(satellite_name)

    ids_and_dates = [
        {
            "name": satellite_name,
            "norad_id": id_date[0],
            "date_added": id_date[1].strftime("%Y-%m-%d %H:%M:%S %Z"),
            "is_current_version": id_date[2],
        }
        for id_date in satellite_ids_dates
    ]

    return ids_and_dates


def get_names_for_satellite_id(
    sat_repo: AbstractSatelliteRepository,
    satellite_id: str,
    api_source: str,
    api_version: str,
):
    """
    Fetches names associated with a given NORAD ID.

    Parameters:
        sat_repo (AbstractSatelliteRepository):
            The repository instance used to fetch satellite data.
        satellite_id (str):
            The NORAD of the satellite.

    Returns:
        List[dict]:
            A list of dictionaries containing the satellite name, NORAD ID,
            date added, and whether it is the current version. Each dictionary
            includes the following keys:
                - "name": The name of the satellite.
                - "norad_id": The NORAD ID of the satellite.
                - "date_added": The date the NORAD ID was added.
                - "is_current_version": A boolean indicating if it is the current
                    version.
    """
    satellite_names_and_dates = sat_repo.get_satellite_names_from_norad_id(satellite_id)

    names_and_dates = [
        {
            "name": name_date[0],
            "norad_id": satellite_id,
            "date_added": name_date[1].strftime("%Y-%m-%d %H:%M:%S %Z"),
            "is_current_version": name_date[2],
        }
        for name_date in satellite_names_and_dates
    ]
    return names_and_dates
