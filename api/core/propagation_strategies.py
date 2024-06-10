from collections import namedtuple

import numpy as np
from astropy import units as u
from astropy.coordinates import (
    EarthLocation,
)
from astropy.time import Time, TimeDelta
from sgp4.api import Satrec
from skyfield.api import EarthSatellite, load, wgs84
from skyfield.nutationlib import iau2000b
from utils.coordinate_systems import (
    az_el_to_ra_dec,
    ecef_to_enu,
    enu_to_az_el,
    teme_to_ecef,
)
from utils.time_utils import jd_to_gst

from core.utils import calculate_current_position, icrf2radec


class SkyfieldPropagationStrategy:
    def propagate(
        self, julian_date, tle_line_1, tle_line_2, latitude, longitude, elevation
    ):
        """Use Skyfield (https://rhodesmill.org/skyfield/earth-satellites.html)
        to propagate satellite and observer states.

        Parameters
        ----------
        tle_line_1: 'str'
            TLE line 1
        tle_line_2: 'str'
            TLE line 2
        lat: 'float'
            The observer WGS84 latitude in degrees
        lon: 'float'
            The observers WGS84 longitude in degrees (positive value represents east,
            negative value represents west)
        elevation: 'float'
            The observer elevation above WGS84 ellipsoid in meters
        julian_date: 'float'
            UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
        tleapi: 'str'
            base API for query

        Returns
        -------
        Right Ascension: 'float'
            The right ascension of the satellite relative to observer coordinates in
            ICRS reference frame in degrees. Range of response is [0,360)
        Declination: 'float'
            The declination of the satellite relative to observer coordinates in ICRS
            reference frame in degrees. Range of response is [-90,90]
        Altitude: 'float'
            The altitude of the satellite relative to observer coordinates in ICRS
            reference frame in degrees. Range of response is [0,90]
        Azimuth: 'float'
            The azimuth of the satellite relative to observer coordinates in ICRS
            reference frame in degrees. Range of response is [0,360)
        distance: 'float'
            Range from observer to object in km
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

        eph = load("de430t.bsp")
        earth = eph["Earth"]
        sun = eph["Sun"]

        earthp = earth.at(t).position.km
        sunp = sun.at(t).position.km
        earthsun = sunp - earthp
        earthsunn = earthsun / np.linalg.norm(earthsun)
        satsun = sat_gcrs - earthsun
        satsunn = satsun / np.linalg.norm(satsun)
        phase_angle = np.rad2deg(np.arccos(np.dot(satsunn, topocentricn)))

        # Is the satellite in Earth's Shadow?
        r_parallel = np.dot(sat_gcrs, earthsunn) * earthsunn
        r_tangential = sat_gcrs - r_parallel

        illuminated = True

        obs_gcrs = curr_pos.at(t).position.km

        if np.linalg.norm(r_parallel) < 0:
            # rearthkm
            if np.linalg.norm(r_tangential) < 6370:
                # print(np.linalg.norm(r_tangential),np.linalg.norm(r))
                # yes the satellite is in Earth's shadow, no need to continue
                # (except for the moon of course)
                illuminated = False
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
            sat_gcrs.tolist(),
            obs_gcrs.tolist(),
            julian_date,
        )


class SGP4PropagationStrategy:
    def propagate(
        self, julian_date, tle_line_1, tle_line_2, latitude, longitude, elevation
    ):
        # new function
        # TODO:  SCK-62: pull out the observer location to a level above this so it
        # doesn't get recalculated every time
        observer_location = EarthLocation(
            lat=latitude * u.deg, lon=longitude * u.deg, height=elevation * u.m
        )
        location_itrs = observer_location.itrs.cartesian.xyz.value / 1000

        # Compute the x, y coordinates of the CIP (Celestial Intermediate Pole)
        dpsi, deps = iau2000b(julian_date)

        # Compute the nutation in longitude
        nutation_arcsec = dpsi / 10000000  # Convert from arcseconds to degrees
        nutation = nutation_arcsec / 3600

        location_itrs = np.array(location_itrs)
        theta_gst = jd_to_gst(julian_date, nutation)

        satellite = Satrec.twoline2rv(tle_line_1, tle_line_2)
        error, r, v = satellite.sgp4(julian_date, 0)

        r_ecef = teme_to_ecef(r, theta_gst)
        difference = r_ecef - location_itrs
        r_enu = ecef_to_enu(difference, latitude, longitude)
        az, el = enu_to_az_el(r_enu)
        ra, dec = az_el_to_ra_dec(az, el, latitude, longitude, julian_date)

        return az, el, ra, dec


class TestPropagationStrategy:
    def propagate(
        self, julian_date, tle_line_1, tle_line_2, latitude, longitude, elevation
    ):
        """Use Skyfield (https://rhodesmill.org/skyfield/earth-satellites.html)
        to propagate satellite and observer states.

        Parameters
        ----------
        tle_line_1: 'str'
            TLE line 1
        tle_line_2: 'str'
            TLE line 2
        lat: 'float'
            The observer WGS84 latitude in degrees
        lon: 'float'
            The observers WGS84 longitude in degrees (positive value represents east,
            negative value represents west)
        elevation: 'float'
            The observer elevation above WGS84 ellipsoid in meters
        julian_date: 'float'
            UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
        tleapi: 'str'
            base API for query

        Returns
        -------
        Right Ascension: 'float'
            The right ascension of the satellite relative to observer coordinates in
            ICRS reference frame in degrees. Range of response is [0,360)
        Declination: 'float'
            The declination of the satellite relative to observer coordinates in ICRS
            reference frame in degrees. Range of response is [-90,90]
        Altitude: 'float'
            The altitude of the satellite relative to observer coordinates in ICRS
            reference frame in degrees. Range of response is [0,90]
        Azimuth: 'float'
            The azimuth of the satellite relative to observer coordinates in ICRS
            reference frame in degrees. Range of response is [0,360)
        distance: 'float'
            Range from observer to object in km
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

        # Is the satellite in Earth's Shadow?
        r_parallel = np.dot(sat, earthsunn) * earthsunn
        r_tangential = sat - r_parallel

        illuminated = True

        if np.linalg.norm(r_parallel) < 0:
            # rearthkm
            if np.linalg.norm(r_tangential) < 6370:
                # print(np.linalg.norm(r_tangential),np.linalg.norm(r))
                # yes the satellite is in Earth's shadow, no need to continue
                # (except for the moon of course)
                illuminated = False
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
                "jd",
            ],
        )
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
        print(self.elevation)

    def propagate(self):
        return self.propagation_strategy.propagate(
            self.julian_date,
            self.tle_line_1,
            self.tle_line_2,
            self.latitude,
            self.longitude,
            self.elevation,
        )
