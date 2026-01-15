# Testing

## Test Structure and Organization

SatChecker uses **pytest** as its testing framework with the following test structure:

```
tests/
├── conftest.py              # Global test configuration and fixtures
├── unit/                    # Unit tests for individual components
│   ├── test_satellite.py
│   ├── test_tle.py
│   ├── test_fov_service.py
│   ├── test_tools_service.py
│   └── ...
├── integration/             # Integration tests for API endpoints
│   ├── test_ephemeris_routes.py
│   ├── test_fov_routes.py
│   ├── test_tools_routes.py
│   └── ...
├── benchmark/               # Performance benchmark tests
│   ├── test_ephemeris_benchmark.py
│   ├── test_fov_benchmark.py
│   └── ...
├── factories/               # Test data factories
│   ├── satellite_factory.py
│   └── tle_factory.py
└── data/                    # Test data files
    └── de430t.bsp           # Included here for CI runs
```

## Running Tests

### Prerequisites
Before running tests, ensure you have the required services running:

1. **PostgreSQL** - Test database
2. **Redis** - For caching and Celery tasks

### Basic Test Commands

```bash
# Run all tests (excluding benchmarks)
pytest -v --durations=10 --ignore=tests/benchmark

# Run with coverage reporting
pytest --cov=. --cov-report html --cov-report term-missing

# Run specific test categories
pytest tests/unit/                    # Unit tests only
pytest tests/integration/             # Integration tests only
pytest tests/benchmark/               # Benchmark tests only

### Environment Variables for Testing

Set these environment variables before running tests:

```bash
export PYTHONPATH=/satchecker/src/ # wherever that is on your machine
export SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/test_satchecker"
export LOCAL_DB=1
```

### Test Configuration

The test suite is configured in `pytest.ini`.


## Test Fixtures and Utilities

### Database Fixtures
- **`app`**: Flask application with test configuration
- **`client`**: Test client for making HTTP requests
- **`session`**: Database session for each test
- **`cleanup_database`**: Automatic database cleanup after each test
- **`pg_session_factory`**: Database session factory for each test

### Service Fixtures
- **`services_available`**: Checks if PostgreSQL and Redis are available
- **`cleanup_cache`**: Clears Redis cache after each test

### Utility Fixtures
- **`test_location`**: Test location using EarthLocation
- **`test_time`**: Test time using Time

### Mock Repositories
- **`FakeSatelliteRepository`**: Mock satellite data repository
- **`FakeTLERepository`**: Mock TLE data repository

### Test Factories
- **`SatelliteFactory`**: Creates test satellite objects using Faker
- **`TLEFactory`**: Creates test TLE objects using Faker

## Test Categories

### Unit Tests (`tests/unit/`)
Test individual components in isolation:
- Domain models (`test_satellite.py`, `test_tle.py`)
- Services (`test_fov_service.py`, `test_tools_service.py`)
  - This is where the bulk of the service logic is tested.
- Utilities (`test_utils.py`)
- Validation (`test_validation_service.py`)

### Integration Tests (`tests/integration/`)
Test API endpoints and component interactions:
- **Ephemeris Routes** (`test_ephemeris_routes.py`): Test satellite position calculations
- **FOV Routes** (`test_fov_routes.py`): Test field-of-view analysis
- **Tools Routes** (`test_tools_routes.py`): Test utility endpoints
- **Repository Tests**: Test database interactions

### Benchmark Tests (`tests/benchmark/`)
Performance testing for critical operations:
- **Ephemeris Benchmarks**: Individual satellite position calculation performance
- **FOV Benchmarks**: Field-of-view endpoint performance
- **Tools Benchmarks**: Utility function performance (retrieving TLEs, satellite metadata, etc.)

Benchmark tests are run separately in a GitHub Actions workflow that runs on every push to the `main` branch.
Results are stored in the `dev/bench` directory and are automatically uploaded to the GitHub Pages site for the repo
(via the `gh-pages` branch).

## Continuous Integration

Tests run automatically on:
- **GitHub Actions**: On every push and pull request
- **GitLab CI**: For deployment pipelines

## Known Issues

1. **Flaky tests**
   - There are currently 2 flaky tests - if this happens in a GitHub Actions run, re-run the test action.
   If it happens locally, re-run the individual test.
     - `test_fov_service.py::test_satellite_in_fov`
     - `test_fov_service.py::test_get_satellites_above_horizon_exception_handling`

2. **Benchmark tests**
    - These used to time out - they don't anymore, but there is technically a chance they
    still could if load on the server is too high. This would be a good indication to check
    with IT about increasing the resources allocated to the server.
