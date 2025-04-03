# SatChecker
[![Tests](https://github.com/iausathub/satchecker/actions/workflows/run_tests.yml/badge.svg)](https://github.com/iausathub/satchecker/actions/workflows/run_tests.yml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.github.com/mdadighat/6cb250448637a389052d5192a09b62d0/raw/satchecker-coverage.json)](https://github.com/iausathub/satchecker/actions/workflows/code_coverage.yml)
[![Benchmarks](https://github.com/iausathub/satchecker/actions/workflows/benchmark.yml/badge.svg)](https://github.com/iausathub/satchecker/actions/workflows/benchmark.yml)

SatChecker is a satellite tracking and prediction tool from the IAU CPS (IAU Centre for the Protection of the Dark and Quiet Sky from Satellite Constellation Interference) SatHub group. Its primary goal is to help everyone observe the night sky without interference from satellites. SatChecker uses Two-Line Element Sets (TLEs) from Space Track (and Celestrak), but it will eventually incorporate data formats from other sources to provide accurate predictions of satellite positions at a given time and location.

SatChecker can help you observe satellites to verify brightness predictions and contribute to quantifying the issue in general, but it also helps you avoid them. For planning astronomical observations, SatChecker will (in future versions) alert you to potential satellite passes that may interfere with your observations. This tool will provide detailed information about each predicted satellite pass, including range, on-sky velocity, and an "illuminated" flag to indicate when a satellite is reflecting sunlight.

Future updates will include estimates of satellite brightness, field of view interference predictions, and alerts if a predicted satellite pass will match a given position/brightness threshold.

### [API Documentation](https://satchecker.readthedocs.io/en/latest/)
Read the Docs documentation for the current version (API and code)

### [Contributing Guide](setup/CONTRIBUTING.md)
The contributing guide has links to the info to get things running locally and guidelines on making changes.

### [Wiki](https://github.com/iausathub/satchecker/wiki)
The wiki has all the info on setup, documentation, architecture and design info, and general information on the project.

<a name="license"></a>
## License
[![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
