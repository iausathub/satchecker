FROM --platform=linux/amd64 python:3.11-slim as python

RUN useradd api

WORKDIR /usr/src/app

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc python3-dev openssl libssl-dev curl
RUN apt-get install -y gosu
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download Skyfield ephemeris to avoid runtime downloads
RUN mkdir -p /app/skyfield-data \
    && curl -sL -o /app/skyfield-data/de430t.bsp \
    https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de430t.bsp \
    && apt-get remove -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . ./api

ENV FLASK_APP satchecker.py
ENV SKYFIELD_DATA_DIR=/app/skyfield-data

RUN chown -R api:api ./ /app/skyfield-data
USER api
EXPOSE 5000

RUN chmod +x /usr/src/app/api/start.sh

CMD ./api/start.sh
