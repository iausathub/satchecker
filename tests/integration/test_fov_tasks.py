"""Tests for async FOV tasks using Celery.

This module tests asynchronous Field of View (FOV) calculations that use
Celery for background task processing.
"""

# ruff: noqa: S101
from datetime import datetime

from tests.factories.satellite_factory import SatelliteFactory
from tests.factories.tle_factory import TLEFactory

from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.services.tasks.fov_tasks import get_fov_task_status


def test_get_fov_task_status_pending(app, mocker):
    """Test getting status of a pending task."""
    with app.app_context():
        # Use a fake task ID
        task_id = "fake-task-id-12345"

        status = get_fov_task_status(task_id)

        # Should return pending status for task that hasn't been run yet
        assert status["status"] == "PENDING"
        assert status["task_id"] == task_id
        assert "message" in status


def test_fov_endpoint_async_integration(client, session, services_available):
    """Test the async endpoint returns a task and the status endpoint is queryable."""
    # Create test satellite and TLE
    satellite = SatelliteFactory(sat_name="ISS", sat_number=25544)
    tle = TLEFactory(
        satellite=satellite,
        epoch=datetime(2024, 10, 1, 0, 0, 0),
    )

    tle_repo = SqlAlchemyTLERepository(session)
    tle_repo.add(tle)
    session.commit()

    # Make request with async=true
    response = client.get(
        "/fov/satellite-passes/?latitude=0&longitude=0&elevation=0"
        "&mid_obs_time_jd=2460218.5&duration=30&ra=224.048903&dec=78.778084"
        "&fov_radius=2&group_by=satellite&async=true"
    )

    assert response.status_code == 200
    data = response.json

    # Should return task information with valid task_id
    assert "task_id" in data
    assert data["task_id"] is not None
    assert isinstance(data["task_id"], str)

    assert "status" in data
    assert data["status"] in ["PENDING", "PROGRESS", "SUCCESS"]

    assert "message" in data
    assert isinstance(data["message"], str)

    # Verify task status endpoint is queryable
    task_id = data["task_id"]
    status_response = client.get(f"/fov/task-status/{task_id}")

    assert status_response.status_code == 200
    status_data = status_response.json

    # Verify status endpoint returns valid structure
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

    # Make request with async=false for immediate results
    response = client.get(
        "/fov/satellite-passes/?latitude=0&longitude=0&elevation=0"
        "&mid_obs_time_jd=2460218.5&duration=30&ra=224.048903&dec=78.778084"
        "&fov_radius=2&group_by=satellite&async=false"
    )

    assert response.status_code == 200
    data = response.json

    # Should return actual results, not a task ID
    assert "task_id" not in data
    # Should have FOV data
    assert "data" in data or "satellites" in data or "info" in data


def test_get_fov_task_status_progress(app, mocker):
    """Test getting status of a task in progress."""
    with app.app_context():
        # Mock a task in PROGRESS state
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
        # Mock a task in FAILURE state
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
        # Mock AsyncResult to raise an exception
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
        # Mock a task in an unknown/custom state
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
        # Mock a task in SUCCESS state with a list result
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
        # Mock a task in SUCCESS state with a non-list result
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
        assert metrics["propagation_time"] == 0.8  # 0.5 + 0.3
