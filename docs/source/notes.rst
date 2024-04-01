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


Satellite IDs
-----------------------------------------------------------
Satellites are assigned a temporary ID after launch, which can be used
to identify them until they are assigned a permanent catalog number by
Space Force. SpaceTrack and CelesTrak use different temporary numbering systems - SatChecker
uses the ones from CelesTrak. Satellites can be found by searching by
any of their IDs, including the temporary ones, but only the most recent ID
will be displayed in the results.

Other Notes
-----------------------------------------------------------
* Results are limited to 1000 points per request.

* Orbital predictions can be slightly less accurate right after satellite launch (and before they reach their final orbit), so those positions may be off by a bit temporarily.
