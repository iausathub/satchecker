import time as python_time
from datetime import datetime

import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from skyfield.api import EarthSatellite, load, wgs84

from api.adapters.repositories.satellite_repository import AbstractSatelliteRepository
from api.adapters.repositories.tle_repository import AbstractTLERepository
from api.utils import coordinate_systems


def get_satellite_passes_in_fov(
    sat_repo: AbstractSatelliteRepository,
    tle_repo: AbstractTLERepository,
    location: EarthLocation,
    mid_obs_time_jd: Time,
    duration: float,
    ra: float,
    dec: float,
    fov_radius: float,
    api_source: str,
    api_version: str,
) -> list[dict]:
    start_time = python_time.time()
    print(f"\nStarting FOV calculation at: {datetime.now().isoformat()}")
    print(f"FOV Parameters: RA={ra}°, Dec={dec}°, Radius={fov_radius}°")
    print(f"Duration: {duration} seconds")

    # Get all current TLEs
    tle_start = python_time.time()
    tles, count = tle_repo.get_all_tles_at_epoch(
        mid_obs_time_jd.to_datetime(), 1, 10000, "zip"
    )
    tle_time = python_time.time() - tle_start
    print(f"Retrieved {count} TLEs in {tle_time:.2f} seconds")
    ts = load.timescale()

    time_step = 1 / 86400  # 1 second
    # Get times to check based on the mid point of the observation and the duration
    # the mid point is in JD and the duration is in seconds, use a time step of 1 second

    # convert duration to JD
    duration_jd = duration / 86400

    prop_start = python_time.time()
    jd_times = np.arange(
        mid_obs_time_jd.jd - duration_jd / 2,
        mid_obs_time_jd.jd + duration_jd / 2,
        time_step,
    )
    t = ts.ut1_jd(jd_times)  # Convert entire array to Skyfield time objects
    print(f"Checking {len(jd_times)} time points")

    # Set up observer position once
    curr_pos = wgs84.latlon(
        location.lat.value, location.lon.value, location.height.value
    )

    all_results = []
    satellites_processed = 0
    points_in_fov = 0
    total_sat_time = 0

    # Prepare ICRF vector once
    icrf = coordinate_systems.radec2icrf(ra, dec)
    icrf = icrf.reshape(3, 1)  # Reshape for broadcasting

    for tle in tles:
        sat_start = python_time.time()
        try:
            satellite = EarthSatellite(tle.tle_line1, tle.tle_line2, ts=ts)
            difference = satellite - curr_pos

            # Propagate all times at once
            topocentric = difference.at(t)
            topocentricn = topocentric.position.km / np.linalg.norm(
                topocentric.position.km, axis=0, keepdims=True
            )

            # Calculate angles for all times at once
            sat_fov_angles = np.arccos(np.sum(topocentricn * icrf, axis=0))

            # Find times where satellite is in FOV
            in_fov_mask = np.degrees(sat_fov_angles) < fov_radius

            # Process only the points that are in FOV
            for i, in_fov in enumerate(in_fov_mask):
                if in_fov:
                    # Get RA/Dec for this position
                    this_pos = topocentricn[:, i]
                    ra_sat, dec_sat = coordinate_systems.icrf2radec(this_pos)

                    satellite_pass = {
                        "ra": ra_sat,
                        "dec": dec_sat,
                        "name": tle.satellite.sat_name,
                        "norad_id": tle.satellite.sat_number,
                        "julian_date": jd_times[i],
                        "angle": np.degrees(sat_fov_angles[i]),
                    }
                    all_results.append(satellite_pass)
                    points_in_fov += 1

            sat_time = python_time.time() - sat_start
            total_sat_time += sat_time
            satellites_processed += 1

            if satellites_processed % 100 == 0:
                elapsed = python_time.time() - start_time
                avg_sat_time = total_sat_time / satellites_processed
                print(
                    f"Processed {satellites_processed}/{count} satellites in {elapsed:.2f} seconds"  # noqa: E501
                )
                print(f"Average time per satellite: {avg_sat_time:.3f} seconds")
                print(f"Found {points_in_fov} points in FOV so far")

        except Exception as e:
            print(f"Error processing TLE {tle.satellite.sat_name}: {e}")
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
    print(
        f"Average time per satellite: {total_sat_time/satellites_processed:.3f} seconds"
    )
    print("\nResults Summary:")
    print(f"Satellites processed: {satellites_processed}/{count}")
    print(f"Points in FOV: {points_in_fov}")
    print(f"End time: {datetime.now().isoformat()}")

    return all_results
