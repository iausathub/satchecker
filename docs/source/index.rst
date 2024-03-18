.. SatChecker documentation master file, created by
   sphinx-quickstart on Sat Sep  2 12:16:11 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SatChecker Ephemeris API Documentation
======================================

SatChecker is a satellite position prediction tool from the IAU CPS (IAU Centre for
the Protection of the Dark and Quiet Sky from Satellite Constellation Interference)
SatHub group. It uses TLEs (two-line element sets) from CelesTrak and Space-Track
to provide predictions of satellite positions at a given time and location.
It also provides additional information like range, on-sky velocity, and an
"illuminated" flag for each prediction point.


.. toctree::
   :caption: Ephemeris API
   :maxdepth: 3
   :hidden:

   api
   errors
   notes

.. toctree::
   :caption: Examples
   :maxdepth: 3
   :hidden:

   examples
   notebooks/demo.ipynb

.. toctree::
   :caption: Development
   :maxdepth: 2
   :hidden:

   release
   acknowledgements
