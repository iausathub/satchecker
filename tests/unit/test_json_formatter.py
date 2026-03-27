# ruff: noqa: S101
import json
import logging
import sys

from api import JSONFormatter


def make_record(msg="Test", level=logging.INFO, name="test", exc_info=None, **extras):
    """Helper to create a log record."""
    record = logging.LogRecord(
        name=name,
        level=level,
        pathname="",
        lineno=0,
        msg=msg,
        args=(),
        exc_info=exc_info,
    )
    for key, value in extras.items():
        setattr(record, key, value)
    return record


class TestJSONFormatter:
    """Tests for JSONFormatter class."""

    def test_message_format(self):
        """Test JSON log message formatting."""
        formatter = JSONFormatter()
        record = make_record("Test message", name="test.logger")
        data = json.loads(formatter.format(record))

        # Required fields present
        assert data["timestamp"].endswith("Z")
        assert "T" in data["timestamp"]
        assert data["level"] == "INFO"
        assert data["logger"] == "test.logger"
        assert data["message"] == "Test message"

        # Extra fields not present
        assert "endpoint" not in data
        assert "method" not in data
        assert "status" not in data

    def test_extra_fields_included(self):
        """Test that extra fields are included when set."""
        formatter = JSONFormatter()
        record = make_record(
            "api_request",
            endpoint="get-tle-data",
            method="GET",
            path="/tools/get-tle-data",
            status=200,
            duration_ms=45.23,
            ip="192.168.1.100",
            query="id=25544&id_type=catalog",
            user_agent="python-requests/2.31.0",
        )
        data = json.loads(formatter.format(record))

        assert data["endpoint"] == "get-tle-data"
        assert data["method"] == "GET"
        assert data["status"] == 200
        assert data["duration_ms"] == 45.23

    def test_exception_traceback_included(self):
        """Test that exception tracebacks are captured."""
        formatter = JSONFormatter()
        try:
            raise ValueError("Test error")
        except ValueError:
            exc_info = sys.exc_info()

        record = make_record(exc_info=exc_info, level=logging.ERROR)
        data = json.loads(formatter.format(record))

        assert "exception" in data
        assert "ValueError" in data["exception"]
        assert "Test error" in data["exception"]
