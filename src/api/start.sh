#!/bin/bash


export PYTHONPATH="${PYTHONPATH}:$(pwd)/src:src"


# Start the Celery worker in the background
celery -A api.satchecker.celery worker --loglevel INFO &

echo $PYTHONPATH
# Start the Flask server in the foreground
exec gunicorn --workers=3 --timeout 120 -b 0.0.0.0:5000 --access-logfile - api.satchecker:app
