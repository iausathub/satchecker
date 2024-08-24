#!/bin/bash


export PYTHONPATH="${PYTHONPATH}:$(pwd)"


# Start the Celery worker in the background
celery -A api.satchecker.celery worker --loglevel INFO &


# Start the Flask server in the foreground
gunicorn --workers=3 --timeout 120 -b 0.0.0.0:5000 --access-logfile - api.satchecker:app
