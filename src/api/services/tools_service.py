import csv
import io
import logging
import zipfile
from datetime import datetime
from typing import Any

from api.adapters.repositories.satellite_repository import AbstractSatelliteRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.utils.output_utils import format_date, satellite_data_to_json

logger = logging.getLogger(__name__)


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
    logger.info(f"Fetching TLE data for {id_type} ID: {id}")
    logger.info(f"Date range: {start_date} to {end_date}")

    try:
        tles = (
            tle_repo.get_all_for_date_range_by_satellite_number(
                id, start_date, end_date
            )
            if id_type == "catalog"
            else tle_repo.get_all_for_date_range_by_satellite_name(
                id, start_date, end_date
            )
        )
        logger.info(f"Retrieved {len(tles)} TLEs")
    except Exception as e:
        logger.error(f"Failed to retrieve TLEs: {str(e)}", exc_info=True)
        raise

    # Extract the TLE data from the result set
    try:
        tle_data = [
            {
                "satellite_name": tle.satellite.sat_name,
                "satellite_id": tle.satellite.sat_number,
                "tle_line1": tle.tle_line1,
                "tle_line2": tle.tle_line2,
                "epoch": format_date(tle.epoch),
                "date_collected": format_date(tle.date_collected),
                "data_source": tle.data_source,
            }
            for tle in tles
        ]
        logger.info(f"Successfully formatted {len(tle_data)} TLE records")
    except Exception as e:
        logger.error(f"Failed to format TLE data: {str(e)}", exc_info=True)
        raise

    results = {
        "count": len(tle_data),
        "data": tle_data,
        "source": api_source,
        "version": api_version,
    }

    return results


def get_tles_around_epoch_results(
    tle_repo: AbstractTLERepository,
    id: str,
    id_type: str,
    epoch: datetime,
    count_before: int,
    count_after: int,
    api_source: str,
    api_version: str,
):
    """
    Fetches TLEs around a specific epoch date.

    This function retrieves TLEs from the repository that are around the specified
    epoch date. It allows for a count of TLEs to be specified before and after
    the epoch date.

    Parameters:
        tle_repo (AbstractTLERepository): The repository to fetch TLE data from.
        id (str): The ID of the satellite.
        id_type (str): The type of the ID, either "catalog" or "name".
        epoch (datetime): The epoch date to fetch TLEs around.
        count_before (int): The number of TLEs to fetch before the epoch date.
        count_after (int): The number of TLEs to fetch after the epoch date.

    Returns:
        List[dict]: A list of dictionaries containing the TLE data.
    """
    logger.info(f"Fetching TLEs around epoch {epoch} for {id_type} ID: {id}")
    logger.info(
        f"Requesting {count_before} TLEs before and {count_after} TLEs after epoch"
    )

    try:
        tles_result = tle_repo.get_tles_around_epoch(
            id, id_type, epoch, count_before, count_after
        )
        logger.info("Successfully retrieved TLEs from repository")
    except Exception as e:
        logger.error(
            f"Failed to retrieve TLEs from repository: {str(e)}", exc_info=True
        )
        raise

    # Ensure tles is a list to avoid iteration errors
    tles = (
        []
        if tles_result is None
        else tles_result if isinstance(tles_result, list) else [tles_result]
    )
    logger.info(f"Processing {len(tles)} TLE records")

    try:
        # Extract the TLE data from the result set
        tle_data = [
            {
                "satellite_name": tle.satellite.sat_name,
                "satellite_id": tle.satellite.sat_number,
                "tle_line1": tle.tle_line1,
                "tle_line2": tle.tle_line2,
                "epoch": format_date(tle.epoch),
                "date_collected": format_date(tle.date_collected),
                "data_source": tle.data_source,
            }
            for tle in tles
        ]
        logger.info(f"Successfully formatted {len(tle_data)} TLE records")
    except Exception as e:
        logger.error(f"Failed to format TLE data: {str(e)}", exc_info=True)
        raise

    return [
        {
            "tle_data": tle_data,
            "source": api_source,
            "version": api_version,
        }
    ]


def get_nearest_tle_result(
    tle_repo: AbstractTLERepository,
    id: str,
    id_type: str,
    epoch: datetime,
    api_source: str,
    api_version: str,
) -> list[dict[str, list[dict[str, Any]] | str]]:
    """
    Fetches the nearest TLE to a specific epoch date.

    This function retrieves the TLE from the repository that is closest to the
    specified epoch date.

    Parameters:
        tle_repo (AbstractTLERepository): The repository to fetch TLE data from.
        id (str): The ID of the satellite.
        id_type (str): The type of the ID, either "catalog" or "name".
        epoch (datetime): The epoch date to fetch the nearest TLE to.
        api_source (str): The source of the API request.
        api_version (str): The version of the API request.

    Returns:
        list[dict[str, list[dict[str, Any]] | str]]: A single-item list
        containing a dictionary with:
        - tle_data: List of dictionaries, each containing:
            - satellite_name (str): Name of the satellite
            - satellite_id (int): NORAD catalog number
            - tle_line1 (str): First line of the TLE
            - tle_line2 (str): Second line of the TLE
            - epoch (str): Epoch of the TLE in 'YYYY-MM-DD HH:MM:SS TZ' format
            - date_collected (str): Date TLE was collected
            - data_source (str): Source of the TLE data
        - source (str): API source identifier
        - version (str): API version identifier
    """
    logger.info(f"Fetching nearest TLE to epoch {epoch} for {id_type} ID: {id}")

    try:
        tle = tle_repo.get_nearest_tle(id, id_type, epoch)
    except Exception as e:
        logger.error(f"Failed to retrieve nearest TLE: {str(e)}", exc_info=True)
        raise

    # Extract the TLE data from the result set
    try:
        if tle is not None:
            logger.info(f"Found nearest TLE with epoch: {tle.epoch}")
            tle_data = [
                {
                    "satellite_name": tle.satellite.sat_name,
                    "satellite_id": tle.satellite.sat_number,
                    "tle_line1": tle.tle_line1,
                    "tle_line2": tle.tle_line2,
                    "epoch": format_date(tle.epoch),
                    "date_collected": format_date(tle.date_collected),
                    "data_source": tle.data_source,
                }
            ]
        else:
            tle_data = []
            logger.warning(f"No TLE found for {id_type} ID: {id} near epoch {epoch}")
        logger.info("Successfully formatted TLE data")
    except Exception as e:
        logger.error(f"Failed to format TLE data: {str(e)}", exc_info=True)
        raise

    return [
        {
            "tle_data": tle_data,
            "source": api_source,
            "version": api_version,
        }
    ]


def get_adjacent_tle_results(
    tle_repo: AbstractTLERepository,
    id: str,
    id_type: str,
    epoch: datetime,
    api_source: str,
    api_version: str,
    format: str = "json",
) -> list[dict[str, list[dict[str, Any]] | str]] | io.BytesIO:
    """
    Fetches the adjacent TLEs to a specific epoch date - one TLE before and one after.

    Parameters:
        tle_repo (AbstractTLERepository): The repository to fetch TLE data from.
        id (str): The ID of the satellite.
        id_type (str): The type of the ID, either "catalog" or "name".
        epoch (datetime): The epoch date to fetch the adjacent TLEs to.
        api_source (str): The source of the API request.
        api_version (str): The version of the API request.
        format (str): The format of the response, either "json" or "txt".
    Returns:
        list[dict[str, list[dict[str, Any]] | str]] | io.BytesIO:
            - For JSON format: A list containing a dictionary with TLE data
            - For TXT format: A BytesIO object containing the formatted TLE text
    """
    logger.info(f"Fetching adjacent TLEs for {id_type} ID: {id} at epoch {epoch}")
    logger.info(f"Requested format: {format}")

    try:
        tles = tle_repo.get_adjacent_tles(id, id_type, epoch)
        logger.info(f"Retrieved {len(tles)} adjacent TLEs")
    except Exception as e:
        logger.error(f"Failed to retrieve adjacent TLEs: {str(e)}", exc_info=True)
        raise

    if format == "txt":
        try:
            tle_data: list[str] = [
                f"{tle.satellite.sat_name}\n{tle.tle_line1}\n{tle.tle_line2}\n"
                for tle in tles
            ]
            text_content = "".join(tle_data)
            logger.info("Successfully formatted TLE data as text")
            return io.BytesIO(text_content.encode())
        except Exception as e:
            logger.error(f"Failed to format TLE data as text: {str(e)}", exc_info=True)
            raise
    else:
        try:
            tle_json_data = [
                {
                    "satellite_name": tle.satellite.sat_name,
                    "satellite_id": tle.satellite.sat_number,
                    "tle_line1": tle.tle_line1,
                    "tle_line2": tle.tle_line2,
                    "epoch": format_date(tle.epoch),
                    "date_collected": format_date(tle.date_collected),
                    "data_source": tle.data_source,
                }
                for tle in tles
            ]
            logger.info("Successfully formatted TLE data as JSON")
            return [
                {
                    "tle_data": tle_json_data,
                    "source": api_source,
                    "version": api_version,
                }
            ]
        except Exception as e:
            logger.error(f"Failed to format TLE data as JSON: {str(e)}", exc_info=True)
            raise


def get_satellite_data(
    sat_repo: AbstractSatelliteRepository,
    id: str,
    id_type: str,
    api_source: str,
    api_version: str,
):
    """
    Fetches satellite data based on the provided ID and ID type.

    This function retrieves satellite metadata from the repository based on the
    provided ID. The ID can be either a catalog ID or a satellite name, determined
    by the id_type parameter.

    Parameters:
        sat_repo (AbstractSatelliteRepository): The repository to fetch satellite data
        from.
        id (str): The ID of the satellite, either a catalog ID or a satellite name.
        id_type (str): The type of the ID, either "catalog" or "name".
        api_source (str): The source of the API request.
        api_version (str): The version of the API request.

    Returns:
        List[Dict[str, Any]]: A list containing a dictionary with satellite data.
                              Returns an empty list if no satellite data is found.
    """
    logger.info(f"Fetching satellite data for {id_type} ID: {id}")

    try:
        satellite = (
            sat_repo.get_satellite_data_by_id(id)
            if id_type == "catalog"
            else sat_repo.get_satellite_data_by_name(id)
        )
        if satellite is None:
            logger.warning(f"No satellite found for {id_type} ID: {id}")
            return []
        logger.info(f"Found satellite: {satellite.sat_name}")
    except Exception as e:
        logger.error(f"Failed to retrieve satellite data: {str(e)}", exc_info=True)
        raise

    try:
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
                "generation": satellite.generation,
                "constellation": satellite.constellation,
            }
        ]
        logger.info("Successfully formatted satellite data")
    except Exception as e:
        logger.error(f"Failed to format satellite data: {str(e)}", exc_info=True)
        raise

    results = {
        "count": len(satellite_data),
        "data": satellite_data,
        "source": api_source,
        "version": api_version,
    }

    return results


def get_starlink_generations(
    sat_repo: AbstractSatelliteRepository,
    api_source: str,
    api_version: str,
):
    """
    Fetches and formats information about Starlink satellite generations.

    This function retrieves data about different Starlink satellite generations,
    including their earliest and latest launch dates. The data is formatted into
    a standardized response structure.

    Parameters:
        sat_repo (AbstractSatelliteRepository):
            The repository instance used to fetch Starlink generation data.
        api_source (str):
            The source identifier for the API request.
        api_version (str):
            The version identifier for the API request.

    Returns:
        dict: A dictionary containing:
            - count (int): Number of Starlink generations found
            - data (list): List of dictionaries, each containing:
                - generation (str): The generation identifier
                - earliest_launch_date (str): The earliest launch date for this
                generation
                - latest_launch_date (str): The latest launch date for this generation
            - source (str): The API source identifier
            - version (str): The API version identifier

    Raises:
        Exception: If there is an error retrieving or formatting the generation data
    """
    logger.info("Fetching list of Starlink generations")

    try:
        generation_info = sat_repo.get_starlink_generations()
        logger.info(f"Retrieved {len(generation_info)} Starlink generations")
    except Exception as e:
        logger.error(
            f"Failed to retrieve Starlink generations: {str(e)}", exc_info=True
        )
        raise

    try:
        generation_list = [
            {
                "generation": gen,
                "earliest_launch_date": format_date(earliest),
                "latest_launch_date": format_date(latest),
            }
            for gen, earliest, latest in generation_info
        ]
        logger.info("Successfully formatted generation list")
    except Exception as e:
        logger.error(f"Failed to format generation list: {str(e)}", exc_info=True)
        raise

    return {
        "count": len(generation_list),
        "data": generation_list,
        "source": api_source,
        "version": api_version,
    }


def get_active_satellites(
    sat_repo: AbstractSatelliteRepository,
    object_type: str | None,
    api_source: str,
    api_version: str,
):
    """
    Fetches active satellites based on the provided object type (optional).

    Parameters:
        sat_repo (AbstractSatelliteRepository): The repository to fetch satellite data
        from.
        object_type (str): The type of the object, either "payload", "debris",
        "rocket body", "tba", or "unknown".
        api_source (str): The source of the API request.
        api_version (str): The version of the API request.

    Returns:
        dict: A dictionary containing:
            - count: number of satellites found
            - data: list of satellite data
            - source: API source
            - version: API version
    """
    logger.info(f"Fetching active satellites with object type: {object_type}")

    try:
        satellites = sat_repo.get_active_satellites(object_type)
        logger.info(f"Retrieved {len(satellites)} active satellites")
    except Exception as e:
        logger.error(f"Failed to retrieve active satellites: {str(e)}", exc_info=True)
        raise

    satellite_json = satellite_data_to_json(satellites, api_source, api_version)

    return satellite_json


def search_all_satellites(
    sat_repo: AbstractSatelliteRepository,
    parameters: dict,
    api_source: str,
    api_version: str,
):
    satellites = sat_repo.search_all_satellites(parameters)

    satellite_json = satellite_data_to_json(satellites, api_source, api_version)

    return satellite_json


def get_all_tles_at_epoch_formatted(
    tle_repo: AbstractTLERepository,
    epoch_date: datetime,
    format: str = "json",
    page: int = 1,
    per_page: int = 100,
    api_source: str = "",
    api_version: str = "",
) -> list[dict[str, Any]] | io.BytesIO:
    """
    Fetches all TLEs at a specific epoch date with support for different output formats.

    Parameters:
        tle_repo (AbstractTLERepository): The repository to fetch TLE data from.
        epoch_date (datetime): The epoch date for the TLE data.
        format (str): Output format - either "json", "txt", or "zip".
        page (int): The page number for pagination (used for JSON format).
        per_page (int): The number of results per page (used for JSON format).
        api_source (str): The source of the API request.
        api_version (str): The version of the API request.

    Returns:
        list[dict[str, Any]] | io.BytesIO: Either a list containing TLE data
        and pagination info (JSON) or a BytesIO object containing formatted TLE data
        (TXT/ZIP).
    """
    logger.info(f"Fetching all TLEs at epoch {epoch_date} in {format} format")
    logger.info(f"Pagination: page {page}, {per_page} items per page")

    # For text format, get all records
    actual_per_page = 1000000 if format == "txt" else per_page
    actual_page = 1 if format == "txt" else page

    try:
        tles, total_count, _ = tle_repo.get_all_tles_at_epoch(
            epoch_date, actual_page, actual_per_page, format
        )
        logger.info(f"Retrieved {len(tles)} TLEs out of {total_count} total")
    except Exception as e:
        logger.error(f"Failed to retrieve TLEs: {str(e)}", exc_info=True)
        raise

    if format == "txt":
        try:
            tle_data: list[str] = [
                f"{tle.satellite.sat_name}\n{tle.tle_line1}\n{tle.tle_line2}\n"
                for tle in tles
            ]
            text_content = "".join(tle_data)
            logger.info("Successfully formatted TLE data as text")
            return io.BytesIO(text_content.encode())
        except Exception as e:
            logger.error(f"Failed to format TLE data as text: {str(e)}", exc_info=True)
            raise

    elif format == "zip":
        try:
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer)

            csv_writer.writerow(
                [
                    "satellite_name",
                    "satellite_id",
                    "tle_line1",
                    "tle_line2",
                    "epoch",
                    "date_collected",
                    "data_source",
                ]
            )

            for tle in tles:
                csv_writer.writerow(
                    [
                        tle.satellite.sat_name,
                        tle.satellite.sat_number,
                        tle.tle_line1,
                        tle.tle_line2,
                        format_date(tle.epoch),
                        format_date(tle.date_collected),
                        tle.data_source,
                    ]
                )

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("tle_data.csv", csv_buffer.getvalue())

            zip_buffer.seek(0)
            logger.info("Successfully created ZIP file with TLE data")
            return zip_buffer
        except Exception as e:
            logger.error(f"Failed to create ZIP file: {str(e)}", exc_info=True)
            raise

    else:
        try:
            tle_json_data = [
                {
                    "satellite_name": tle.satellite.sat_name,
                    "satellite_id": tle.satellite.sat_number,
                    "tle_line1": tle.tle_line1,
                    "tle_line2": tle.tle_line2,
                    "epoch": format_date(tle.epoch),
                    "date_collected": format_date(tle.date_collected),
                    "data_source": tle.data_source,
                }
                for tle in tles
            ]
            logger.info("Successfully formatted TLE data as JSON")
            return [
                {
                    "per_page": per_page,
                    "page": page,
                    "total_results": total_count,
                    "data": tle_json_data,
                    "source": api_source,
                    "version": api_version,
                }
            ]
        except Exception as e:
            logger.error(f"Failed to format TLE data as JSON: {str(e)}", exc_info=True)
            raise


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
    logger.info(f"Fetching NORAD IDs for satellite name: {satellite_name}")

    try:
        satellite_ids_dates = sat_repo.get_norad_ids_from_satellite_name(satellite_name)
        logger.info(f"Retrieved {len(satellite_ids_dates)} NORAD IDs")
    except Exception as e:
        logger.error(f"Failed to retrieve NORAD IDs: {str(e)}", exc_info=True)
        raise

    try:
        ids_and_dates = [
            {
                "name": satellite_name,
                "norad_id": id_date[0],
                "date_added": format_date(id_date[1]),
                "is_current_version": id_date[2],
            }
            for id_date in satellite_ids_dates
        ]
        logger.info("Successfully formatted NORAD ID data")
    except Exception as e:
        logger.error(f"Failed to format NORAD ID data: {str(e)}", exc_info=True)
        raise

    results = {
        "count": len(ids_and_dates),
        "data": ids_and_dates,
        "source": api_source,
        "version": api_version,
    }

    return results


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
    logger.info(f"Fetching satellite names for NORAD ID: {satellite_id}")

    try:
        satellite_names_and_dates = sat_repo.get_satellite_names_from_norad_id(
            satellite_id
        )
        logger.info(f"Retrieved {len(satellite_names_and_dates)} satellite names")
    except Exception as e:
        logger.error(f"Failed to retrieve satellite names: {str(e)}", exc_info=True)
        raise

    try:
        names_and_dates = [
            {
                "name": name_date[0],
                "norad_id": satellite_id,
                "date_added": format_date(name_date[1]),
                "is_current_version": name_date[2],
            }
            for name_date in satellite_names_and_dates
        ]
        logger.info("Successfully formatted satellite name data")
    except Exception as e:
        logger.error(f"Failed to format satellite name data: {str(e)}", exc_info=True)
        raise

    results = {
        "count": len(names_and_dates),
        "data": names_and_dates,
        "source": api_source,
        "version": api_version,
    }

    return results
