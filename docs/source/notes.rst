Notes
=============

Coordinate System
-----------------------------------------------------------
The coordinate system used for the RA/Dec coordinate results is
the IRCF (International Reference Celestial Frame), which is almost
identical to J2000 with possible minute differences.

Validation
-----------------------------------------------------------
SatChecker has been validated with a preliminary set of observations done with
DECam/Blanco by Guillermo Damke to verify that a given set of satellites appeared
in the expected location at the expected time (Starlink Gen 2s). The results were
consistent with the expected positions.

TLE Accuracy
-----------------------------------------------------------
It's important to note that TLE accuracy varies and can impact predicted satellite
positions. Public Space-Track TLEs for LEO satellites are often off by several arcminutes, and
in occasional cases, errors can reach up to a degree, even for recent data. Accuracy tends to degrade
with time since the TLE was issued and can also be affected by conditions like space weather.
Occasionally, TLEs are systematically incorrect and later corrected.

SatChecker draws from both Space-Track and CelesTrak, the latter of which includes supplemental
TLEs from satellite operators such as SpaceX and Amazon, which can sometimes incorporate
maneuvers and updates, and increase the accuracy of the predictions.

Satellite IDs
-----------------------------------------------------------
Satellites are assigned a temporary ID after launch, which can be used
to identify them until they are assigned a permanent catalog number by
Space Force. SpaceTrack and CelesTrak use different temporary numbering systems - SatChecker
uses the ones from CelesTrak. Satellites can be found by searching by
any of their IDs, including the temporary ones, but only the most recent ID
will be displayed in the results.

TLE Dates
-----------------------------------------------------------
TLEs are only good for a maximum of two weeks as far as prediction accuracy goes, so
using a TLE closest to the date requested gives the most accurate postion information.
SatChecker will automatically select the most relevant TLE available for the requested date,
but will still be constrained by the data_source parameter. This means that by default, Space-Track
TLEs will be checked unless otherwise specified. This is relevant in two primary cases:

1. If there is a supplemental TLE available from CelesTrak that is newer than what has been retrieved from Space-Track, using CelesTrak as the data source will provide the most accurate position information.
2. Eventually, when archival TLEs are available, these will all be from Space-Track, so using CelesTrak as a data source will likely give a less timely result.

Other Notes
-----------------------------------------------------------
* Results are limited to 1000 points per request.

* Orbital predictions can be slightly less accurate right after satellite launch (and before they reach their final orbit), so those positions may be off by a bit temporarily.
