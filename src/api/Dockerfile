FROM --platform=linux/amd64 python:3.11-slim as python

RUN useradd api

WORKDIR /usr/src/app

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc python3-dev openssl libssl-dev redis-server
RUN apt-get install -y gosu
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./api

ENV FLASK_APP satchecker.py

RUN chown -R api:api ./
USER api
EXPOSE 5000

RUN chmod +x /usr/src/app/api/start.sh

CMD redis-server & ./api/start.sh
