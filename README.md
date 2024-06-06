# SatChecker
SatChecker is a satellite position prediction tool from the [IAU CPS](https://cps.iau.org/sathub/) (IAU Centre for the Protection of the Dark and Quiet Sky from Satellite Constellation Interference) SatHub group. It uses [TLEs](https://celestrak.org/NORAD/documentation/tle-fmt.php) (two-line element sets) from [CelesTrak](https://celestrak.org/), and eventually other sources, to provide predictions of satellite positions at a given time and location. It also provides additional information like range, on-sky velocity, and an "illuminated" flag for each prediction point.

#### [API Documentation](https://satchecker.readthedocs.io/en/latest/)

- [Local Installation](#installation)
    * [Dependencies](#dependencies)
    * [Setup](#setup)
    * [Local Database](#local-database)
- [Running Tests](#running-tests)
- [Building RTD Documentation](#building-rtd-documentation)
- [Tools](#tools)
- [Deployment & Infrastructure](#deployment-infrastructure)
- [Architecture](#architecture)
- [License](#license)

<a name="installation"></a>
## Local Installation

<a name="dependencies"></a>
### Dependencies
* Python 3.11.4
* Docker (for running local database if desired)
* PGAdmin (optional, for viewing postgres database)

<a name="setup"></a>
### Setup
1. Navigate to the directory where you want to install SatChecker and clone the repo:
```bash
git clone https://github.com/iausathub/satchecker.git
```
2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install the requirements:
```bash
cd api
pip install -r requirements.txt
```
5. Start the API server:
```bash
flask run
```
6. http://localhost:5000 should now redirect to the API documentation - actual API endpoints require a local test database to be set up.

<a name="local-database"></a>
### Local Database
The steps below are to set up the database to run in a Docker container for easier setup/cleanup, but you can use the `db.sql` file to set up the PostgreSQL database on your machine if you prefer.

You can populate the test database with the `retrieve_TLE.py` script in the `satchecker/data` directory. Since there isn't a pre-determined set of test data, it will differ for each machine but that shouldn't matter.

1. Set the environment variable for using the local database in ```.flaskenv```:
    ```bash
    LOCAL_DB=1
    ```
2. Install Docker Desktop for your OS: https://www.docker.com/products/docker-desktop (or PostgreSQL if you prefer to run it locally)
3. Open a terminal and navigate to the `setup/local_db` directory on your machine.
4. Run the following command to build the Docker image:
   ```bash
   docker build -t satchecker-db .
   ```
   If this is the first time you're setting this up, you'll also have to create a local volume for the database data so it doesn't get deleted when you stop the container:
   ```bash
   docker volume create satchecker_db_vol
   ```
5. Run the following command to start the container:

    ```bash
    docker run -d --name satchecker-db -v satchecker_db_vol:/var/lib/postgresql/data -p 5432:5432 satchecker-db
    ```
    You may have to replace the 5432 with a different port if you already have a PostgreSQL instance running on your machine (xxxx:5432).

6. Run the retrieve_TLE.py script in both modes to populate the database with supplemental and general TLE data:

   ```bash
   python retrieve_TLE.py -m gp -s localhost -p 5432 -d postgres -u postgres -pw sat123 -sc celestrak
   ```

   ```bash
   python retrieve_TLE.py -m sup -s localhost -p 5432 -d postgres -u postgres -pw sat123 -sc celestrak
    ```

7. You can now connect to the database using your preferred PostgreSQL client to verify the data was loaded correctly. If you changed any of the database setup fields, you'll have to update them in `utils.py` in the SatChecker code to match.
8. Sample request to test the database connection:
    ```bash
    http://localhost:5000/ephemeris/name/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1
    ```

<a name="running-tests"></a>
## Running Tests
If you are in the main `satchecker` directory, run the following command to run the pytest tests with code coverage:

```bash
python -m pytest
```

The code coverage report is generated in html by default, and can be found at satchecker/htmlcov/index.html after running the tests. Edit the pytest.ini if you need to change the code coverage report format.

<a name="building-rtd-documentation"></a>
## Building RTD Documentation
1. Navigate to `satchecker/docs` and run the following command to install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the following command to build the documentation:
    ```bash
    make clean html
    ```
3. Open a browser and navigate to `satchecker/docs/build/html/index.html` to view the documentation.

The documentation will be built automatically when you push to the `main` branch. You can view the latest version [here](https://satchecker.readthedocs.io/en/latest/).

<a name="tools"></a>
## Tools

### Formatting and Linting
Right now the code is set up to use [Black](https://black.readthedocs.io/en/stable/) for code formatting and [Ruff](https://docs.astral.sh/ruff/) for linting with the following rules turned on:
* E (pycodestyle errors)
* F (Pyflakes)
* I (isort)
* N (pep8-naming)
* UP (pyupgrade)
* S (flake8-bandit)
* B (flake8-bugbear)

Ruff and Black can be set up to run as pre-commit hooks, but they are also run on every push to a branch in the run_tests.yml workflow (which also runs all the tests)

<a name="deployment-infrastructure"></a>
## Deployment & Infrastructure
All active development takes place in GitHub. The main branch is the one that’s deployed to production; develop is the one that is deployed to test. Pull requests merged into develop are automatically deployed to the test environment, but main is only deployed
upon a release.

Service deployment and network management is done by NOIRLab's IT department. Pull requests and merges must be approved by an IAU CPS repo maintainer before they can be merged into the main or develop branches.

### AWS

[Network Organization](setup/aws/satchecker_AWS_network.drawio.png)

[AWS Services](setup/aws/satchecker_AWS_services.drawio.png)


<a name="architecture"></a>
## Architecture


<a name="license"></a>
## License
[![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
