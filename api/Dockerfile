FROM python:slim

RUN useradd api

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core core
COPY satchecker.py ./

ENV FLASK_APP satchecker.py

RUN chown -R api:api ./
USER api

EXPOSE 5000

CMD [ "gunicorn", "--workers=3", "--timeout", "120", "-b", "0.0.0.0:5000", "--access-logfile", "-", "satchecker:app"]