import concurrent.futures
import multiprocessing
import time
from abc import ABC, abstractmethod
from collections import namedtuple
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Optional, Union

import numpy as np
from astropy import units as u
from astropy.coordinates import EarthLocation
from astropy.time import Time, TimeDelta
from sgp4.api import Satrec
from skyfield.api import EarthSatellite, load, wgs84
from skyfield.nutationlib import iau2000b

from api.adapters.repositories.ephemeris_repository import AbstractEphemerisRepository
from api.domain.models.interpolable_ephemeris import InterpolableEphemeris
from api.utils import coordinate_systems, output_utils
from api.utils.coordinate_systems import (
    az_el_to_ra_dec,
    calculate_current_position,
    calculate_satellite_observer_relative,
    ecef_to_enu,
    ecef_to_itrs,
    enu_to_az_el,
    get_phase_angle,
    icrf2radec,
    is_illuminated,
    is_illuminated_vectorized,
    itrs_to_gcrs,
    load_earth_sun,
    teme_to_ecef,
)
from api.utils.interpolation_utils import (
    InterpolatedSplinesDict,
    generate_and_propagate_sigma_points,
    get_interpolated_sigma_points_KI,
    interpolate_sigma_pointsKI,
    reconstruct_covariance_at_time,
)
from api.utils.time_utils import jd_to_gst

_ts = load.timescale()


def get_timescale():
    return _ts


"""
A named tuple containing the following fields:
    ra (float):
        The right ascension of the satellite relative to observer
        coordinates in ICRS reference frame in degrees. Range of response
        is [0, 360).
    dec (float):
        The declination of the satellite relative to observer
        coordinates in ICRS reference frame in degrees. Range of response
        is [-90, 90].
    alt (float):
        The altitude of the satellite relative to observer
        coordinates in ICRS reference frame in degrees. Range of response
        is [0, 90].
    az (float):
        The azimuth of the satellite relative to observer
        coordinates in ICRS reference frame in degrees. Range of response
        is [0, 360).
    distance (float):
        Range from observer to object in km.
    dracosdec (float):
        Rate of change of right ascension.
    ddec (float):
        Rate of change of declination.
    ddistance (float):
        Rate of change of distance.
    phase_angle (float):
        Phase angle between the satellite, observer, and the Sun.
    sat_altitude_km (float):
        Satellite altitude above Earth's surface in km.
    solar_elevation_deg (float):
        Solar elevation angle in degrees.
    solar_azimuth_deg (float):
        Solar azimuth angle in degrees.
    illuminated (bool):
        Whether the satellite is illuminated.
    satellite_gcrs (list):
        Satellite coordinates in GCRS.
    observer_gcrs (list):
        Observer coordinates in GCRS.
    julian_date (float):
        The input Julian date.
"""
satellite_position = namedtuple(
    "satellite_position",
    [
        "ra",
        "dec",
        "dracosdec",
        "ddec",
        "alt",
        "az",
        "distance",
        "ddistance",
        "phase_angle",
        "sat_altitude_km",
        "solar_elevation_deg",
        "solar_azimuth_deg",
        "illuminated",
        "satellite_gcrs",
        "observer_gcrs",
        "julian_date",
    ],
)


satellite_position_fov = namedtuple(
    "satellite_position_fov",
    [
        "ra",
        "dec",
        "covariance",
        "angle",
        "altitude",
        "azimuth",
        "range_km",
        "julian_date",
        "name",
        "norad_id",
        "propagation_epoch",
        "propagation_source",
    ],
)


class BasePropagationStrategy(ABC):
    """Base class for all propagation strategies."""

    @abstractmethod
    def propagate(
        self,
        julian_dates: Union[float, list[float], np.ndarray],
        tle_line_1: str,
        tle_line_2: str,
        latitude: float,
        longitude: float,
        elevation: float,
        **kwargs,
    ) -> Union[
        satellite_position,
        list[satellite_position],
        list[satellite_position_fov],
        list[dict[str, Any]],
    ]:
        """
        Propagate satellite positions.

        Args:
            julian_dates: Single Julian date or array of Julian dates
            tle_line_1: First line of TLE
            tle_line_2: Second line of TLE
            latitude: Observer latitude in degrees
            longitude: Observer longitude in degrees
            elevation: Observer elevation in meters
            **kwargs: Additional strategy-specific parameters

        Returns:
            Propagated position(s) in the strategy's format
        """
        pass


class SkyfieldPropagationStrategy(BasePropagationStrategy):
    def propagate(
        self,
        julian_dates: Union[float, list[float], np.ndarray],
        tle_line_1: str,
        tle_line_2: str,
        latitude: float,
        longitude: float,
        elevation: float,
        **kwargs,
    ) -> list[satellite_position]:
        """
        Use Skyfield (https://rhodesmill.org/skyfield/earth-satellites.html)
        to propagate satellite and observer states.

        Args:
            julian_dates: Single Julian date or array of Julian dates
            tle_line_1: TLE line 1
            tle_line_2: TLE line 2
            latitude: The observer WGS84 latitude in degrees
            longitude: The observers WGS84 longitude in degrees (positive value
                represents east, negative value represents west)
            elevation: The observer elevation above WGS84 ellipsoid in meters
            **kwargs: Additional parameters (not used in this strategy)

        Returns:
            List of propagated positions

        Raises:
            RuntimeError: If propagation fails due to invalid TLE
            or numerical instability
        """
        # Convert single date to list for consistent handling
        if isinstance(julian_dates, (float, int)):
            julian_dates = [julian_dates]

        try:
            ts = get_timescale()
            satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)
            curr_pos = wgs84.latlon(latitude, longitude, elevation)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize propagation: {str(e)}") from e

        results = []
        for julian_date in julian_dates:
            try:
                jd = Time(julian_date, format="jd", scale="ut1")

                if jd.jd == 0:
                    # Use ts.ut1_jd instead of ts.from_astropy because from_astropy uses
                    # astropy.Time.TT.jd instead of UT1
                    t = ts.ut1_jd(satellite.model.jdsatepoch)
                else:
                    t = ts.ut1_jd(jd.jd)

                difference = satellite - curr_pos
                topocentric = difference.at(t)
                position_norm = np.linalg.norm(topocentric.position.km)
                if position_norm == 0:
                    raise RuntimeError(
                        f"Zero magnitude position vector " f"at JD {julian_date}"
                    )

                topocentricn = topocentric.position.km / position_norm

                ra, dec, distance = topocentric.radec()
                alt, az, distance = topocentric.altaz()

                dtday = TimeDelta(1, format="sec")
                tplusdt = ts.ut1_jd((jd + dtday).jd)
                tminusdt = ts.ut1_jd((jd - dtday).jd)

                dtsec = 1
                dtx2 = 2 * dtsec

                sat_gcrs = satellite.at(t).position.km

                # satn = sat / np.linalg.norm(sat)
                # satpdt = satellite.at(tplusdt).position.km
                # satmdt = satellite.at(tminusdt).position.km
                # vsat = (satpdt - satmdt) / dtx2
                sattop = difference.at(t).position.km
                sattopr = np.linalg.norm(sattop)
                if sattopr == 0:
                    raise RuntimeError(
                        f"Zero magnitude topocentric vector " f"at JD {julian_date}"
                    )

                sattopn = sattop / sattopr
                sattoppdt = difference.at(tplusdt).position.km
                sattopmdt = difference.at(tminusdt).position.km

                ratoppdt, dectoppdt = icrf2radec(sattoppdt)
                ratopmdt, dectopmdt = icrf2radec(sattopmdt)

                vsattop = (sattoppdt - sattopmdt) / dtx2

                ddistance = np.dot(vsattop, sattopn)
                rxy = np.dot(sattop[0:2], sattop[0:2])
                if rxy == 0:
                    raise RuntimeError(
                        f"Zero magnitude XY projection at JD {julian_date}"
                    )

                dra = (sattop[1] * vsattop[0] - sattop[0] * vsattop[1]) / rxy
                denominator = np.sqrt(1 - sattopn[2] * sattopn[2])
                if denominator == 0:
                    raise RuntimeError(
                        f"Invalid position vector for declination rate "
                        f"at JD {julian_date}"
                    )

                ddec = vsattop[2] / denominator
                dracosdec = dra * np.cos(dec.radians)

                dra = (ratoppdt - ratopmdt) / dtx2
                ddec = (dectoppdt - dectopmdt) / dtx2
                dracosdec = dra * np.cos(dec.radians)

                # drav, ddecv = icrf2radec(vsattop / sattopr, unit_vector=True)
                # dracosdecv = drav * np.cos(dec.radians)
                obs_gcrs = curr_pos.at(t).position.km
                phase_angle = get_phase_angle(topocentricn, sat_gcrs, julian_date)

                # Get solar altitude and azimuth
                earth, sun = load_earth_sun()
                sun_relative_to_earth = sun - earth
                sun_relative_to_observer = sun_relative_to_earth - curr_pos

                solar_alt, solar_az, _ = sun_relative_to_observer.at(t).altaz()
                solar_elevation_deg = solar_alt.degrees
                solar_azimuth_deg = solar_az.degrees

                illuminated = is_illuminated(sat_gcrs, julian_date)

                # Calculate satellite altitude above Earth's surface
                sat_altitude_km = wgs84.height_of(satellite.at(t)).km

                results.append(
                    satellite_position(
                        ra._degrees,
                        dec.degrees,
                        dracosdec,
                        ddec,
                        alt._degrees,
                        az._degrees,
                        distance.km,
                        ddistance,
                        phase_angle,
                        sat_altitude_km,
                        solar_elevation_deg,
                        solar_azimuth_deg,
                        illuminated,
                        sat_gcrs.tolist(),
                        obs_gcrs.tolist(),
                        julian_date,
                    )
                )
            except Exception as e:
                raise RuntimeError(
                    f"Propagation failed at JD {julian_date}: {str(e)}"
                ) from e

        return results


class SGP4PropagationStrategy(BasePropagationStrategy):  # pragma: no cover
    def propagate(
        self,
        julian_dates: Union[float, list[float], np.ndarray],
        tle_line_1: str,
        tle_line_2: str,
        latitude: float,
        longitude: float,
        elevation: float,
        **kwargs,
    ) -> Union[satellite_position, list[satellite_position]]:
        """
        Propagates satellite and observer states using the SGP4 propagation model.

        Args:
            julian_dates: Single Julian date or array of Julian dates
            tle_line_1: First line of TLE
            tle_line_2: Second line of TLE
            latitude: Observer latitude in degrees
            longitude: Observer longitude in degrees
            elevation: Observer elevation in meters above the WGS84 ellipsoid.
            **kwargs: Additional parameters (not used in this strategy)

        Returns:
            Single satellite position or list of positions
        """
        # Convert single date to list for consistent handling
        if isinstance(julian_dates, (float, int)):
            julian_dates = [julian_dates]

        results = []
        observer_location = EarthLocation(
            lat=latitude * u.deg, lon=longitude * u.deg, height=elevation * u.m
        )
        location_itrs = observer_location.itrs.cartesian.xyz.value / 1000
        for julian_date in julian_dates:

            # Compute the coordinates of the CIP (Celestial Intermediate Pole)
            dpsi, deps = iau2000b(julian_date)

            # Compute the nutation in longitude
            nutation_arcsec = dpsi / 10000000  # Convert from arcseconds to degrees
            nutation = nutation_arcsec / 3600

            location_itrs = np.array(location_itrs)
            theta_gst = jd_to_gst(julian_date, nutation)
            obs_gcrs = observer_location.get_gcrs(
                obstime=Time(julian_date, format="jd")
            )

            # Split Julian Date into integer and fractional parts for full accuracy
            # See Usage note here: https://pypi.org/project/sgp4/
            jd_int = int(julian_date)
            jd_frac = julian_date - jd_int

            # Propagate satellite
            satellite = Satrec.twoline2rv(tle_line_1, tle_line_2)
            error, r, v = satellite.sgp4(jd_int, jd_frac)

            r_ecef = teme_to_ecef(r, theta_gst)
            difference = r_ecef - location_itrs
            latitude = observer_location.lat.value
            longitude = observer_location.lon.value
            r_enu = ecef_to_enu(difference, latitude, longitude)

            # Az, Alt, RA, Dec
            az, alt = enu_to_az_el(r_enu)
            ra, dec = az_el_to_ra_dec(az, alt, latitude, longitude, julian_date)

            # Convert ECEF to ITRS
            r_itrs = ecef_to_itrs(r_ecef)

            # Convert ITRS to GCRS
            sat_gcrs = itrs_to_gcrs(r_itrs, julian_date)
            topocentric_gcrs = itrs_to_gcrs(ecef_to_itrs(difference), julian_date)
            topocentric_gcrs_norm = topocentric_gcrs / np.linalg.norm(topocentric_gcrs)

            # phase angle
            phase_angle = get_phase_angle(topocentric_gcrs_norm, sat_gcrs, julian_date)
            illuminated = is_illuminated(sat_gcrs, julian_date)

            # TODO: Implement distance, dracosdec, ddec, ddistance for SGP4
            dracosdec = None
            ddec = None
            distance = None
            ddistance = None

            obs_gcrs = observer_location.get_gcrs_posvel(
                obstime=Time(julian_date, format="jd")
            )
            obs_gcrs = obs_gcrs[0].xyz.value / 1000

            results.append(
                satellite_position(
                    ra,
                    dec,
                    dracosdec,
                    ddec,
                    alt,
                    az,
                    distance,
                    ddistance,
                    phase_angle,
                    None,  # sat_altitude_km - not calculated in SGP4
                    None,
                    None,
                    illuminated,
                    sat_gcrs.tolist() if sat_gcrs is not None else None,
                    obs_gcrs.tolist() if obs_gcrs is not None else None,
                    julian_date,
                )
            )

        return results[0] if len(results) == 1 else results


class TestPropagationStrategy(BasePropagationStrategy):  # pragma: no cover
    def propagate(
        self,
        julian_dates: Union[float, list[float], np.ndarray],
        tle_line_1: str,
        tle_line_2: str,
        latitude: float,
        longitude: float,
        elevation: float,
        **kwargs,
    ) -> Union[satellite_position, list[satellite_position]]:
        """
        Test propagation strategy that uses Skyfield implementation.

        Args:
            julian_dates: Single Julian date or array of Julian dates
            tle_line_1: First line of TLE
            tle_line_2: Second line of TLE
            latitude: Observer latitude in degrees
            longitude: Observer longitude in degrees
            elevation: Observer elevation in meters
            **kwargs: Additional parameters (not used in this strategy)

        Returns:
            Single satellite position or list of positions
        """
        # Convert single date to list for consistent handling
        if isinstance(julian_dates, (float, int)):
            julian_dates = [julian_dates]

        results = []
        for julian_date in julian_dates:
            ts = get_timescale()
            eph = load("de430t.bsp")
            earth = eph["Earth"]
            sun = eph["Sun"]
            satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)
            curr_pos = calculate_current_position(latitude, longitude, elevation)

            jd = Time(julian_date, format="jd", scale="ut1")
            if jd.jd == 0:
                t = ts.ut1_jd(satellite.model.jdsatepoch)
            else:
                t = ts.ut1_jd(jd.jd)

            difference = satellite - curr_pos
            topocentric = difference.at(t)
            topocentricn = topocentric.position.km / np.linalg.norm(
                topocentric.position.km
            )

            ra, dec, distance = topocentric.radec()
            alt, az, distance = topocentric.altaz()

            dtday = TimeDelta(1, format="sec")
            tplusdt = ts.ut1_jd((jd + dtday).jd)
            tminusdt = ts.ut1_jd((jd - dtday).jd)

            dtsec = 1
            dtx2 = 2 * dtsec

            sat = satellite.at(t).position.km

            sattop = difference.at(t).position.km
            sattopr = np.linalg.norm(sattop)
            sattopn = sattop / sattopr
            sattoppdt = difference.at(tplusdt).position.km
            sattopmdt = difference.at(tminusdt).position.km

            ratoppdt, dectoppdt = icrf2radec(sattoppdt)
            ratopmdt, dectopmdt = icrf2radec(sattopmdt)

            vsattop = (sattoppdt - sattopmdt) / dtx2

            ddistance = np.dot(vsattop, sattopn)
            rxy = np.dot(sattop[0:2], sattop[0:2])
            dra = (sattop[1] * vsattop[0] - sattop[0] * vsattop[1]) / rxy
            ddec = vsattop[2] / np.sqrt(1 - sattopn[2] * sattopn[2])
            dracosdec = dra * np.cos(dec.radians)

            dra = (ratoppdt - ratopmdt) / dtx2
            ddec = (dectoppdt - dectopmdt) / dtx2
            dracosdec = dra * np.cos(dec.radians)

            earthp = earth.at(t).position.km
            sunp = sun.at(t).position.km
            earthsun = sunp - earthp
            earthsunn = earthsun / np.linalg.norm(earthsun)
            satsun = sat - earthsun
            satsunn = satsun / np.linalg.norm(satsun)
            phase_angle = np.rad2deg(np.arccos(np.dot(satsunn, topocentricn)))

            illuminated = is_illuminated(sat, earthsunn)

            results.append(
                satellite_position(
                    ra._degrees,
                    dec.degrees,
                    dracosdec,
                    ddec,
                    alt.degrees,
                    az.degrees,
                    distance.km,
                    ddistance,
                    phase_angle,
                    None,
                    None,
                    None,
                    illuminated,
                    None,  # satellite_gcrs
                    None,  # observer_gcrs
                    jd.jd,
                )
            )

        return results[0] if len(results) == 1 else results


# remove pragma: no cover if another use is found for this
class FOVPropagationStrategy(BasePropagationStrategy):
    def propagate(
        self,
        julian_dates: Union[float, list[float], np.ndarray],
        tle_line_1: str,
        tle_line_2: str,
        latitude: float,
        longitude: float,
        elevation: float,
        fov_center: tuple[float, float] = (0.0, 0.0),  # Default to (0,0)
        fov_radius: float = 0.0,  # Default to 0 degrees
        **kwargs,
    ) -> list[dict[str, Any]]:  # pragma: no cover
        """
        Propagate satellite positions and check if they fall within FOV.

        Args:
            julian_dates: Single Julian date or array of Julian dates
            tle_line_1: First line of TLE
            tle_line_2: Second line of TLE
            latitude: Observer latitude in degrees
            longitude: Observer longitude in degrees
            elevation: Observer elevation in meters
            fov_center: Tuple of (RA, Dec) in degrees. Defaults to (0,0)
            fov_radius: FOV radius in degrees. Defaults to 0
            **kwargs: Additional parameters (not used in this strategy)

        Returns:
            List of dictionaries containing position data for points in FOV

        Raises:
            RuntimeError: If propagation fails due to invalid TLE
            or numerical instability
        """
        # Convert single date to list for consistent handling
        if isinstance(julian_dates, (float, int)):
            julian_dates = [julian_dates]

        try:
            ts = get_timescale()
            t = ts.ut1_jd(julian_dates)

            # Set up observer and FOV vectors
            curr_pos = wgs84.latlon(latitude, longitude, elevation)
            icrf = coordinate_systems.radec2icrf(fov_center[0], fov_center[1]).reshape(
                3, 1
            )

            # Create satellite and get positions
            satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)
            difference = satellite - curr_pos
            topocentric = difference.at(t)
            position_norm = np.linalg.norm(
                topocentric.position.km, axis=0, keepdims=True
            )
            if np.any(position_norm == 0):
                raise RuntimeError("Zero magnitude position vector detected")

            topocentricn = topocentric.position.km / position_norm

            # Vectorized angle calculation
            sat_fov_angles = np.arccos(np.sum(topocentricn * icrf, axis=0))
            in_fov_mask = np.degrees(sat_fov_angles) < fov_radius

            if not np.any(in_fov_mask):
                return []

            # Get alt/az for points in FOV
            alt, az, distance = topocentric.altaz()
            fov_indices = np.where(in_fov_mask)[0]

            # Vectorized creation of results
            positions = topocentricn[:, fov_indices]
            ra_decs = np.array(
                [coordinate_systems.icrf2radec(pos) for pos in positions.T]
            )

            return [
                {
                    "ra": ra_dec[0],
                    "dec": ra_dec[1],
                    "altitude": float(alt._degrees[idx]),
                    "azimuth": float(az._degrees[idx]),
                    "range_km": float(distance.km[idx]),
                    "julian_date": julian_dates[idx],
                    "angle": np.degrees(sat_fov_angles[idx]),
                }
                for idx, ra_dec in zip(fov_indices, ra_decs)
            ]

        except Exception as e:
            raise RuntimeError(f"FOV propagation failed: {str(e)}") from e


def process_satellite_batch(args):
    """Process a batch of satellites for FOV calculations."""
    (
        tle_batch,
        julian_dates,
        lat,
        lon,
        elev,
        fov_center,
        fov_radius,
        include_tles,
        illuminated_only,
    ) = args

    # Convert single date to list for consistent handling
    if isinstance(julian_dates, (float, int)):
        julian_dates = [julian_dates]

    ts = get_timescale()
    t = ts.ut1_jd(julian_dates)

    # Set up observer and FOV vectors
    curr_pos = wgs84.latlon(lat, lon, elev)  # do here because of serialization
    icrf = coordinate_systems.radec2icrf(fov_center[0], fov_center[1]).reshape(3, 1)

    batch_results = []
    satellites_processed = 0

    for tle in tle_batch:
        try:
            # Create satellite
            satellite = EarthSatellite(tle.tle_line1, tle.tle_line2, ts=ts)

            difference = satellite - curr_pos
            topocentric = difference.at(t)
            topocentricn = topocentric.position.km / np.linalg.norm(
                topocentric.position.km, axis=0, keepdims=True
            )

            # Vectorized angle calculation
            sat_fov_angles = np.arccos(np.sum(topocentricn * icrf, axis=0))
            in_fov_mask = (
                np.degrees(sat_fov_angles) < fov_radius * 1.2
            )  # add 20% margin
            if illuminated_only:
                # only show points that are illuminated
                sat_gcrs = [
                    satellite.at(ts.ut1_jd(jd)).position.km for jd in julian_dates
                ]
                illuminated = is_illuminated_vectorized(sat_gcrs, julian_dates)
                visible_mask = np.logical_and(in_fov_mask, illuminated)
            else:
                visible_mask = in_fov_mask

            if not np.any(visible_mask):
                satellites_processed += 1
                continue

            # Get alt/az for points in FOV
            alt, az, distance = topocentric.altaz()
            fov_indices = np.where(in_fov_mask)[0]

            # Vectorized creation of results
            positions = topocentricn[:, fov_indices]
            ra_decs = np.array(
                [coordinate_systems.icrf2radec(pos) for pos in positions.T]
            )

            # Prepare results with conditional TLE data
            result_entries = []
            for idx, ra_dec in zip(fov_indices, ra_decs):
                result = {
                    "ra": ra_dec[0],
                    "dec": ra_dec[1],
                    "altitude": float(alt._degrees[idx]),
                    "azimuth": float(az._degrees[idx]),
                    "range_km": float(distance.km[idx]),
                    "julian_date": julian_dates[idx],
                    "angle": np.degrees(sat_fov_angles[idx]),
                    "name": tle.satellite.sat_name,
                    "norad_id": tle.satellite.sat_number,
                    "tle_epoch": output_utils.format_date(tle.epoch),
                }

                # Only include TLE data if requested
                if include_tles:
                    result["tle_data"] = {
                        "tle_line1": tle.tle_line1,
                        "tle_line2": tle.tle_line2,
                        "source": tle.data_source,
                    }

                result_entries.append(result)

            batch_results.extend(result_entries)
            satellites_processed += 1

        except Exception as e:
            print(f"Error processing satellite {tle.satellite.sat_name}: {e}")
            satellites_processed += 1

    return batch_results, satellites_processed


class FOVParallelPropagationStrategy:
    def propagate(
        self,
        all_tles,
        jd_times,
        location,
        fov_center,
        fov_radius,
        batch_size=1000,
        max_workers=None,
        include_tles=True,
        illuminated_only=False,
    ) -> tuple[list[dict[str, Any]], float, int]:
        """
        Propagate satellite positions and check if they fall within FOV.

        Args:
            all_tles: List of TLE objects
            jd_times: Array of Julian dates
            location: Observer's location
            fov_center: Tuple of (RA, Dec) in degrees. Defaults to (0,0)
            fov_radius: FOV radius in degrees. Defaults to 0
            batch_size: Number of satellites to process in each batch
            max_workers: Maximum number of worker processes to use
            include_tles: Whether to include TLE data in results
            **kwargs: Additional parameters (not used in this strategy)

        Returns:
            tuple: (
                results: List of dictionaries containing position data for points
                in FOV,
                execution_time: Total execution time in seconds,
                satellites_processed: Number of satellites processed
            )
        """
        """Process FOV calculations in parallel."""
        all_results = []
        start_time = time.time()
        satellites_processed = 0

        # Default to number of CPU cores
        if max_workers is None:
            max_workers = min(multiprocessing.cpu_count(), 16)  # Cap at 16 workers

        lat = location.lat.value
        lon = location.lon.value
        elev = location.height.value

        # Create batches of satellites
        satellite_batches = []
        for i in range(0, len(all_tles), batch_size):
            batch = all_tles[i : i + batch_size]
            satellite_batches.append(batch)

        args_list = [
            (
                batch,
                jd_times,
                lat,
                lon,
                elev,
                fov_center,
                fov_radius,
                include_tles,
                illuminated_only,
            )
            for batch in satellite_batches
        ]

        print(
            f"Processing {len(all_tles)} satellites in {len(satellite_batches)} batches"
            f" ({max_workers} workers)"
        )

        # Process batches in parallel
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            completed = 0
            futures = []

            for args in args_list:
                futures.append(executor.submit(process_satellite_batch, args))

            # Collect results as they complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    batch_results, batch_satellites = future.result()
                    all_results.extend(batch_results)
                    satellites_processed += batch_satellites
                    completed += 1
                    print(f"Batch {completed}/{len(satellite_batches)} complete")
                except Exception as e:
                    print(f"Error processing batch: {e}")

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Total execution time: {execution_time:.2f} seconds")

        return all_results, execution_time, satellites_processed


class KroghPropagationStrategy(BasePropagationStrategy):  # pragma: no cover
    def __init__(self):
        """Initialize the Krogh propagation strategy."""
        self.ephemeris_data: Optional[InterpolableEphemeris] = None
        self.sigma_points_dict: Optional[dict] = None
        self.interpolated_splines: Optional[InterpolatedSplinesDict] = None

    def load_ephemeris(
        self, ephemeris: InterpolableEphemeris, ephem_repo: AbstractEphemerisRepository
    ) -> None:
        """
        Load and parse ephemeris data from a file.

        Args:
            sat_number: Satellite NORAD number
            epoch: Epoch time for the ephemeris
        """
        self.ephemeris_data = ephemeris

        # Generate sigma points for this specific ephemeris
        import time

        start_time = time.time()
        print(f"Generating sigma points for ephemeris {ephemeris.id}")
        self.sigma_points_dict = generate_and_propagate_sigma_points(
            self.ephemeris_data
        )
        sigma_time = time.time() - start_time
        print(f"Sigma points generation took {sigma_time:.2f} seconds")

        # Generate splines on-demand since we disabled database storage
        start_time = time.time()
        print(f"Generating interpolated splines for ephemeris {ephemeris.id}")
        if ephemeris.id is None:
            raise ValueError(
                "Ephemeris ID is None, cannot retrieve interpolator splines"
            )
        interpolated_splines_obj = ephem_repo.get_interpolator_splines(ephemeris.id)
        if interpolated_splines_obj is None:
            interpolated_splines = interpolate_sigma_pointsKI(self.sigma_points_dict)
        else:
            interpolated_splines = interpolated_splines_obj.get_interpolated_splines()
        self.interpolated_splines = interpolated_splines
        spline_time = time.time() - start_time
        print(f"Spline generation took {spline_time:.2f} seconds")

    def propagate(
        self,
        julian_dates: Union[float, list[float], np.ndarray],
        tle_line_1: str,
        tle_line_2: str,
        latitude: float,
        longitude: float,
        elevation: float,
        **kwargs,
    ) -> list[satellite_position_fov]:
        """
        Propagate satellite positions using Krogh interpolation.

        Args:
            julian_dates: Single Julian date or array of Julian dates
            tle_line_1: First line of TLE (not used in this strategy)
            tle_line_2: Second line of TLE (not used in this strategy)
            latitude: Observer latitude in degrees
            longitude: Observer longitude in degrees
            elevation: Observer elevation in meters
            **kwargs: Additional parameters (not used in this strategy)

        Returns:
            List of satellite positions
        """
        if self.interpolated_splines is None:
            raise ValueError("No ephemeris data loaded. Call load_ephemeris() first.")

        # Convert single date to list for consistent handling
        if isinstance(julian_dates, (float, int)):
            julian_dates = [julian_dates]

        results = []
        for jd in julian_dates:
            # Get interpolated sigma points
            interpolated_points = get_interpolated_sigma_points_KI(
                self.interpolated_splines, jd
            )

            # Reconstruct mean state and covariance
            mean_state, covariance = reconstruct_covariance_at_time(interpolated_points)

            # Extract position from mean state (first 3 components)
            satellite_position_gcrs = mean_state[:3]

            # Calculate observer position in GCRS
            observer_location = EarthLocation(
                lat=latitude * u.deg, lon=longitude * u.deg, height=elevation * u.m
            )
            obs_gcrs = (
                observer_location.get_gcrs(
                    obstime=Time(jd, format="jd")
                ).cartesian.xyz.value
                / 1000
            )  # Convert to km

            # Calculate topocentric position (satellite - observer) in GCRS
            topocentric_gcrs = satellite_position_gcrs - obs_gcrs

            # Convert topocentric GCRS position to RA/Dec
            ra, dec = icrf2radec(topocentric_gcrs)

            # Calculate observer-relative coordinates for altitude/azimuth
            altitude, azimuth, range_km = calculate_satellite_observer_relative(
                satellite_position_gcrs, latitude, longitude, elevation, jd
            )

            # Convert to satellite position format
            results.append(
                satellite_position_fov(
                    ra=ra,
                    dec=dec,
                    covariance=covariance,
                    angle=None,
                    altitude=altitude,
                    azimuth=azimuth,
                    range_km=range_km,
                    julian_date=float(jd),  # Ensure jd is a float
                    name=None,  # added in fov_service
                    norad_id=None,  # added in fov_service
                    propagation_epoch=None,  # added in fov_service
                    propagation_source=None,  # added in fov_service
                )
            )

        return results


class PropagationInfo:
    def __init__(
        self,
        propagation_strategy,
        tle_line_1,
        tle_line_2,
        julian_date,
        latitude,
        longitude,
        elevation,
    ):
        self.propagation_strategy = propagation_strategy
        self.tle_line_1 = tle_line_1
        self.tle_line_2 = tle_line_2
        self.julian_date = julian_date
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def propagate(self):
        return self.propagation_strategy.propagate(
            self.julian_date,
            self.tle_line_1,
            self.tle_line_2,
            self.latitude,
            self.longitude,
            self.elevation,
        )
