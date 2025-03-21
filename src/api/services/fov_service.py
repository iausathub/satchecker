import json
import time as python_time
from datetime import datetime, timedelta

import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from skyfield.api import EarthSatellite, load, wgs84

from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.entrypoints.extensions import redis_client
from api.utils import coordinate_systems, output_utils


def _create_fov_cache_key(
    location: EarthLocation,
    mid_obs_time_jd: Time,
    start_time_jd: Time,
    duration: float,
    ra: float,
    dec: float,
    fov_radius: float,
) -> str:
    """Create a unique cache key for the FOV calculation."""
    key_parts = [
        "fov",
        f"lat_{location.lat.value:.6f}",
        f"lon_{location.lon.value:.6f}",
        f"height_{location.height.value:.6f}",
        f"mid_time_{mid_obs_time_jd.jd if mid_obs_time_jd else 'None'}",
        f"start_time_{start_time_jd.jd if start_time_jd else 'None'}",
        f"duration_{duration}",
        f"ra_{ra}",
        f"dec_{dec}",
        f"radius_{fov_radius}",
    ]
    return ":".join(key_parts)


def get_satellite_passes_in_fov(
    tle_repo: AbstractTLERepository,
    location: EarthLocation,
    mid_obs_time_jd: Time,
    start_time_jd: Time,
    duration: float,
    ra: float,
    dec: float,
    fov_radius: float,
    group_by: str,
    api_source: str,
    api_version: str,
) -> dict:
    start_time = python_time.time()
    print(f"\nStarting FOV calculation at: {datetime.now().isoformat()}")
    print(f"FOV Parameters: RA={ra}°, Dec={dec}°, Radius={fov_radius}°")
    print(f"Duration: {duration} seconds")

    # Create cache key and check cache

    cache_key = _create_fov_cache_key(
        location, mid_obs_time_jd, start_time_jd, duration, ra, dec, fov_radius
    )
    cached_data = redis_client.get(cache_key)
    if cached_data:
        cache_time = python_time.time() - start_time
        print("Found cached result")
        cached_results = json.loads(cached_data)
        # Return cached results using the same formatting function
        return output_utils.fov_data_to_json(
            cached_results["results"],
            cached_results["points_in_fov"],
            {
                "total_time": round(cache_time, 3),
                "points_in_fov": cached_results["points_in_fov"],
                "from_cache": True,
            },
            api_source,
            api_version,
            group_by,
        )

    # Get all current TLEs
    tle_start = python_time.time()
    time_param = mid_obs_time_jd if mid_obs_time_jd is not None else start_time_jd
    tles, count = tle_repo.get_all_tles_at_epoch(
        time_param.to_datetime(), 1, 10000, "zip"
    )

    tle_time = python_time.time() - tle_start
    print(f"Retrieved {count} TLEs in {tle_time:.2f} seconds")

    # Pre-compute time arrays and constants
    ts = load.timescale()
    time_step = 1 / 86400  # 1 second
    duration_jd = duration / 86400

    prop_start = python_time.time()
    if mid_obs_time_jd is not None:
        jd_times = np.arange(
            mid_obs_time_jd.jd - duration_jd / 2,
            mid_obs_time_jd.jd + duration_jd / 2,
            time_step,
        )
    elif start_time_jd is not None:
        jd_times = np.arange(
            start_time_jd.jd,
            start_time_jd.jd + duration_jd,
            time_step,
        )
    t = ts.ut1_jd(jd_times)
    print(f"Checking {len(jd_times)} time points")

    # Set up observer and FOV vectors once
    curr_pos = wgs84.latlon(
        location.lat.value, location.lon.value, location.height.value
    )
    icrf = coordinate_systems.radec2icrf(ra, dec).reshape(3, 1)

    all_results = []
    satellites_processed = 0
    points_in_fov = 0
    total_sat_time = 0

    for tle in tles:
        sat_start = python_time.time()
        try:
            satellite = EarthSatellite(tle.tle_line1, tle.tle_line2, ts=ts)
            difference = satellite - curr_pos
            topocentric = difference.at(t)
            topocentricn = topocentric.position.km / np.linalg.norm(
                topocentric.position.km, axis=0, keepdims=True
            )

            # Vectorized angle calculation
            sat_fov_angles = np.arccos(np.sum(topocentricn * icrf, axis=0))
            in_fov_mask = np.degrees(sat_fov_angles) < fov_radius

            if np.any(in_fov_mask):  # Only get alt/az if satellite is ever in FOV
                alt, az, _ = topocentric.altaz()
                fov_indices = np.where(in_fov_mask)[0]

                # Vectorized creation of results
                positions = topocentricn[:, fov_indices]
                ra_decs = np.array(
                    [coordinate_systems.icrf2radec(pos) for pos in positions.T]
                )

                results = [
                    {
                        "ra": ra_dec[0],
                        "dec": ra_dec[1],
                        "altitude": float(alt._degrees[idx]),
                        "azimuth": float(az._degrees[idx]),
                        "name": tle.satellite.sat_name,
                        "norad_id": tle.satellite.sat_number,
                        "julian_date": jd_times[idx],
                        "angle": np.degrees(sat_fov_angles[idx]),
                        "tle_epoch": output_utils.format_date(tle.epoch),
                    }
                    for idx, ra_dec in zip(fov_indices, ra_decs)
                ]

                all_results.extend(results)
                points_in_fov += len(results)

            sat_time = python_time.time() - sat_start
            total_sat_time += sat_time
            satellites_processed += 1

            if satellites_processed % 100 == 0:
                elapsed = python_time.time() - start_time
                avg_sat_time = total_sat_time / satellites_processed
                print(
                    f"Processed {satellites_processed}/{count} "
                    f"satellites in {elapsed:.2f} seconds"
                )
                print(f"Average time per satellite: {avg_sat_time:.3f} seconds")
                print(f"Found {points_in_fov} points in FOV so far")

        except Exception as e:
            print(f"Error processing TLE {tle.satellite.sat_name}: {e}")
            satellites_processed += 1
            continue

    end_time = python_time.time()
    total_time = end_time - start_time
    prop_time = end_time - prop_start

    # Print performance metrics
    print("\nPerformance Metrics:")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(
        f"TLE retrieval time: {tle_time:.2f} seconds ({(tle_time/total_time)*100:.1f}%)"
    )
    print(
        f"Propagation time: {prop_time:.2f} seconds ({(prop_time/total_time)*100:.1f}%)"
    )
    print("\nResults Summary:")
    print(f"Satellites processed: {satellites_processed}/{count}")
    print(f"Points in FOV: {points_in_fov}")
    print(f"End time: {datetime.now().isoformat()}")

    performance_metrics = {
        "total_time": round(total_time, 3),
        "tle_time": round(tle_time, 3),
        "propagation_time": round(prop_time, 3),
        "satellites_processed": satellites_processed,
        "points_in_fov": points_in_fov,
        "jd_times": jd_times.tolist(),
    }

    result = output_utils.fov_data_to_json(
        all_results,
        points_in_fov,
        performance_metrics,
        api_source,
        api_version,
        group_by,
    )

    # Cache only the raw results and points_in_fov
    cache_data = {
        "results": all_results,
        "points_in_fov": points_in_fov,
    }
    redis_client.setex(cache_key, timedelta(hours=1), json.dumps(cache_data))

    return result


def get_satellites_above_horizon(
    tle_repo: AbstractTLERepository,
    location: EarthLocation,
    julian_dates: list[Time],
    min_altitude: float,
    min_range: float,
    max_range: float,
    illuminated_only: bool = False,
    api_source: str = "",
    api_version: str = "",
) -> dict:
    """
    Get all satellites above the horizon at a specific time.

    Args:
        tle_repo: Repository for TLE data
        location: Observer's location
        time_jd: Time to check (as Time object)
        min_altitude: Minimum altitude in degrees (default: 0.0 = horizon)
        api_source: Source of the API call
        api_version: Version of the API
    """
    start_time = python_time.time()
    print(f"\nStarting horizon check at: {datetime.now().isoformat()}")
    print(f"Minimum altitude: {min_altitude}°")
    print(f"Time: {julian_dates}")
    print(f"Location: {location}")

    time_jd = julian_dates[0]

    # Get all current TLEs
    tle_start = python_time.time()
    tles, count = tle_repo.get_all_tles_at_epoch(time_jd.to_datetime(), 1, 10000, "zip")
    tle_time = python_time.time() - tle_start

    # Set up time and observer
    ts = load.timescale()
    t = ts.ut1_jd([time_jd.jd])  # Single time point
    curr_pos = wgs84.latlon(
        location.lat.value, location.lon.value, location.height.value
    )

    all_results = []
    satellites_processed = 0
    visible_satellites = 0

    for tle in tles:
        try:
            satellite = EarthSatellite(tle.tle_line1, tle.tle_line2, ts=ts)
            difference = satellite - curr_pos
            topocentric = difference.at(t)

            # Get altitude and azimuth
            alt, az, distance = topocentric.altaz()

            # Check if above minimum altitude and within range
            if (
                float(alt._degrees[0]) >= min_altitude
                and min_range <= distance.km[0] <= max_range
            ):
                # Get position in RA/Dec
                topocentricn = topocentric.position.km / np.linalg.norm(
                    topocentric.position.km, axis=0
                )
                ra_sat, dec_sat = coordinate_systems.icrf2radec(topocentricn[:, 0])
                if illuminated_only:
                    sat_gcrs = satellite.at(t).position.km
                    illuminated = coordinate_systems.is_illuminated(
                        sat_gcrs[:, 0], time_jd.jd
                    )
                    if not illuminated:
                        continue
                result = {
                    "ra": ra_sat,
                    "dec": dec_sat,
                    "altitude": float(alt._degrees[0]),
                    "azimuth": float(az._degrees[0]),
                    "name": tle.satellite.sat_name,
                    "norad_id": tle.satellite.sat_number,
                    "julian_date": time_jd.jd,
                    "range_km": float(distance.km[0]),
                    "tle_epoch": output_utils.format_date(tle.epoch),
                }
                all_results.append(result)
                visible_satellites += 1

            satellites_processed += 1

            if satellites_processed % 100 == 0:
                elapsed = python_time.time() - start_time
                print(
                    f"Processed {satellites_processed}/{count} satellites in {elapsed:.2f} seconds"  # noqa: E501
                )
                print(f"Found {visible_satellites} visible satellites so far")

        except Exception as e:
            print(f"Error processing Satellite {tle.satellite.sat_name}: {e}")
            satellites_processed += 1
            continue

    end_time = python_time.time()
    total_time = end_time - start_time

    performance_metrics = {
        "total_time": round(total_time, 3),
        "tle_time": round(tle_time, 3),
        "satellites_processed": satellites_processed,
        "visible_satellites": visible_satellites,
    }

    return output_utils.fov_data_to_json(
        all_results, count, performance_metrics, api_source, api_version, "time"
    )
