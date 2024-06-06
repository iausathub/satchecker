URL Examples
=============

Here are a few examples of how to use the API:


**Get all visible passes of STARLINK-1600 at a given location for the specified time range:**
https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460010.1&stepjd=0.5

**Get any passes (visible or not) of STARLINK-1600 at a given location for the specified time range:**
https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90

**Attempt to get visible passes STARLINK-1600 at a given location for the specified time range, with no results:**
https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1
