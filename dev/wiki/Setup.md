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
cd src/api
pip install -r requirements.txt
```

4. Configure the database - either set the environment variable for using the local database in ```.flaskenv```:
```bash
LOCAL_DB=1
```
or change the database configuration in ```.flaskenv``` (for example):
```bash
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=localhost # (or your database host)
DB_PORT=5432
DB_NAME=satchecker_test
```
or in ```src/api/config.py```:
```python
username, password, host, port, dbname = (
            "postgres",
            "postgres",
            "localhost", # (or your database host)
            "5432",
            "satchecker_test",
        )
```

<a name="local-database"></a>
### Local Database

#### Using a Local PostgreSQL database
1. Run this from either PGAdmin or the command line (from the main satchecker directory):
```bash
psql -U <username> -h <host> -d <dbname> -f /dev/local_db/db.sql
```

#### Using Docker

1. Install Docker Desktop for your OS: https://www.docker.com/products/docker-desktop (or PostgreSQL if you prefer to run it locally)
2. Open a terminal and navigate to the `dev/local_db` directory on your machine.
3. Run the following command to build the Docker image:
   ```bash
   docker build -t satchecker-db .
   ```
   If this is the first time you're setting this up, you'll also have to create a local volume for the database data so it doesn't get deleted when you stop the container:
   ```bash
   docker volume create satchecker_db_vol
   ```
4. Run the following command to start the container:

    ```bash
    docker run -d --name satchecker-db -v satchecker_db_vol:/var/lib/postgresql/data -p 5432:5432 satchecker-db
    ```
    You may have to replace the 5432 with a different port if you already have a PostgreSQL instance running on your machine (xxxx:5432).

### Celery/Redis setup
(under construction)
1. Install Redis w/ default settings.
2. pip install Celery
3. from api directory `celery -A satchecker.celery worker --loglevel INFO`


### Running SatChecker locally
1. Confirm the login details for your local database in `src/api/config.py` and change any of the fields below if needed. The dockerfile uses `sat123` as a db password, so if you used that you'll need to change the password here.

```python
username, password, host, port, dbname = (
            "postgres",
            "postgres",
            "localhost",
            "5432",
            "satchecker_test",
        )
```

2. Run the retrieve_TLE.py script in both modes to populate the database with supplemental and general TLE data (change db login as needed):

   ```bash
   python retrieve_TLE.py -m gp -s localhost -p 5432 -d postgres -u postgres -pw sat123 -sc celestrak
   ```

   ```bash
   python retrieve_TLE.py -m sup -s localhost -p 5432 -d postgres -u postgres -pw sat123 -sc celestrak
    ```

3. Start the API server:
```bash
export PYTHONPATH=/pathtosatchecker/satchecker/src
flask run
```

4. http://localhost:5000 should now redirect to the API documentation.

5. Sample request to test the database connection:
    ```bash
    http://localhost:5000/ephemeris/name/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&julian_date=2460000.1
    ```
