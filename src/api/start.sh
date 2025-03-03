#!/bin/bash

# Set PYTHONPATH to include the parent directory of api
cd /usr/src/app/api
export PYTHONPATH="/usr/src/app"

# Run database migrations
alembic -c migrations/alembic.ini upgrade head

# Start the Celery worker in the background
celery -A api.satchecker.celery worker --loglevel INFO &

# Start the Flask server in the foreground
exec gunicorn --workers=3 --timeout 120 -b 0.0.0.0:5000 --access-logfile - api.satchecker:app
