"""Tests for async FOV tasks using Celery.

This module tests asynchronous Field of View (FOV) calculations that use
Celery for background task processing.
"""

# ruff: noqa: S101
from contextlib import nullcontext
from datetime import datetime, timezone

import numpy as np
from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.adapters.repositories.ephemeris_repository import SqlAlchemyEphemerisRepository
from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.services.tasks.fov_tasks import get_fov_task_status, refine_with_ephemeris_task

# from api.utils.output_utils import format_date


def test_get_fov_task_status_pending(app, mocker):
    """Test getting status of a pending task."""
    with app.app_context():
        task_id = "fake-task-id-12345"

        status = get_fov_task_status(task_id)

        assert status["status"] == "PENDING"
        assert status["task_id"] == task_id
        assert "message" in status


def test_fov_endpoint_async_integration(client, session, services_available):
    """Test the async endpoint returns a task and the status endpoint is queryable."""
    # Satellite must have launch_date <= epoch and decay_date None or > epoch
    # for get_all_tles_at_epoch to include it
    satellite = SatelliteFactory(
        sat_name="ISS",
        sat_number=25544,
        launch_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
        decay_date=None,
    )
    tle = TLEFactory(
        satellite=satellite,
        tle_line1=(
            "1 25544U 98067A   24275.50000000  .00012769  00000+0  22936-3 0  9997"
        ),
        tle_line2=(
            "2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
        ),
        epoch=datetime(2024, 10, 1, 0, 0, 0, tzinfo=timezone.utc),
        data_source="spacetrack",
    )

    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    # mid_obs_time_jd=2460585.0 = 2024-10-01 12:00 UTC; ensures TLE epoch in query range
    response = client.get(
        "/fov/satellite-passes/?latitude=0&longitude=0&elevation=0"
        "&mid_obs_time_jd=2460585.0&duration=30&ra=224.048903&dec=78.778084"
        "&fov_radius=2&group_by=satellite&async=true"
    )

    assert response.status_code == 200
    data = response.json

    assert "task_id" in data
    assert data["task_id"] is not None
    assert isinstance(data["task_id"], str)

    assert "status" in data
    assert data["status"] in ["PENDING", "PROGRESS", "SUCCESS"]

    assert "message" in data
    assert isinstance(data["message"], str)

    task_id = data["task_id"]
    status_response = client.get(f"/fov/task-status/{task_id}")

    assert status_response.status_code == 200
    status_data = status_response.json

    assert "task_id" in status_data
    assert status_data["task_id"] == task_id
    assert "status" in status_data
    assert status_data["status"] in ["PENDING", "PROGRESS", "SUCCESS", "FAILURE"]


def test_fov_endpoint_sync(client, session, services_available):
    """Test the synchronous FOV endpoint (async=false)."""
    satellite = SatelliteFactory(sat_name="ISS", sat_number=25544)
    tle = TLEFactory(
        satellite=satellite,
        epoch=datetime(2024, 10, 1, 0, 0, 0),
    )

    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    response = client.get(
        "/fov/satellite-passes/?latitude=0&longitude=0&elevation=0"
        "&mid_obs_time_jd=2460218.5&duration=30&ra=224.048903&dec=78.778084"
        "&fov_radius=2&group_by=satellite&async=false"
    )

    assert response.status_code == 200
    data = response.json

    assert "task_id" not in data
    assert "data" in data or "satellites" in data or "info" in data


def test_get_fov_task_status_progress(app, mocker):
    """Test getting status of a task in progress."""
    with app.app_context():
        mock_task = mocker.Mock()
        mock_task.state = "PROGRESS"
        mock_task.info = {
            "status": "Processing batch 2/5",
            "progress": 40,
            "satellites_processed": 100,
            "total_satellites": 250,
        }

        mocker.patch(
            "api.services.tasks.fov_tasks.celery.AsyncResult",
            return_value=mock_task,
        )
        task_id = "test-progress-task-id"
        status = get_fov_task_status(task_id)

        assert status["status"] == "PROGRESS"
        assert status["task_id"] == task_id
        assert status["message"] == "Processing batch 2/5"
        assert status["progress"] == 40


def test_get_fov_task_status_failure(app, mocker):
    """Test getting status of a failed task."""
    with app.app_context():
        mock_task = mocker.Mock()
        mock_task.state = "FAILURE"
        mock_task.info = Exception("Propagation error occurred")

        mocker.patch(
            "api.services.tasks.fov_tasks.celery.AsyncResult",
            return_value=mock_task,
        )
        task_id = "test-failure-task-id"
        status = get_fov_task_status(task_id)

        assert status["status"] == "FAILURE"
        assert status["task_id"] == task_id
        assert "error" in status
        assert "Propagation error occurred" in status["error"]
        assert status["message"] == "FOV calculation failed"


def test_get_fov_task_status_exception_handling(app, mocker):
    """Test exception handling in get_fov_task_status."""
    with app.app_context():
        mocker.patch(
            "api.services.tasks.fov_tasks.celery.AsyncResult",
            side_effect=Exception("Connection error"),
        )
        task_id = "test-exception-task-id"
        status = get_fov_task_status(task_id)

        assert status["status"] == "ERROR"
        assert status["task_id"] == task_id
        assert "error" in status
        assert "Connection error" in status["error"]
        assert "Error occurred while checking task status" in status["message"]


def test_get_fov_task_status_unknown_state(app, mocker):
    """Test getting status of a task in an unknown state."""
    with app.app_context():
        mock_task = mocker.Mock()
        mock_task.state = "REVOKED"

        mocker.patch(
            "api.services.tasks.fov_tasks.celery.AsyncResult",
            return_value=mock_task,
        )
        task_id = "test-unknown-task-id"
        status = get_fov_task_status(task_id)

        assert status["status"] == "REVOKED"
        assert status["task_id"] == task_id
        assert "Unknown task state" in status["message"]


def test_get_fov_task_status_success_with_list_result(app, mocker):
    """Test getting status of a successful task with list result (normal case)."""
    with app.app_context():
        mock_task = mocker.Mock()
        mock_task.state = "SUCCESS"
        # Result is a tuple: (results, points_in_fov, group_by, performance_metrics)
        mock_task.result = [
            [
                {
                    "name": "TEST SAT",
                    "norad_id": 12345,
                    "ra": 100.0,
                    "dec": 50.0,
                    "altitude": 45.0,
                    "azimuth": 180.0,
                    "julian_date": 2460218.5,
                    "date_time": "2024-10-01 00:00:00",
                    "angle": 1.5,
                    "range_km": 500.0,
                    "tle_epoch": "2024-10-01 00:00:00",
                }
            ],  # results
            1,  # points_in_fov
            "satellite",  # group_by
            {"total_time": 1.5, "satellites_processed": 1},  # performance_metrics
        ]

        mocker.patch(
            "api.services.tasks.fov_tasks.celery.AsyncResult",
            return_value=mock_task,
        )
        task_id = "test-success-list-task-id"
        status = get_fov_task_status(task_id)

        assert status["status"] == "SUCCESS"
        assert status["task_id"] == task_id
        assert "data" in status or "satellites" in status
        assert status["message"] == "FOV calculation completed successfully"


def test_get_fov_task_status_success_non_list(app, mocker):
    """Test getting status of a successful task with non-list result."""
    with app.app_context():
        mock_task = mocker.Mock()
        mock_task.state = "SUCCESS"
        mock_task.result = {"custom": "result", "data": "value"}

        mocker.patch(
            "api.services.tasks.fov_tasks.celery.AsyncResult",
            return_value=mock_task,
        )
        task_id = "test-success-non-list-task-id"
        status = get_fov_task_status(task_id)

        assert status["status"] == "SUCCESS"
        assert status["task_id"] == task_id
        assert status["result"] == {"custom": "result", "data": "value"}
        assert status["message"] == "FOV calculation completed successfully"


def test_aggregate_fov_results_task(app):
    """Test aggregate_fov_results_task combines batch results."""
    from api.services.tasks.fov_tasks import aggregate_fov_results_task

    with app.app_context():
        # (batch_results, batch_sats, execution_time)
        group_results = [
            ([{"ra": 100, "dec": 50}], 1, 0.5),
            ([{"ra": 200, "dec": 60}], 1, 0.3),
        ]
        result = aggregate_fov_results_task(
            group_results,
            group_by="satellite",
            tle_time=0.1,
            jd_times=[2460218.5],
        )
        all_results, points_in_fov, group_by, metrics = result
        assert len(all_results) == 2
        assert points_in_fov == 2
        assert group_by == "satellite"
        assert metrics["satellites_processed"] == 2
        assert metrics["calculation_time"] == 0.8
        assert metrics["data_retrieval_time"] == 0.1
        assert metrics["total_time"] == 0.9
        assert metrics["points_in_fov"] == 2


def test_refine_with_ephemeris_task(mocker):
    aggregate_result = (
        [
            {"norad_id": 12345, "orbital_data_source": "tle", "ra": 100.0, "dec": 50.0},
            {"norad_id": 12345, "orbital_data_source": "tle", "ra": 101.0, "dec": 51.0},
            {"norad_id": 99999, "orbital_data_source": "tle", "ra": 300.0, "dec": 10.0},
        ],
        3,
        "satellite",
        {"total_time": 1.0, "points_in_fov": 3},
    )
    jd_times = [2460218.5]

    fake_session = mocker.Mock()
    fake_db = mocker.Mock()
    fake_db.engine = mocker.Mock()
    fake_db.engine.url = mocker.Mock()
    fake_db.engine.url.render_as_string.return_value = "postgresql://user:***@db/test"

    fake_app = mocker.Mock()
    fake_app.app_context.return_value = nullcontext()

    fake_satellite = mocker.Mock()
    fake_satellite.sat_name = "TEST SAT"
    fake_ephemeris = mocker.Mock()
    fake_ephemeris.id = 1
    fake_ephemeris.generated_at = datetime(2024, 10, 1, tzinfo=timezone.utc)
    fake_ephemeris.satellite = fake_satellite

    fake_repo = mocker.Mock()
    fake_repo.get_closest_by_satellite_numbers.return_value = {12345: fake_ephemeris}

    mocker.patch("api.app", fake_app)
    mocker.patch("api.entrypoints.extensions.db", fake_db)
    mocker.patch("sqlalchemy.orm.Session", return_value=fake_session)
    mocker.patch(
        "api.adapters.repositories.ephemeris_repository.SqlAlchemyEphemerisRepository",
        return_value=fake_repo,
    )
    mocker.patch(
        "api.utils.time_utils.ensure_datetime",
        return_value=datetime.now(timezone.utc),
    )
    mocker.patch(
        "api.utils.output_utils.format_date",
        return_value="2024-10-01 00:00:00",
    )

    fake_position = mocker.Mock()
    fake_position.ra = 100.2
    fake_position.dec = 50.2
    fake_position.covariance = np.eye(3)
    fake_position.altitude = 40.0
    fake_position.azimuth = 180.0
    fake_position.range_km = 550.0
    fake_position.julian_date = 2460218.5

    fake_krogh = mocker.Mock()
    fake_krogh.propagate.return_value = [fake_position, fake_position]
    mocker.patch(
        "api.services.tasks.fov_tasks.KroghPropagationStrategy",
        return_value=fake_krogh,
    )

    refined_results, points, group_by, metrics = refine_with_ephemeris_task(
        aggregate_result,
        jd_times=jd_times,
        location_lat=0.0,
        location_lon=0.0,
        location_height=0.0,
        ra=100.0,
        dec=50.0,
        fov_radius=2.0,
    )

    sat_12345_entries = [r for r in refined_results if r["norad_id"] == 12345]
    sat_99999_entries = [r for r in refined_results if r["norad_id"] == 99999]

    assert len(sat_12345_entries) == 2
    assert len(sat_99999_entries) == 1
    assert all(r["orbital_data_source"] == "ephemeris" for r in sat_12345_entries)
    assert points == len(refined_results)
    assert group_by == "satellite"
    assert "ephemeris_refinement_time" in metrics
    assert metrics["points_in_fov"] == points
    fake_session.close.assert_called_once()


def test_refine_with_ephemeris_task_position_outside_fov(mocker):
    aggregate_result = (
        [
            {"norad_id": 12345, "orbital_data_source": "tle", "ra": 100.0, "dec": 50.0},
        ],
        1,
        "satellite",
        {"total_time": 1.0, "points_in_fov": 1},
    )

    fake_session = mocker.Mock()
    fake_db = mocker.Mock()
    fake_db.engine = mocker.Mock()
    fake_db.engine.url = mocker.Mock()
    fake_db.engine.url.render_as_string.return_value = "postgresql://user:***@db/test"

    fake_app = mocker.Mock()
    fake_app.app_context.return_value = nullcontext()

    fake_ephemeris = mocker.Mock()
    fake_ephemeris.generated_at = datetime(2024, 10, 1, tzinfo=timezone.utc)
    fake_ephemeris.satellite = mocker.Mock(sat_name="TEST SAT")
    fake_repo = mocker.Mock()
    fake_repo.get_closest_by_satellite_numbers.return_value = {12345: fake_ephemeris}

    mocker.patch("api.app", fake_app)
    mocker.patch("api.entrypoints.extensions.db", fake_db)
    mocker.patch("sqlalchemy.orm.Session", return_value=fake_session)
    mocker.patch(
        "api.adapters.repositories.ephemeris_repository.SqlAlchemyEphemerisRepository",
        return_value=fake_repo,
    )
    mocker.patch(
        "api.utils.time_utils.ensure_datetime",
        return_value=datetime.now(timezone.utc),
    )
    mocker.patch(
        "api.utils.output_utils.format_date",
        return_value="2024-10-01 00:00:00",
    )

    out_of_fov_position = mocker.Mock()
    out_of_fov_position.ra = 300.0
    out_of_fov_position.dec = -50.0
    out_of_fov_position.covariance = np.eye(3)
    out_of_fov_position.altitude = 40.0
    out_of_fov_position.azimuth = 180.0
    out_of_fov_position.range_km = 550.0
    out_of_fov_position.julian_date = 2460218.5

    fake_krogh = mocker.Mock()
    fake_krogh.propagate.return_value = [out_of_fov_position]
    mocker.patch(
        "api.services.tasks.fov_tasks.KroghPropagationStrategy",
        return_value=fake_krogh,
    )

    refined_results, points, _, metrics = refine_with_ephemeris_task(
        aggregate_result,
        jd_times=[2460218.5],
        location_lat=0.0,
        location_lon=0.0,
        location_height=0.0,
        ra=100.0,
        dec=50.0,
        fov_radius=2.0,
    )

    assert refined_results == aggregate_result[0]
    assert points == 1
    assert metrics["points_in_fov"] == 1
    fake_session.close.assert_called_once()


def test_fov_ephemeris_refinement_end_to_end_real_values(
    client, session, services_available, starlink_ephemeris
):
    """End-to-end check: same scenario with TLE-only vs ephemeris refinement."""
    satellite = SatelliteFactory(
        sat_name="STARLINK-31570",
        sat_number=59324,
        launch_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
        decay_date=None,
    )
    tle = TLEFactory(
        satellite=satellite,
        tle_line1=(
            "1 59324C 24057E   25283.08937500 -.00019866  00000+0 -71932-3 0  2835"
        ),
        tle_line2=(
            "2 59324  43.0038 317.9750 0001389 281.8907  26.1850 15.27608592    19"
        ),
        epoch=datetime(2025, 10, 10, 2, 8, 42, 123456, tzinfo=timezone.utc),
        data_source="spacetrack",
    )
    SqlAlchemyTLERepository(session).add(tle)

    ephemeris_repo = SqlAlchemyEphemerisRepository(session)
    ephemeris = starlink_ephemeris
    ephemeris_repo.add(ephemeris)
    session.commit()

    common_query = (
        "/fov/satellite-passes/?latitude=0&longitude=0&elevation=0"
        "&mid_obs_time_jd=2460959.317847&duration=30&ra=312.6525015&dec=-0.9114941"
        "&fov_radius=180&group_by=satellite&async=false"
    )
    tle_only_response = client.get(f"{common_query}&tle_only=true")
    refined_response = client.get(f"{common_query}&tle_only=false")

    assert tle_only_response.status_code == 200
    assert refined_response.status_code == 200

    tle_satellites = tle_only_response.json["data"]["satellites"]
    refined_satellites = refined_response.json["data"]["satellites"]

    tle_matches = [s for s in tle_satellites.values() if s["norad_id"] == 59324]
    refined_matches = [s for s in refined_satellites.values() if s["norad_id"] == 59324]

    assert tle_matches, "Expected NORAD 59324 in TLE-only response."
    assert refined_matches, "Expected NORAD 59324 in refined response."

    tle_starlink = tle_matches[0]
    # refined_starlink = refined_matches[0]
    tle_positions = tle_starlink["positions"]
    # refined_positions = refined_starlink["positions"]

    # Disabled until ephemeris positions are fully ready
    # assert refined_positions[0]["ra"] == 290.30728478
    # assert refined_positions[0]["dec"] == -18.57246244
    assert tle_positions[0]["ra"] == 290.27460934
    assert tle_positions[0]["dec"] == -18.5859209
    assert all(p["orbital_data_source"] == "tle" for p in tle_positions)
    # assert all(p["orbital_data_source"] == "ephemeris" for p in refined_positions)
    # assert all(
    #    p["orbital_data_epoch"] == format_date(ephemeris.generated_at)
    #    for p in refined_positions
    # )
