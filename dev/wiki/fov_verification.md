# FOV Verification

## Notes
This uses position data obtained from SCORE to verify/compare the position data obtained from the FOV API.
For Pelican 3001, other satellites found in the FOV query are also plotted, but not for ACS 3 since with the longer duration and field of view, there were too many satellites to plot.

The track separation is currently the difference is between points on the observed/predicted tracks. The points on the track for the observed data have been interpolated to match the cadence of the predicted data for easier comparison.

### Pelican 3001 - 8 degree FOV
<img src="../docs/source/images/pelican_05_08_8deg.png" alt="Pelican 3001 - 05-08-2024" width="100%"/>

<img src="../docs/source/images/pelican_05_20_8deg.png" alt="Pelican 3001 - 05-20-2024" width="100%"/>

<img src="../docs/source/images/pelican_06_05_8deg.png" alt="Pelican 3001 - 06-05-2024" width="100%"/>

----

### Pelican 3001 - 2 degree FOV
<img src="../docs/source/images/pelican_05_08_24.png" alt="Pelican 3001 - 05-08-2024 - 2 degree FOV" width="100%"/>

<img src="../docs/source/images/pelican_05_20_24.png" alt="Pelican 3001 - 05-20-2024 - 2 degree FOV" width="100%"/>

<img src="../docs/source/images/pelican_06_05_24.png" alt="Pelican 3001 - 06-05-2024 - 2 degree FOV" width="100%"/>

----

### ACS 3 - 30 degree FOV
<img src="../docs/source/images/acs3_30deg.png" alt="ACS 3 - 10-04-2024" width="100%"/>

### ACS 3 - 2 degree FOV
<img src="../docs/source/images/acs3_10_04_24.png" alt="ACS 3 - 10-04-2024" width="100%"/>
