from collections import namedtuple

import numpy as np
from astropy import units as u
from astropy.coordinates import EarthLocation
from astropy.time import Time, TimeDelta
from sgp4.api import Satrec
from skyfield.api import EarthSatellite, load, wgs84
from skyfield.nutationlib import iau2000b

from api.utils.coordinate_systems import (
    az_el_to_ra_dec,
    calculate_current_position,
    ecef_to_enu,
    ecef_to_itrs,
    enu_to_az_el,
    get_phase_angle,
    icrf2radec,
    is_illuminated,
    itrs_to_gcrs,
    teme_to_ecef,
)
from api.utils.time_utils import jd_to_gst

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
        "illuminated",
        "satellite_gcrs",
        "observer_gcrs",
        "julian_date",
    ],
)


class SkyfieldPropagationStrategy:
    def propagate(
        self,
        julian_date: float,
        tle_line_1: str,
        tle_line_2: str,
        latitude: float,
        longitude: float,
        elevation: float,
    ) -> satellite_position:
        """
        Use Skyfield (https://rhodesmill.org/skyfield/earth-satellites.html)
        to propagate satellite and observer states.

        Args:
            tle_line_1 (str): TLE line 1
            tle_line_2 (str): TLE line 2
            latitude (float): The observer WGS84 latitude in degrees
            longitude (float): The observers WGS84 longitude in degrees (positive value
                represents east, negative value represents west)
            elevation (float): The observer elevation above WGS84 ellipsoid in meters
            julian_date (float): UT1 Universal Time Julian Date. An input of 0 will use
                the TLE epoch.

        Returns:
            satellite_position: A named tuple containing the satellite position results

        """

        # This is the skyfield implementation
        ts = load.timescale()
        satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)

        # Get current position and find topocentric ra and dec
        curr_pos = wgs84.latlon(latitude, longitude, elevation)
        # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
        # Use ts.ut1_jd instead of ts.from_astropy because from_astropy uses
        # astropy.Time.TT.jd instead of UT1
        jd = Time(julian_date, format="jd", scale="ut1")

        if jd.jd == 0:
            t = ts.ut1_jd(satellite.model.jdsatepoch)
        else:
            t = ts.ut1_jd(jd.jd)

        difference = satellite - curr_pos
        topocentric = difference.at(t)
        topocentricn = topocentric.position.km / np.linalg.norm(topocentric.position.km)

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

        # drav, ddecv = icrf2radec(vsattop / sattopr, unit_vector=True)
        # dracosdecv = drav * np.cos(dec.radians)

        phase_angle = get_phase_angle(topocentricn, sat_gcrs, julian_date)

        illuminated = is_illuminated(sat_gcrs, julian_date)

        obs_gcrs = curr_pos.at(t).position.km

        return satellite_position(
            ra._degrees,
            dec.degrees,
            dracosdec,
            ddec,
            alt._degrees,
            az._degrees,
            distance.km,
            ddistance,
            phase_angle,
            illuminated,
            sat_gcrs.tolist(),
            obs_gcrs.tolist(),
            julian_date,
        )


class SGP4PropagationStrategy:
    def propagate(
        self, julian_date, tle_line_1, tle_line_2, latitude, longitude, elevation
    ) -> satellite_position:  # pragma: no cover
        """
        Propagates satellite and observer states using the SGP4 propagation model.

        Args:
            julian_date (float): The Julian Date at which to propagate the satellite.
            tle_line_1 (str): The first line of the Two-Line Element set representing
                the satellite.
            tle_line_2 (str): The second line of the Two-Line Element set representing
                the satellite.
            latitude (float): The latitude of the observer's location, in degrees.
            longitude (float): The longitude of the observer's location, in degrees.
            elevation (float): The height of the observer's location, in meters above
                the WGS84 ellipsoid.

        Returns:
            satellite_position: A named tuple containing the satellite position results
        """

        # TODO:  SCK-62: pull out the observer location to a level above this so it
        # doesn't get recalculated every time
        observer_location = EarthLocation(
            lat=latitude * u.deg, lon=longitude * u.deg, height=elevation * u.m
        )
        location_itrs = observer_location.itrs.cartesian.xyz.value / 1000

        # Compute the coordinates of the CIP (Celestial Intermediate Pole)
        dpsi, deps = iau2000b(julian_date)

        # Compute the nutation in longitude
        nutation_arcsec = dpsi / 10000000  # Convert from arcseconds to degrees
        nutation = nutation_arcsec / 3600

        location_itrs = np.array(location_itrs)
        theta_gst = jd_to_gst(julian_date, nutation)
        obs_gcrs = observer_location.get_gcrs(obstime=Time(julian_date, format="jd"))

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

        return satellite_position(
            ra,
            dec,
            dracosdec,
            ddec,
            alt,
            az,
            distance,
            ddistance,
            phase_angle,
            illuminated,
            sat_gcrs.tolist() if sat_gcrs is not None else None,
            obs_gcrs.tolist() if obs_gcrs is not None else None,
            julian_date,
        )


class TestPropagationStrategy:
    def propagate(
        self, julian_date, tle_line_1, tle_line_2, latitude, longitude, elevation
    ) -> satellite_position:  # pragma: no cover
        """
        Propagates satellite and observer states using a test method

        Args:
            julian_date (float): The Julian Date at which to propagate the satellite.

            tle_line_1 (str): The first line of the Two-Line Element set representing
                the satellite.

            tle_line_2 (str): The second line of the Two-Line Element set representing
                the satellite.

            latitude (float): The latitude of the observer's location, in degrees.

            longitude (float): The longitude of the observer's location, in degrees.

            elevation (float): The height of the observer's location, in meters above
                the WGS84 ellipsoid.

        Returns:
            satellite_position: A namedtuple containing the satellite position results
        """

        # This is the skyfield implementation
        ts = load.timescale()
        eph = load("de430t.bsp")
        earth = eph["Earth"]
        sun = eph["Sun"]
        satellite = EarthSatellite(tle_line_1, tle_line_2, ts=ts)
        # Get current position and find topocentric ra and dec
        curr_pos = calculate_current_position(latitude, longitude, elevation)
        # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
        # Use ts.ut1_jd instead of ts.from_astropy because from_astropy uses
        # astropy.Time.TT.jd instead of UT1
        jd = Time(julian_date, format="jd", scale="ut1")
        if jd.jd == 0:
            t = ts.ut1_jd(satellite.model.jdsatepoch)
        else:
            t = ts.ut1_jd(jd.jd)

        difference = satellite - curr_pos
        topocentric = difference.at(t)
        topocentricn = topocentric.position.km / np.linalg.norm(topocentric.position.km)

        ra, dec, distance = topocentric.radec()
        alt, az, distance = topocentric.altaz()

        dtday = TimeDelta(1, format="sec")
        tplusdt = ts.ut1_jd((jd + dtday).jd)
        tminusdt = ts.ut1_jd((jd - dtday).jd)

        # haven't had the need to change this but leaving it here for clarity purposes
        dtsec = 1
        dtx2 = 2 * dtsec

        sat = satellite.at(t).position.km

        # satn = sat / np.linalg.norm(sat)
        # satpdt = satellite.at(tplusdt).position.km
        # satmdt = satellite.at(tminusdt).position.km
        # vsat = (satpdt - satmdt) / dtx2

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

        # drav, ddecv = icrf2radec(vsattop / sattopr, unit_vector=True)
        # dracosdecv = drav * np.cos(dec.radians)

        earthp = earth.at(t).position.km
        sunp = sun.at(t).position.km
        # earthp, sunp = calculate_earth_sun(t)
        earthsun = sunp - earthp
        earthsunn = earthsun / np.linalg.norm(earthsun)
        satsun = sat - earthsun
        satsunn = satsun / np.linalg.norm(satsun)
        phase_angle = np.rad2deg(np.arccos(np.dot(satsunn, topocentricn)))

        illuminated = is_illuminated(sat, earthsunn)

        return satellite_position(
            ra._degrees,
            dec.degrees,
            dracosdec,
            ddec,
            alt.degrees,
            az.degrees,
            distance.km,
            ddistance,
            phase_angle,
            illuminated,
            jd.jd,
        )


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
