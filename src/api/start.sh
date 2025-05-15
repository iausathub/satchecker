#!/bin/bash

# Set PYTHONPATH to include the parent directory of api
cd /usr/src/app/api
export PYTHONPATH="/usr/src/app"

# Run database migrations
alembic -c migrations/alembic.ini upgrade head

# Start the Celery worker in the background
celery -A api.satchecker.celery worker --loglevel INFO &

# Start the Flask server in the foreground
exec gunicorn --workers=4 --threads=4 --timeout 300 -b 0.0.0.0:5000 --access-logfile - --keep-alive 120 api.satchecker:app
