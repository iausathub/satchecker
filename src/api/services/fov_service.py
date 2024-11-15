import time as python_time
from datetime import datetime

import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from skyfield.api import EarthSatellite, load, wgs84

from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.utils import coordinate_systems, output_utils


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

    return output_utils.fov_data_to_json(
        all_results,
        points_in_fov,
        performance_metrics,
        api_source,
        api_version,
        group_by,
    )
