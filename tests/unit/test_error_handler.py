# ruff: noqa: S101
from werkzeug.exceptions import BadRequest, NotFound

from api.common.exceptions import ValidationError
from api.middleware.error_handler import handle_error


def test_handle_http_exception(app):
    with app.test_request_context("/test"):
        error = NotFound()
        response, status_code = handle_error(error)
        assert status_code == 404
        assert "error_type" in response.json
        assert response.json["error_type"] == "NotFound"


def test_handle_validation_error(app):
    with app.test_request_context("/test"):
        error = ValidationError(400, "Test validation error")
        response, status_code = handle_error(error)
        assert status_code == 400
        assert response.json["message"] == "Test validation error"
        assert response.json["error_type"] == "ValidationError"


def test_handle_generic_exception(app):
    with app.test_request_context("/test"):
        error = Exception("Unexpected error")
        response, status_code = handle_error(error)
        assert status_code == 500
        assert response.json["message"] == "Internal server error"
        assert response.json["error_type"] == "Exception"


def test_error_response_structure(app):
    with app.test_request_context("/test"):
        error = BadRequest("Bad request test")
        response, status_code = handle_error(error)
        assert set(response.json.keys()) == {
            "path",
            "method",
            "error_type",
            "message",
            "status_code",
        }


def test_error_path_and_method(app):
    with app.test_request_context("/custom/path", method="POST"):
        error = BadRequest()
        response, status_code = handle_error(error)
        assert response.json["path"] == "/custom/path"
        assert response.json["method"] == "POST"


def test_error_with_custom_status_code(app):
    with app.test_request_context("/test"):
        error = ValidationError(429, "Rate limit exceeded")
        response, status_code = handle_error(error)
        assert status_code == 429
        assert response.json["message"] == "Rate limit exceeded"


def test_handle_exception_with_non_integer_code(app):
    # SQLAlchemy errors carry a "code" attribute that is a docs slug string
    # (e.g. "9h9h"), not an HTTP status. It must not be treated as a status code.
    class FakeSQLAlchemyError(Exception):
        code = "9h9h"

    with app.test_request_context("/test"):
        error = FakeSQLAlchemyError("invalid input syntax for type integer")
        response, status_code = handle_error(error)
        assert status_code == 500
        assert response.json["message"] == "Internal server error"
        assert response.json["error_type"] == "FakeSQLAlchemyError"
