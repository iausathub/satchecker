#!/bin/bash

# Set PYTHONPATH to include the parent directory of api
cd /usr/src/app/api
export PYTHONPATH="/usr/src/app"

# Run database migrations
flask db upgrade head

# Start the Flask server in the foreground
exec gunicorn --workers=4 --threads=4 --worker-class=gthread --timeout 300 -b 0.0.0.0:5000 --access-logfile - --keep-alive 120 api.satchecker:app
