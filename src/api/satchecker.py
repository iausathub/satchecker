"""SatChecker application runner."""

from api import app
from api.celery_app import celery  # noqa: F401

if __name__ == "__main__":
    app.run(debug=True)
