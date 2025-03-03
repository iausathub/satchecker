FROM postgres
ENV POSTGRES_PASSWORD sat123
ENV POSTGRES_DB postgres
ENV POSTGRES_USER postgres
COPY db.sql /docker-entrypoint-initdb.d/
