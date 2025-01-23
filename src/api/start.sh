#!/bin/bash

export PYTHONPATH="/usr/src/app/api:${PYTHONPATH}:$(pwd)/src"

# Run database migrations
cd /usr/src/app/api
alembic -c migrations/alembic.ini upgrade head

# Start the Celery worker in the background
celery -A api.satchecker.celery worker --loglevel INFO &

echo $PYTHONPATH
# Start the Flask server in the foreground
exec gunicorn --workers=3 --timeout 120 -b 0.0.0.0:5000 --access-logfile - api.satchecker:app
