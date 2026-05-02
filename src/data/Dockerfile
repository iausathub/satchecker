#image for updating TLEs
FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /usr/src/app

COPY src/data/ ./

COPY src/data/docker_context_stubs/api/__init__.py ./api/__init__.py
COPY src/api/domain/models/satellite.py ./api/domain/models/satellite.py
COPY src/api/domain/models/interpolable_ephemeris.py ./api/domain/models/interpolable_ephemeris.py

ENV PYTHONPATH=/usr/src/app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
#
