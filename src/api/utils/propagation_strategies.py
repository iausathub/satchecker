import concurrent.futures
import multiprocessing
import time
from abc import ABC, abstractmethod
from collections import namedtuple
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Union

import julian
import numpy as np
from astropy import units as u
from astropy.coordinates import EarthLocation
from astropy.time import Time, TimeDelta
from scipy.interpolate import KroghInterpolator
from scipy.linalg import sqrtm
from sgp4.api import Satrec
from skyfield.api import EarthSatellite, load, wgs84
from skyfield.nutationlib import iau2000b

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
            in_fov_mask = np.degrees(sat_fov_angles) < fov_radius
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
        self.ephemeris_data = None
        self.sigma_points_dict = None
        self.interpolated_splines = None

    def load_ephemeris(self, ephemeris: InterpolableEphemeris) -> None:
        """
        Load and parse ephemeris data from a file.

        Args:
            sat_number: Satellite NORAD number
            epoch: Epoch time for the ephemeris
        """
        self.ephemeris_data = ephemeris
        self.sigma_points_dict = self._generate_and_propagate_sigma_points(
            self.ephemeris_data
        )
        self.interpolated_splines = self._interpolate_sigma_pointsKI(
            self.sigma_points_dict
        )

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
            interpolated_points = self._get_interpolated_sigma_points_KI(
                self.interpolated_splines, jd
            )

            # Reconstruct mean state and covariance
            mean_state, covariance = self._reconstruct_covariance_at_time(
                interpolated_points
            )

            # Extract position from mean state (first 3 components)
            satellite_position_gcrs = mean_state[:3]

            # Calculate observer-relative coordinates
            altitude, azimuth, range_km = calculate_satellite_observer_relative(
                satellite_position_gcrs, latitude, longitude, elevation, jd
            )

            # Convert to satellite position format
            results.append(
                satellite_position_fov(
                    ra=mean_state[0],
                    dec=mean_state[1],
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

    def _generate_and_propagate_sigma_points(
        self, ephemeris: InterpolableEphemeris
    ) -> dict:
        """
        Generate and propagate sigma points using the Unscented Transform for improved
        numerical stability.

        This method implements the Unscented Transform to generate sigma points from
        the state vectors and covariance matrices in the ephemeris data. The sigma
        points are used to capture the mean and covariance of the state distribution
        more accurately than linearization methods.

        The method uses optimized parameters for the Unscented Transform:
        - alpha = 0.001 (reduced for better numerical stability)
        - beta = 2.0 (optimal for Gaussian distributions)
        - kappa = 3-n (modified for better stability)

        Args:
            ephemeris (InterpolableEphemeris): The ephemeris data containing state
            vectors and covariance matrices.

        Returns:
            dict: A dictionary mapping Julian dates to sigma point information:
                - sigma_points (np.ndarray): Array of 13 sigma points (6D state vectors)
                - weights (dict): Dictionary containing mean and covariance weights
                - epoch (datetime): Timestamp for these sigma points
                - state_vector (np.ndarray): Original state vector
                - covariance (np.ndarray): Original covariance matrix

        Raises:
            ValueError: If no sigma points could be generated successfully
            np.linalg.LinAlgError: If covariance matrix is not positive definite

        Note:
            The method uses Cholesky decomposition for numerical stability,
            falling back to matrix square root if Cholesky fails. Each sigma
            point set contains 13 points:
            - 1 mean state point
            - 6 points from positive Cholesky decomposition
            - 6 points from negative Cholesky decomposition
        """
        try:
            # Use high precision for Julian date conversion
            julian_dates = np.array(
                [float(julian.to_jd(point.timestamp)) for point in ephemeris.points],
                dtype=np.float64,
            )

            # Stack positions and velocities into state vectors
            state_vectors = np.hstack(
                (
                    np.array(
                        [point.position for point in ephemeris.points], dtype=np.float64
                    ),
                    np.array(
                        [point.velocity for point in ephemeris.points], dtype=np.float64
                    ),
                )
            )
            covariances = np.array(
                [point.covariance for point in ephemeris.points], dtype=np.float64
            )

            sigma_points_dict = {}

            # Optimized Unscented Transform parameters
            n = 6
            alpha = np.float64(0.001)  # Reduced alpha for better numerical stability
            beta = np.float64(2.0)  # Optimal for Gaussian
            kappa = np.float64(3 - n)  # Modified for better stability
            lambda_param = alpha * alpha * (n + kappa) - n

            # Precompute weights for efficiency and precision
            w0_m = lambda_param / (n + lambda_param)
            wn_m = np.float64(0.5) / (n + lambda_param)
            w0_c = w0_m + (1 - alpha * alpha + beta)
            wn_c = wn_m

            weights = {
                "mean": {"w0": w0_m, "wn": wn_m},
                "covariance": {"w0": w0_c, "wn": wn_c},
            }

            for idx, (jd, point) in enumerate(zip(julian_dates, ephemeris.points)):
                try:
                    state_vector = state_vectors[idx]
                    covariance = covariances[idx]

                    # Ensure symmetry of covariance matrix
                    covariance = (covariance + covariance.T) / 2

                    # Scale covariance with improved numerical stability
                    scaled_cov = (n + lambda_param) * covariance

                    # Try Cholesky first, fall back to modified sqrtm if needed
                    try:
                        L = np.linalg.cholesky(scaled_cov)  # noqa: N806
                    except np.linalg.LinAlgError:
                        L = sqrtm(scaled_cov)  # noqa: N806

                    sigma_0 = state_vector
                    sigma_n = sigma_0[:, np.newaxis] + L
                    sigma_2n = sigma_0[:, np.newaxis] - L

                    all_sigma_points = np.vstack([sigma_0, sigma_n.T, sigma_2n.T])

                    sigma_points_dict[float(jd)] = {  # Ensure jd is a float
                        "sigma_points": all_sigma_points,
                        "weights": weights,
                        "epoch": point.timestamp,
                        "state_vector": state_vector,
                        "covariance": covariance,
                    }

                except Exception as e:
                    print(
                        f"Warning: Failed to process timestamp "
                        f"{point.timestamp}: {str(e)}"
                    )
                    continue

            if not sigma_points_dict:
                raise ValueError("No sigma points could be generated successfully")

            return sigma_points_dict

        except Exception as e:
            raise ValueError(f"Failed to generate sigma points: {str(e)}") from e

    def _create_chunked_krogh_interpolator(
        self, x: np.ndarray, y: np.ndarray, chunk_size: int = 14, overlap: int = 8
    ) -> list:
        """
        Create a series of overlapping Krogh interpolators to handle large datasets
        with improved stability.

        This method splits the input data into overlapping chunks and creates a Krogh
        interpolator for each chunk. This approach helps avoid numerical instability
        that can occur when interpolating over many points using a single interpolator.

        The method uses a sliding window approach with overlap to ensure smooth
        transitions between chunks. For each chunk:
        - First chunk: Valid from start to just before end
        - Middle chunks: Valid in middle portion, leaving overlap areas for
        adjacent chunks
        - Last chunk: Valid from just after start to end

        Args:
            x (np.ndarray): Independent variable values (e.g., times)
            y (np.ndarray): Dependent variable values to interpolate
            chunk_size (int, optional): Number of points to use in each interpolation
            chunk. Defaults to 14.
            overlap (int, optional): Number of points to overlap between chunks.
                Defaults to 8.

        Returns:
            list: List of dictionaries, each containing:
                - interpolator (KroghInterpolator): The interpolator for this chunk
                - range (tuple): Valid range for this interpolator (lower, upper)

        Note:
            - If input data length is less than chunk_size, returns a single
            interpolator
            - Overlap should be less than chunk_size to ensure progress
            - The valid ranges are slightly narrower than the actual chunks to ensure
              smooth transitions between interpolators
        """
        if len(x) <= chunk_size:
            interp = KroghInterpolator(x, y)
            return [{"interpolator": interp, "range": (x[0], x[-1])}]

        # Split data into overlapping chunks
        interpolators = []
        i = 0
        while i < len(x):
            end_idx = min(i + chunk_size, len(x))
            chunk_x = x[i:end_idx]
            chunk_y = y[i:end_idx]

            # Create interpolator for this chunk
            interp = KroghInterpolator(chunk_x, chunk_y)

            # Record the valid range for this chunk (slightly narrower than the
            # actual chunk) to ensure smooth transitions between chunks
            if i == 0:
                # First chunk - use from beginning to just before end
                valid_range = (
                    chunk_x[0],
                    chunk_x[-2] if len(chunk_x) > 2 else chunk_x[-1],
                )
            elif end_idx == len(x):
                # Last chunk - use from just after start to end
                valid_range = (
                    chunk_x[1] if len(chunk_x) > 1 else chunk_x[0],
                    chunk_x[-1],
                )
            else:
                # Middle chunks - use middle portion, leaving overlap areas
                # for adjacent chunks
                valid_range = (
                    chunk_x[1] if len(chunk_x) > 1 else chunk_x[0],
                    chunk_x[-2] if len(chunk_x) > 2 else chunk_x[-1],
                )

            interpolators.append({"interpolator": interp, "range": valid_range})

            # Move to next chunk with overlap, ensuring we make progress
            i = max(end_idx - overlap, i + 1)

        return interpolators

    def _interpolate_sigma_pointsKI(  # noqa: N802
        self, sigma_points_dict: dict
    ) -> dict:
        """
        Create high-precision interpolation splines for sigma point trajectories using
        chunked Krogh interpolation.

        This method processes the sigma points dictionary to create interpolators for
        each component of the position and velocity vectors. It handles 13 sigma
        points (1 mean + 6 positive + 6 negative Cholesky points) and creates separate
        interpolators for each component (x, y, z) of both position and velocity.

        The method uses chunked Krogh interpolation to maintain numerical stability when
        dealing with long time series. Each component is interpolated independently, and
        invalid or non-finite values are handled gracefully.

        Args:
            sigma_points_dict (dict): Dictionary mapping Julian dates to sigma point
                information:
                - sigma_points (np.ndarray): Array of 13 sigma points (6D state vectors)
                - weights (dict): Dictionary containing mean and covariance weights
                - epoch (datetime): Timestamp for these sigma points
                - state_vector (np.ndarray): Original state vector
                - covariance (np.ndarray): Original covariance matrix

        Returns:
            dict: Dictionary containing interpolation splines and time range:
                - positions (list): List of lists of position interpolators:
                    - Outer list: One entry per sigma point (13 total)
                    - Inner list: One entry per component (x, y, z)
                    - Each entry: List of chunked Krogh interpolators
                - velocities (list): List of lists of velocity interpolators:
                    - Outer list: One entry per sigma point (13 total)
                    - Inner list: One entry per component (x, y, z)
                    - Each entry: List of chunked Krogh interpolators
                - time_range (tuple): (start_time, end_time) in Julian dates

        Note:
            - Each component (x, y, z) of position and velocity has its own set of
              interpolators
            - Interpolators are created only for valid (finite) data points
            - The chunking parameters (chunk_size=14, overlap=8) are optimized
            for stability
            - None is returned for components with no valid data points
        """
        julian_dates = np.array(sorted(sigma_points_dict.keys()), dtype=np.float64)
        n_sigma_points = 13

        positions_by_point: list[list[np.ndarray]] = [[] for _ in range(n_sigma_points)]
        velocities_by_point: list[list[np.ndarray]] = [
            [] for _ in range(n_sigma_points)
        ]

        for jd in julian_dates:
            sigma_points = sigma_points_dict[jd]["sigma_points"].astype(np.float64)
            for i in range(n_sigma_points):
                positions_by_point[i].append(sigma_points[i][:3])
                velocities_by_point[i].append(sigma_points[i][3:])

        # Convert lists to numpy arrays
        positions_array: list[np.ndarray] = [
            np.array(pos, dtype=np.float64) for pos in positions_by_point
        ]
        velocities_array: list[np.ndarray] = [
            np.array(vel, dtype=np.float64) for vel in velocities_by_point
        ]

        position_splines = []
        velocity_splines = []

        for i in range(n_sigma_points):
            # Position splines
            pos_splines_i: list[list[dict[str, Any]] | None] = []
            for j in range(3):
                pos_data = positions_array[i][:, j]
                valid_mask = np.isfinite(pos_data)
                if np.any(valid_mask):
                    # Use not-a-knot cubic splines for better accuracy
                    spline = self._create_chunked_krogh_interpolator(
                        julian_dates[valid_mask],
                        pos_data[valid_mask],
                        chunk_size=14,
                        overlap=8,
                    )
                    pos_splines_i.append(spline)
                else:
                    pos_splines_i.append(None)
            position_splines.append(pos_splines_i)

            vel_splines_i: list[list[dict[str, Any]] | None] = []
            for j in range(3):
                vel_data = velocities_array[i][:, j]
                valid_mask = np.isfinite(vel_data)
                if np.any(valid_mask):
                    spline = self._create_chunked_krogh_interpolator(
                        julian_dates[valid_mask],
                        vel_data[valid_mask],
                        chunk_size=14,
                        overlap=8,
                    )
                    vel_splines_i.append(spline)
                else:
                    vel_splines_i.append(None)
            velocity_splines.append(vel_splines_i)

        return {
            "positions": position_splines,
            "velocities": velocity_splines,
            "time_range": (julian_dates[0], julian_dates[-1]),
        }

    def _get_interpolated_sigma_points_KI(  # noqa: N802
        self, interpolated_splines: dict, julian_date: float
    ) -> np.ndarray:
        """
        Get interpolated sigma points at a specific Julian date using optimal
        chunk selection.

        This method interpolates the position and velocity components of all
        13 sigma points at the requested Julian date. It uses a sophisticated
        chunk selection algorithm that prefers interpolators where the requested
        time is in the middle of their valid range, rather than at the edges,
        to minimize interpolation errors.

        The method handles both position and velocity components (x, y, z) for each
        sigma point, selecting the most appropriate interpolator chunk for each
        component based on the requested time's position within the chunk's valid range.

        Args:
            interpolated_splines (dict): Dictionary containing interpolation splines:
                - positions (list): List of lists of position interpolators
                - velocities (list): List of lists of velocity interpolators
                - time_range (tuple): (start_time, end_time) in Julian dates
            julian_date (float): The Julian date at which to interpolate the sigma
            points

        Returns:
            np.ndarray: Array of shape (13, 6) containing the interpolated sigma points:
                - First 13 rows: One row per sigma point
                - 6 columns: [x, y, z, vx, vy, vz] for each point
                - dtype: np.float64 for high precision

        Raises:
            ValueError: If the requested Julian date is outside the interpolation range

        Note:
            - The method uses a centrality score to select the best interpolator chunk
            - For times outside any chunk's range, the nearest chunk is used
            - All calculations are performed in double precision (np.float64)
            - The method assumes the input splines are valid and properly structured
        """
        start_time, end_time = interpolated_splines["time_range"]
        if not (start_time <= julian_date <= end_time):
            raise ValueError(
                f"Requested time {julian_date} is outside the interpolation range "
                f"[{start_time}, {end_time}]"
            )

        n_sigma_points = 13
        interpolated_points = np.zeros((n_sigma_points, 6), dtype=np.float64)

        for i in range(n_sigma_points):
            # Interpolate positions
            for j in range(3):
                if interpolated_splines["positions"][i][j] is not None:
                    splines = interpolated_splines["positions"][i][j]
                    applicable_splines = []
                    for idx, spline_info in enumerate(splines):
                        lower, upper = spline_info["range"]
                        if lower <= julian_date <= upper:
                            # Calculate how central the point is within this
                            # spline's range (0.5 means it's in the middle, 0
                            # or 1 means it's at an edge)
                            centrality = (julian_date - lower) / (upper - lower)

                            # Prefer points that are more central (closer to 0.5)
                            # Converts to 0-1 scale where 1 is most central
                            score = 1 - abs(centrality - 0.5) * 2
                            applicable_splines.append((idx, score, spline_info))

                    # If we found applicable splines, use the most central one
                    if applicable_splines:
                        applicable_splines.sort(key=lambda x: x[1], reverse=True)
                        best_spline = applicable_splines[0][2]
                        interpolated_points[i, j] = best_spline["interpolator"](
                            julian_date
                        )
                    else:
                        # If no spline's range contains this point, use the closest one
                        if julian_date < start_time:
                            interpolated_points[i, j] = splines[0]["interpolator"](
                                julian_date
                            )
                        else:
                            interpolated_points[i, j] = splines[-1]["interpolator"](
                                julian_date
                            )

            # Interpolate velocities
            for j in range(3):
                if interpolated_splines["velocities"][i][j] is not None:
                    splines = interpolated_splines["velocities"][i][j]
                    applicable_splines = []

                    for idx, spline_info in enumerate(splines):
                        lower, upper = spline_info["range"]
                        if lower <= julian_date <= upper:
                            centrality = (julian_date - lower) / (upper - lower)
                            # Prefer points that are more central
                            score = 1 - abs(centrality - 0.5) * 2
                            applicable_splines.append((idx, score, spline_info))

                    # If we found applicable splines, use the most central one
                    if applicable_splines:
                        applicable_splines.sort(key=lambda x: x[1], reverse=True)
                        best_spline = applicable_splines[0][2]
                        interpolated_points[i, j + 3] = best_spline["interpolator"](
                            julian_date
                        )
                    else:
                        # If no spline's range contains this point, use the closest one
                        if julian_date < start_time:
                            interpolated_points[i, j + 3] = splines[0]["interpolator"](
                                julian_date
                            )
                        else:
                            interpolated_points[i, j + 3] = splines[-1]["interpolator"](
                                julian_date
                            )

        return interpolated_points

    def _reconstruct_covariance_at_time(self, interpolated_points: np.ndarray) -> tuple:
        """
        Reconstruct the mean state and covariance matrix from interpolated
        sigma points using the Unscented Transform.

        This method implements the Unscented Transform to reconstruct the mean state
        and covariance matrix from a set of interpolated sigma points. It uses
        optimized parameters for numerical stability and accuracy in the presence
        of non-linear transformations.

        The method uses the following Unscented Transform parameters:
        - alpha = 0.001: Reduced for better numerical stability
        - beta = 2.0: Optimal for Gaussian distributions
        - kappa = 3-n: Modified for better stability
        - lambda = alpha²(n+kappa) - n: Scaling parameter

        Args:
            interpolated_points (np.ndarray): Array of shape (13, 6) containing
            the interpolated sigma points, where:
                - 13 rows: One row per sigma point (1 mean + 6 positive + 6
                negative Cholesky points)
                - 6 columns: [x, y, z, vx, vy, vz] state components
                - dtype: np.float64 for high precision

        Returns:
            tuple: (mean_state, covariance) where:
                - mean_state (np.ndarray): Array of shape (6,) containing the
                mean state vector
                - covariance (np.ndarray): Array of shape (6, 6) containing the
                symmetric covariance matrix

        Note:
            - The mean state is taken directly from the first sigma point for stability
            - The covariance matrix is computed using weighted outer products
            - The final covariance matrix is symmetrized to ensure numerical stability
            - All calculations are performed in double precision (np.float64)
        """
        # Optimized Unscented Transform parameters
        n = 6
        alpha = np.float64(0.001)  # Reduced alpha for better numerical stability
        beta = np.float64(2.0)  # Optimal for Gaussian
        kappa = np.float64(3 - n)  # Modified for better stability
        lambda_param = alpha * alpha * (n + kappa) - n

        w0_m = lambda_param / (n + lambda_param)
        wn_m = np.float64(0.5) / (n + lambda_param)
        w0_c = w0_m + (1 - alpha * alpha + beta)
        wn_c = wn_m

        mean_state = interpolated_points[0].copy()  # Copy to ensure it's a new array

        # Calculate covariance with improved numerical stability
        diff_0 = interpolated_points[0] - mean_state
        covariance = w0_c * np.outer(diff_0, diff_0)

        for i in range(1, len(interpolated_points)):
            diff = interpolated_points[i] - mean_state
            covariance += wn_c * np.outer(diff, diff)

        covariance = (covariance + covariance.T) / 2

        return mean_state, covariance


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
