import csv
import io
import logging
import zipfile
from datetime import datetime, timezone
from typing import Any, cast

from api.adapters.repositories.ephemeris_repository import AbstractEphemerisRepository
from api.adapters.repositories.orbital_elements_repository import (
    AbstractOrbitalElementsRepository,
)
from api.adapters.repositories.satellite_repository import AbstractSatelliteRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.domain.models.orbital_elements import OrbitalElements
from api.domain.models.tle import TLE
from api.utils.orbital_data_utils import ORBITAL_ELEMENTS_CUTOFF, omm_to_tle_lines
from api.utils.output_utils import (
    ephemeris_data_to_parquet,
    ephemeris_data_to_zip,
    format_date,
    satellite_data_to_json,
)

logger = logging.getLogger(__name__)
OrbitalDataRepository = AbstractTLERepository | AbstractOrbitalElementsRepository


def _tle_lines(record: TLE | OrbitalElements) -> tuple[str, str]:
    """Return the TLE line pair for a record, converting OMM elements if needed."""
    if isinstance(record, OrbitalElements):
        return omm_to_tle_lines(record)
    return record.tle_line1, record.tle_line2


def _format_tle_record(record: TLE | OrbitalElements) -> dict[str, Any]:
    """Format a TLE or OMM record as a TLE response dict.

    OMM records are converted to their equivalent TLE lines so the TLE
    endpoints return identical output before and after
    ORBITAL_ELEMENTS_CUTOFF.
    """
    line1, line2 = _tle_lines(record)
    return {
        "satellite_name": record.satellite.sat_name,
        "satellite_id": record.satellite.sat_number,
        "tle_line1": line1,
        "tle_line2": line2,
        "epoch": format_date(record.epoch),
        "date_collected": format_date(record.date_collected),
        "data_source": record.data_source,
    }


def _tle_source_repo(
    tle_repo: AbstractTLERepository,
    orbital_elements_repo: AbstractOrbitalElementsRepository | None,
    epoch: datetime | None,
) -> OrbitalDataRepository:
    """Pick the store that holds TLE-format data for an epoch.

    TLEs are stored before ORBITAL_ELEMENTS_CUTOFF; at/after the cutoff the data
    lives in the OMM store and is converted to TLE format on the way out, so the
    TLE endpoints behave the same either side of the cutoff. When no OMM
    repository is provided the TLE store is used unconditionally.
    """
    if orbital_elements_repo is None or epoch is None:
        return tle_repo
    if epoch.tzinfo is None:
        epoch = epoch.replace(tzinfo=timezone.utc)
    if epoch >= ORBITAL_ELEMENTS_CUTOFF:
        return orbital_elements_repo
    return tle_repo


def _query_date_range(
    repo: OrbitalDataRepository,
    id: str,
    id_type: str,
    start_date: datetime,
    end_date: datetime,
) -> list[TLE] | list[OrbitalElements]:
    """Fetch a repository's records for a satellite over a date range."""
    if id_type == "catalog":
        return repo.get_all_for_date_range_by_satellite_number(id, start_date, end_date)
    return repo.get_all_for_date_range_by_satellite_name(id, start_date, end_date)


def get_orbital_data(
    tle_repo: AbstractTLERepository,
    orbital_elements_repo: AbstractOrbitalElementsRepository,
    format: str,
    id: str,
    id_type: str,
    start_date: datetime,
    end_date: datetime,
    api_source: str,
    api_version: str,
):
    """
    Fetches orbital data for a given satellite.

    This function retrieves either TLE or OMM data from either the NORAD ID or
    satellite name provided. It allows for a date range to be specified for the
    orbital data, and if not provided, it will return all orbital data for the
    satellite.

    Parameters:
        tle_repo (AbstractTLERepository):
            The repository instance used to fetch TLE data.
        orbital_elements_repo (AbstractOrbitalElementsRepository):
            The repository instance used to fetch OMM data.
        format (str):
            The format of the orbital data, either 'tle' or 'omm'.
        id (str):
            The identifier for the satellite.
        id_type (str):
            The type of the ID, either 'catalog' (NORAD ID) or 'name'.
        start_date (datetime):
            The start date of the date range for the orbital data.
        end_date (datetime):
            The end date of the date range for the orbital data.

    Returns:
        List[dict]:
            A list containing the orbital data for the specified
            satellite and date range. Each data point includes the satellite
            name, satellite ID, orbital data (tle lines or orbital elements), epoch,
            date collected, and data source.
    """
    logger.info(f"Fetching TLE data for {id_type} ID: {id}")
    logger.info(f"Date range: {start_date} to {end_date}")
    logger.info(f"Format: {format}")

    if format == "tle":
        format_name = "TLE"
    elif format == "omm":
        format_name = "OMM"
    else:
        raise ValueError(f"Invalid format: {format}")

    orbital_data_set: list[TLE | OrbitalElements]
    try:
        if format == "tle":
            # TLEs are stored before the cutoff and OMM records at/after it;
            # query both stores and merge so a range spanning the cutoff returns
            # one continuous series.
            records: list[TLE | OrbitalElements] = []
            records.extend(
                _query_date_range(tle_repo, id, id_type, start_date, end_date)
            )
            if orbital_elements_repo is not None:
                records.extend(
                    _query_date_range(
                        orbital_elements_repo, id, id_type, start_date, end_date
                    )
                )
            orbital_data_set = sorted(records, key=lambda record: record.epoch)
        else:
            orbital_data_set = list(
                _query_date_range(
                    orbital_elements_repo, id, id_type, start_date, end_date
                )
            )
        logger.info(f"Retrieved {len(orbital_data_set)} {format_name}s")
    except Exception as e:
        logger.error(f"Failed to retrieve {format_name}s: {str(e)}", exc_info=True)
        raise

    # Extract the orbita data from the result set
    try:
        if format == "tle":
            orbital_data_result = [
                _format_tle_record(record) for record in orbital_data_set
            ]
        else:
            orbital_data_result = [
                {
                    "satellite_name": omm.satellite.sat_name,
                    "satellite_id": omm.satellite.sat_number,
                    "orbital_elements": omm.to_omm_dict(),
                    "epoch": format_date(omm.epoch),
                    "date_collected": format_date(omm.date_collected),
                    "data_source": omm.data_source,
                }
                for omm in cast(list[OrbitalElements], orbital_data_set)
            ]
        logger.info(
            f"Successfully formatted {len(orbital_data_set)} {format_name} records"
        )
    except Exception as e:
        logger.error(f"Failed to format {format_name} data: {str(e)}", exc_info=True)
        raise

    results = {
        "count": len(orbital_data_result),
        "data": orbital_data_result,
        "source": api_source,
        "version": api_version,
    }

    return results


def get_orbital_data_around_epoch_results(
    tle_repo: AbstractTLERepository,
    orbital_elements_repo: AbstractOrbitalElementsRepository,
    format: str,
    id: str,
    id_type: str,
    epoch: datetime,
    count_before: int,
    count_after: int,
    api_source: str,
    api_version: str,
):
    """
    Fetches orbital data around a specific epoch date.

    This function retrieves either TLE or OMM data from the repository that are around
    the specified epoch date. It allows for a count of orbital data to be specified
    before and after the epoch date.

    Parameters:
        tle_repo (AbstractTLERepository): The repository to fetch TLE data from.
        orbital_elements_repo (AbstractOrbitalElementsRepository): The repository to
            fetch OMM data from.
        format (str): The format of the orbital data, either "tle" or "omm".
        id (str): The ID of the satellite.
        id_type (str): The type of the ID, either "catalog" or "name".
        epoch (datetime): The epoch date to fetch TLE or OMM data around.
        count_before (int): The number of orbital data to fetch before the epoch date.
        count_after (int): The number of orbital data to fetch after the epoch date.

    Returns:
        List[dict]: A list of dictionaries containing the orbital data.
    """
    repo: OrbitalDataRepository
    if format == "tle":
        repo = _tle_source_repo(tle_repo, orbital_elements_repo, epoch)
        format_name = "TLE"
    elif format == "omm":
        repo = orbital_elements_repo
        format_name = "OMM"
    else:
        raise ValueError(f"Invalid format: {format}")

    logger.info(f"Fetching {format} data around epoch {epoch} for {id_type} ID: {id}")
    logger.info(
        f"Requesting {count_before} {format_name}s before and "
        f"{count_after} {format_name}s after epoch"
    )

    try:
        raw_result: Any = repo.get_orbital_data_around_epoch(
            id, id_type, epoch, count_before, count_after
        )
        logger.info(f"Successfully retrieved {format_name}s from repository")
    except Exception as e:
        logger.error(
            f"Failed to retrieve {format_name}s from repository: {str(e)}",
            exc_info=True,
        )
        raise

    # Ensure the result is a list to avoid iteration errors
    orbital_data_set: list[TLE] | list[OrbitalElements]
    if raw_result is None:
        orbital_data_set = []
    elif isinstance(raw_result, list):
        orbital_data_set = raw_result
    else:
        orbital_data_set = [raw_result]
    logger.info(f"Processing {len(orbital_data_set)} {format_name} records")

    try:
        formatted_data: list[dict[str, Any]] = []
        if format == "tle":
            # Extract the TLE data from the result set
            formatted_data.extend(
                [_format_tle_record(record) for record in orbital_data_set]
            )
        else:
            formatted_data.extend(
                [
                    {
                        "satellite_name": omm.satellite.sat_name,
                        "satellite_id": omm.satellite.sat_number,
                        "orbital_elements": omm.to_omm_dict(),
                        "epoch": format_date(omm.epoch),
                        "date_collected": format_date(omm.date_collected),
                        "data_source": omm.data_source,
                    }
                    for omm in cast(list[OrbitalElements], orbital_data_set)
                ]
            )
        logger.info(
            f"Successfully formatted {len(formatted_data)} {format_name} records"
        )
    except Exception as e:
        logger.error(f"Failed to format TLE data: {str(e)}", exc_info=True)
        raise

    return [
        {
            "orbital_data": formatted_data,
            "source": api_source,
            "version": api_version,
        }
    ]


def get_nearest_orbital_data_result(
    tle_repo: AbstractTLERepository,
    orbital_elements_repo: AbstractOrbitalElementsRepository,
    format: str,
    id: str,
    id_type: str,
    epoch: datetime,
    api_source: str,
    api_version: str,
) -> list[dict[str, list[dict[str, Any]] | str]]:
    """
    Fetches the nearest orbital data (OMM or TLE) to a specific epoch date.

    Parameters:
        tle_repo (AbstractTLERepository): The repository to fetch TLE data from.
        orbital_elements_repo (AbstractOrbitalElementsRepository): The repository to
            fetch OMM data from.
        format (str): The format of the orbital data, either "tle" or "omm".
        id (str): The ID of the satellite.
        id_type (str): The type of the ID, either "catalog" or "name".
        epoch (datetime): The epoch date to fetch the nearest orbital data to.
        api_source (str): The source of the API request.
        api_version (str): The version of the API request.

    Returns:
        list[dict[str, list[dict[str, Any]] | str]]: A single-item list
        containing a dictionary with:
        - orbital_data: List of dictionaries, each containing:
            - satellite_name (str): Name of the satellite
            - satellite_id (int): NORAD catalog number
            - epoch (str): Epoch of the TLE in 'YYYY-MM-DD HH:MM:SS TZ' format
            - date_collected (str): Date TLE was collected
            - data_source (str): Source of the TLE data
            - either the TLE lines or the OMM elements
        - source (str): API source identifier
        - version (str): API version identifier
    """
    logger.info(
        f"Fetching nearest orbital data to epoch {epoch} for {id_type} ID: {id}"
    )

    repo: OrbitalDataRepository
    if format == "tle":
        repo = _tle_source_repo(tle_repo, orbital_elements_repo, epoch)
        format_name = "TLE"
    elif format == "omm":
        repo = orbital_elements_repo
        format_name = "OMM"
    else:
        raise ValueError(f"Invalid format: {format}")

    try:
        orbital_data = repo.get_nearest_orbital_data(id, id_type, epoch)
    except Exception as e:
        logger.error(f"Failed to retrieve nearest TLE: {str(e)}", exc_info=True)
        raise

    # Extract the TLE data from the result set
    try:
        if orbital_data is not None:
            logger.info(f"Found nearest {format_name} with epoch: {orbital_data.epoch}")
            if format == "tle":
                orbital_data_result = [_format_tle_record(orbital_data)]
            else:
                omm = cast(OrbitalElements, orbital_data)
                orbital_data_result = [
                    {
                        "satellite_name": omm.satellite.sat_name,
                        "satellite_id": omm.satellite.sat_number,
                        "orbital_elements": omm.to_omm_dict(),
                        "epoch": format_date(omm.epoch),
                        "date_collected": format_date(omm.date_collected),
                        "data_source": omm.data_source,
                    }
                ]
        else:
            orbital_data_result = []
            logger.warning(
                f"No {format_name} found for {id_type} ID: {id} near epoch {epoch}"
            )
        logger.info(f"Successfully formatted {format_name} data")
    except Exception as e:
        logger.error(f"Failed to format {format_name} data: {str(e)}", exc_info=True)
        raise

    return [
        {
            "orbital_data": orbital_data_result,
            "source": api_source,
            "version": api_version,
        }
    ]


def get_adjacent_orbital_data_results(
    tle_repo: AbstractTLERepository,
    orbital_elements_repo: AbstractOrbitalElementsRepository,
    data_format: str,
    id: str,
    id_type: str,
    epoch: datetime,
    api_source: str,
    api_version: str,
    format: str = "json",
) -> list[dict[str, list[dict[str, Any]] | str]] | io.BytesIO:
    """
    Fetches the adjacent orbital data (OMM or TLE) to a specific epoch date -
    one before and one after.

    Parameters:
        tle_repo (AbstractTLERepository): The repository to fetch TLE data from.
        orbital_elements_repo (AbstractOrbitalElementsRepository): The repository to
            fetch OMM data from.
        data_format (str): The format of the orbital data, either "tle" or "omm".
        id (str): The ID of the satellite.
        id_type (str): The type of the ID, either "catalog" or "name".
        epoch (datetime): The epoch date to fetch the adjacent orbital data to.
        api_source (str): The source of the API request.
        api_version (str): The version of the API request.
        format (str): The format of the response, either "json" or "txt".
    Returns:
        Union[list[dict[str, list[dict[str, Any]] | str]], io.BytesIO]:
            - For JSON format: A list containing a dictionary with orbital data
            - For TXT format: A BytesIO object containing the formatted orbital data
            text
    """
    repo: OrbitalDataRepository
    if data_format == "tle":
        repo = _tle_source_repo(tle_repo, orbital_elements_repo, epoch)
        format_name = "TLE"
    elif data_format == "omm":
        repo = orbital_elements_repo
        format_name = "OMM"
    else:
        raise ValueError(f"Invalid data format: {data_format}")

    logger.info(
        f"Fetching adjacent {format_name} data for {id_type} ID: {id} at epoch {epoch}"
    )
    logger.info(f"Requested format: {format}")

    try:
        orbital_data_set = repo.get_adjacent_orbital_data(id, id_type, epoch)
        logger.info(f"Retrieved {len(orbital_data_set)} adjacent {format_name}s")
    except Exception as e:
        logger.error(
            f"Failed to retrieve adjacent {format_name}s: {str(e)}",
            exc_info=True,
        )
        raise

    if format == "txt" and data_format == "tle":
        try:
            text_lines: list[str] = []
            for record in orbital_data_set:
                line1, line2 = _tle_lines(record)
                text_lines.append(f"{record.satellite.sat_name}\n{line1}\n{line2}\n")
            text_content = "".join(text_lines)
            logger.info(f"Successfully formatted {format_name} data as text")
            return io.BytesIO(text_content.encode())
        except Exception as e:
            logger.error(
                f"Failed to format {format_name} data as text: {str(e)}",
                exc_info=True,
            )
            raise
    else:
        try:
            if data_format == "tle":
                orbital_json_data = [
                    _format_tle_record(record) for record in orbital_data_set
                ]
            else:
                orbital_json_data = [
                    {
                        "satellite_name": omm.satellite.sat_name,
                        "satellite_id": omm.satellite.sat_number,
                        "orbital_elements": omm.to_omm_dict(),
                        "epoch": format_date(omm.epoch),
                        "date_collected": format_date(omm.date_collected),
                        "data_source": omm.data_source,
                    }
                    for omm in cast(list[OrbitalElements], orbital_data_set)
                ]
            logger.info(f"Successfully formatted {format_name} data as JSON")
            return [
                {
                    "orbital_data": orbital_json_data,
                    "source": api_source,
                    "version": api_version,
                }
            ]
        except Exception as e:
            logger.error(
                f"Failed to format {format_name} data as JSON: {str(e)}",
                exc_info=True,
            )
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


def get_all_orbital_data_at_epoch_formatted(
    tle_repo: AbstractTLERepository | None,
    orbital_elements_repo: AbstractOrbitalElementsRepository | None,
    data_format: str,
    epoch_date: datetime,
    format: str = "json",
    page: int = 1,
    per_page: int = 100,
    api_source: str = "",
    api_version: str = "",
) -> list[dict[str, Any]] | io.BytesIO:
    """
    Fetches all orbital data (TLEs or OMMs) at a specific epoch date with support for
    different output formats.

    Parameters:
        tle_repo (AbstractTLERepository): The repository to fetch TLE data from.
        orbital_elements_repo (AbstractOrbitalElementsRepository): The repository to
            fetch OMM data from.
        data_format (str): The format of the orbital data, either "tle" or "omm".
        epoch_date (datetime): The epoch date for the orbital data.
        format (str): Output format - either "json", "txt", or "zip".
        page (int): The page number for pagination (used for JSON format).
        per_page (int): The number of results per page (used for JSON format).
        api_source (str): The source of the API request.
        api_version (str): The version of the API request.

    Returns:
        list[dict[str, Any]] | io.BytesIO: Either a list containing orbital data
        and pagination info (JSON) or a BytesIO object containing formatted orbital data
        (TXT/ZIP).
    """
    # For data_format="tle", both repositories are required so post-cutoff
    # epochs can be served from the OMM store; for "omm" only the OMM repo is
    # used.
    repo: OrbitalDataRepository
    if data_format == "tle":
        repo = _tle_source_repo(
            cast(AbstractTLERepository, tle_repo),
            cast(AbstractOrbitalElementsRepository, orbital_elements_repo),
            epoch_date,
        )
        format_name = "TLE"
    elif data_format == "omm":
        repo = cast(AbstractOrbitalElementsRepository, orbital_elements_repo)
        format_name = "OMM"
    else:
        raise ValueError(f"Invalid data format: {data_format}")

    logger.info(
        f"Fetching all {format_name} data at epoch {epoch_date} in {format} format"
    )
    logger.info(f"Pagination: page {page}, {per_page} items per page")

    # For text format, get all records
    actual_per_page = 1000000 if format == "txt" else per_page
    actual_page = 1 if format == "txt" else page

    try:
        orbital_data_set, total_count, _ = repo.get_all_orbital_data_at_epoch(
            epoch_date, actual_page, actual_per_page, format
        )
        logger.info(
            f"Retrieved {len(orbital_data_set)} {format_name}s out of "
            f"{total_count} total"
        )
    except Exception as e:
        logger.error(f"Failed to retrieve {format_name}s: {str(e)}", exc_info=True)
        raise

    if format == "txt" and data_format == "tle":
        try:
            text_lines: list[str] = []
            for record in orbital_data_set:
                line1, line2 = _tle_lines(record)
                text_lines.append(f"{record.satellite.sat_name}\n{line1}\n{line2}\n")
            text_content = "".join(text_lines)
            logger.info(f"Successfully formatted {format_name} data as text")
            return io.BytesIO(text_content.encode())
        except Exception as e:
            logger.error(
                f"Failed to format {format_name} data as text: {str(e)}",
                exc_info=True,
            )
            raise

    elif format == "zip":
        try:
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer)

            if data_format == "tle":
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

                for record in orbital_data_set:
                    line1, line2 = _tle_lines(record)
                    csv_writer.writerow(
                        [
                            record.satellite.sat_name,
                            record.satellite.sat_number,
                            line1,
                            line2,
                            format_date(record.epoch),
                            format_date(record.date_collected),
                            record.data_source,
                        ]
                    )
            else:
                # Flat CSV using the CCSDS OMM field names (to_omm_dict) plus the
                # SatChecker metadata columns; keep header in sync with row order.
                csv_writer.writerow(
                    [
                        "OBJECT_NAME",
                        "OBJECT_ID",
                        "EPOCH",
                        "MEAN_MOTION",
                        "ECCENTRICITY",
                        "INCLINATION",
                        "RA_OF_ASC_NODE",
                        "ARG_OF_PERICENTER",
                        "MEAN_ANOMALY",
                        "EPHEMERIS_TYPE",
                        "CLASSIFICATION_TYPE",
                        "NORAD_CAT_ID",
                        "ELEMENT_SET_NO",
                        "REV_AT_EPOCH",
                        "BSTAR",
                        "MEAN_MOTION_DOT",
                        "MEAN_MOTION_DDOT",
                        "date_collected",
                        "data_source",
                    ]
                )

                for omm in cast(list[OrbitalElements], orbital_data_set):
                    csv_writer.writerow(
                        [
                            *omm.to_omm_dict().values(),
                            format_date(omm.date_collected),
                            omm.data_source,
                        ]
                    )

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr(f"{data_format}_data.csv", csv_buffer.getvalue())

            zip_buffer.seek(0)
            logger.info(f"Successfully created ZIP file with {format_name} data")
            return zip_buffer
        except Exception as e:
            logger.error(f"Failed to create ZIP file: {str(e)}", exc_info=True)
            raise

    else:
        try:
            if data_format == "tle":
                orbital_json_data = [
                    _format_tle_record(record) for record in orbital_data_set
                ]

            else:
                orbital_json_data = [
                    {
                        "satellite_name": omm.satellite.sat_name,
                        "satellite_id": omm.satellite.sat_number,
                        "orbital_elements": omm.to_omm_dict(),
                        "epoch": format_date(omm.epoch),
                        "date_collected": format_date(omm.date_collected),
                        "data_source": omm.data_source,
                    }
                    for omm in cast(list[OrbitalElements], orbital_data_set)
                ]

            logger.info(f"Successfully formatted {format_name} data as JSON")
            return [
                {
                    "per_page": per_page,
                    "page": page,
                    "total_results": total_count,
                    "data": orbital_json_data,
                    "source": api_source,
                    "version": api_version,
                }
            ]
        except Exception as e:
            logger.error(
                f"Failed to format {format_name} data as JSON: {str(e)}",
                exc_info=True,
            )
            raise


def get_all_ephemeris_data_at_epoch_formatted(
    ephemeris_repo: AbstractEphemerisRepository,
    epoch_date: datetime,
    format: str = "parquet",
) -> io.BytesIO:
    """Fetch all raw ephemeris data valid at an epoch, serialized as a binary file.

    For every satellite whose ephemeris window covers ``epoch_date``, the closest
    record (its full set of stored points) is returned exactly as saved. Because
    this is a much larger data set than TLE/OMM output, it is only served as a
    binary file: a single Parquet file (default) or a zip of per-satellite CSVs.

    Args:
        ephemeris_repo: Repository used to look up ephemeris records.
        epoch_date: The epoch as a tz-aware datetime (the route converts the
            Julian Date query param before calling this service).
        format: Output format, either ``"parquet"`` (default) or ``"zip"``.

    Returns:
        io.BytesIO: The serialized ephemeris data, ready to stream to the client.
    """
    logger.info(
        "Fetching all ephemeris data at epoch %s in %s format", epoch_date, format
    )

    # Closest covering ephemeris record per satellite at the epoch, in one query.
    # Points are loaded from the DB or S3/Parquet by the repository.
    records = ephemeris_repo.get_all_closest_at_epoch(epoch_date)
    logger.info(
        "Retrieved ephemeris for %d satellites at epoch %s", len(records), epoch_date
    )

    if format == "parquet":
        return ephemeris_data_to_parquet(records)
    return ephemeris_data_to_zip(records)


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
