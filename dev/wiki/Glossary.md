- [Coordinate Systems](#coordinate-systems)
    * [TEME](#teme)
    * [GRCS](#gcrs)
    * [ECEF](#ecef)
    * [ECI](#eci)
    * [ENU](#enu)
- [TLE](#tle)

<a name="coordinate-systems"></a>
# Coordinate Systems

<a name="teme"></a>
## TEME
**True Equator, Mean Equinox:** This is a reference frame used for describing positions in space, especially for objects like satellites tracked by NORAD using two-line element sets. It's worth noting that although it's termed "True Equator, Mean Equinox," it doesn't strictly adhere to the traditional definition of mean equinox. Instead, it employs a variation of this concept. In TEME, the Earth-Centered Inertial (ECI) frame is utilized, providing a consistent and standardized way to pinpoint locations relative to the Earth. So, while it shares similarities with the conventional mean equinox concept, it operates with a slight distinction tailored to the specific needs of satellite tracking and orbital calculations.

<a name="gcrs"></a>
## GRCS
**Geocentric Celestial Coordinate System:** GRCS provides a standardized way to describe where things are in the sky, regardless of where on Earth you might be observing from. It's particularly useful for accurately tracking the positions of stars, planets, satellites, and other celestial bodies. Positions are measured from the center of the Earth - this means that the Earth's center serves as the origin (0,0,0) of the coordinate system. GRCS positions objects relative to the celestial sphere, an imaginary sphere surrounding the Earth onto which stars and other celestial objects appear to be fixed.

<a name="ecef"></a>
## ECEF
**Earth-centered, Earth-fixed:** The Earth-Centered, Earth-Fixed (ECEF) coordinate system is a reference frame commonly used in navigation, geodesy, and satellite tracking. This coordinate system is centered on the Earth, and the origin (0,0,0) of the coordinate system is located at the center of the Earth's mass. This coordinate system is stationary with respect to the Earth's surface. As the Earth rotates on its axis and orbits the Sun, the ECEF frame remains fixed relative to the Earth itself. This is in contrast to other coordinate systems that may rotate with the Earth or with the stars.

It differs from GCRS in the following ways:
* Frame of Reference:
  * ECEF is referenced to the Earth's surface, with its origin fixed at the center of the Earth and its axes aligned with the Earth's rotation.
  * GCRS, on the other hand, is referenced to the celestial sphere and is fixed with respect to distant extragalactic objects. Its origin is near the solar system barycenter, and its axes are fixed relative to the distant stars.
* Use Cases:
  * ECEF is primarily used for practical applications on or near the Earth's surface, such as GPS navigation, surveying, and satellite tracking.
  * GCRS is primarily used in astronomy and astrodynamics for precisely describing the positions and motions of celestial bodies.

<a name="eci"></a>
## ECI
**Earth-centered inertial:** Earth-Centered Inertial (ECI) coordinate system is a reference frame used in aerospace engineering, astronomy, and satellite navigation. ECI is centered on the Earth. Its origin (0,0,0) is located at the center of the Earth's mass. The "inertial" aspect means that the coordinate system is non-rotating and remains fixed with respect to the stars.

ECI provides a stable and consistent reference frame for describing the positions and motions of objects in space relative to the Earth. It's particularly useful for applications like satellite tracking, spacecraft navigation, and astrodynamics, where precise positioning and velocity information are required. ECI is often used alongside other coordinate systems, such as ECEF (Earth-Centered, Earth-Fixed), which is referenced to the Earth's surface.

<a name="enu"></a>
## ENU
East-North-Up: The East-North-Up (ENU) coordinate system is a local, Cartesian coordinate system. It works like this:
* East: The East direction corresponds to the direction of increasing longitude. In the ENU coordinate system, the positive X-axis points towards the East, meaning that increasing X-values represent movement to the East.
* North: The North direction corresponds to the direction of increasing latitude. In the ENU coordinate system, the positive Y-axis points towards the North, meaning that increasing Y-values represent movement to the North.
* Up: The Up direction represents elevation or altitude. In the ENU coordinate system, the positive Z-axis points upwards, perpendicular to the Earth's surface. Increasing Z-values represent movement upwards.

The ENU coordinate system provides a convenient way to describe positions and movements relative to a local reference point, and can be used to easily calculate altitude and azimuth of an object.


<a name="tle"></a>
# TLE
<meta charset="utf-8"><b style="font-weight:normal;" id="docs-internal-guid-23f7b61e-7fff-2c2c-1862-817b7312a069"><p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">A Two-Line Element (TLE) is a specific data format used to describe the orbits of Earth-orbiting objects, such as satellites and space debris. A TLE consists of two lines of text. Each line contains a series of numerical values and characters that encode important orbital parameters. TLEs are valid for a maximum of two weeks on either side of the epoch date of the data; the farther you get from that date the less accurate they are. TLEs for recently launched satellites are not as accurate as those in established orbits.</span></p><br /><p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">Example:</span></p><br /><p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">STARLINK-31635&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p><p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">1 59511U 24073A &nbsp; 24136.39154557 -.00000043&nbsp; 00000+0&nbsp; 62293-5 0&nbsp; 9996</span></p><p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">2 59511&nbsp; 43.0022 139.3897 0001210 217.6522 142.4250 15.40719716&nbsp; 5546</span></p><br /><p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">SatChecker doesn&rsquo;t currently need to manually process TLEs - this is handled in Skyfield&rsquo;s EarthSatellite object initialization. However, here is an overview of how this format is structured (adapted for this example from </span><a href="https://en.wikipedia.org/wiki/Two-line_element_set" style="text-decoration:none;"><span style="font-size:11pt;font-family:Arial,sans-serif;color:#1155cc;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;-webkit-text-decoration-skip:none;text-decoration-skip-ink:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">https://en.wikipedia.org/wiki/Two-line_element_set</span></a><span style="font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">):</span></p><br /><p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">Line 1</span></p><div dir="ltr" style="margin-left:0pt;" align="left">
Field | Columns | Content | Example
-- | -- | -- | --
1 | 01 | Line number | 1
2 | 03–07 | Satellite catalog number | 59511
3 | 08 | Classification (U: unclassified, C: classified, S: secret) [12] | U
4 | 10–11 | International Designator (last two digits of launch year) | 24
5 | 12–14 | International Designator (launch number of the year) | 073
6 | 15–17 | International Designator (piece of the launch) | A
7 | 19–20 | Epoch year (last two digits of year) | 24
8 | 21–32 | Epoch (day of the year and fractional portion of the day) | 136.39154557
9 | 34–43 | First derivative of mean motion; the ballistic coefficient [13] | -.00000043
10 | 45–52 | Second derivative of mean motion (decimal point assumed) [13] | 00000+0
11 | 54–61 | B*, the drag term, or radiation pressure coefficient (decimal point assumed) [13] | 62293-5
12 | 63–63 | Ephemeris type (always zero; only used in undistributed TLE data) [14] | 0
13 | 65–68 | Element set number. Incremented when a new TLE is generated for this object.[13] | 999
14 | 69 | Checksum (modulo 10) | 6

</div>

<meta charset="utf-8"><b style="font-weight:normal;" id="docs-internal-guid-24e903a8-7fff-7526-b4ad-5a71ea8f0b7d"><br /><br /><p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">Line 2</span></p><div dir="ltr" style="margin-left:0pt;" align="left">
Field | Columns | Content | Example
-- | -- | -- | --
1 | 01 | Line number | 2
2 | 03–07 | Satellite Catalog number | 59511
3 | 09–16 | Inclination (degrees) | 43.0022
4 | 18–25 | Right ascension of the ascending node (degrees) | 139.3897
5 | 27–33 | Eccentricity (decimal point assumed) | 0001210
6 | 35–42 | Argument of perigee (degrees) | 217.6522
7 | 44–51 | Mean anomaly (degrees) | 142.4250
8 | 53–63 | Mean motion (revolutions per day) | 15.40719716
9 | 64–68 | Revolution number at epoch (revolutions) | 554
10 | 69 | Checksum (modulo 10) | 6

</div>
