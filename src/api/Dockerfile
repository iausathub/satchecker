FROM --platform=linux/amd64 python:3.11-slim as python

# -m creates a writable home so Astropy can use ~/.astropy if needed
RUN useradd -m api

WORKDIR /usr/src/app

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc python3-dev openssl libssl-dev curl
RUN apt-get install -y gosu
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download Skyfield ephemeris and Astropy observatory sites so runtime
# does not depend on outbound fetches (sites.json download failures fall back
# to a Greenwich-only builtin list).
RUN mkdir -p /app/skyfield-data /app/astropy-data \
    && curl -sL -o /app/skyfield-data/de430t.bsp \
    https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de430t.bsp \
    && curl -sL -o /app/astropy-data/sites.json \
    https://www.astropy.org/astropy-data/coordinates/sites.json \
    && apt-get remove -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . ./api

ENV FLASK_APP satchecker.py
ENV SKYFIELD_DATA_DIR=/app/skyfield-data
ENV ASTROPY_SITES_JSON=/app/astropy-data/sites.json
ENV ASTROPY_CACHE_DIR=/tmp/astropy_cache
ENV SERVICE_NAME=api

RUN chown -R api:api ./ /app/skyfield-data /app/astropy-data
USER api
EXPOSE 5000

RUN chmod +x /usr/src/app/api/start.sh

CMD ./api/start.sh
