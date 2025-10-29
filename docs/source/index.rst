.. SatChecker documentation master file, created by
   sphinx-quickstart on Sat Sep  2 12:16:11 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SatChecker Ephemeris API Documentation
======================================

Overview
---------
SatChecker is a satellite position prediction tool from the IAU CPS (IAU Centre for
the Protection of the Dark and Quiet Sky from Satellite Constellation Interference)
SatHub group. It uses TLEs (two-line element sets) from CelesTrak and Space-Track
to provide predictions of satellite positions at a given time and location.
It also provides additional information like range, on-sky velocity, and an
"illuminated" flag for each prediction point.

SatChecker uses the TLE with the closest epoch date available to the date specified
in the API parameters - currently available TLEs go back to July 2019. General TLE data
is updated daily, and supplemental TLEs from CelesTrak are updated every 8 hours.

The SatChecker Tools API provides additional functionality for satellite name and ID lookup,
as well as the ability to retrieve all available TLE data for a given satellite over a given
date range. Satellites can be assigned temporary IDs after launch, and names are subject to
change, so the Tools API can be used to keep track of these changes.


Support
---------
For assistance with SatChecker, please open an issue on the `GitHub repository <https://github.com/iausathub/satchecker/issues>`_,
or email questions to `sathub@cps.iau.org <mailto:sathub@cps.iau.org>`_.

.. toctree::
   :caption: General
   :maxdepth: 3
   :hidden:

   notes

.. toctree::
   :caption: Ephemeris API
   :maxdepth: 3
   :hidden:

   api
   api_response
   errors

.. toctree::
   :caption: Tools API
   :maxdepth: 3
   :hidden:

   tools_satellites
   tools_tle

.. toctree::
   :caption: FOV API
   :maxdepth: 3
   :hidden:

   fov

.. toctree::
   :caption: Examples
   :maxdepth: 3
   :hidden:

   examples
   notebooks/demo.ipynb
   notebooks/fov.ipynb
   notebooks/overhead.ipynb

.. toctree::
   :caption: Development Documentation
   :maxdepth: 2
   :hidden:

   src.api

   release
   acknowledgements
