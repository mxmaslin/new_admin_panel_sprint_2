FROM postgres:13.5

COPY ./app/movies_database.sql /docker-entrypoint-initdb.d/movies_database.sql

COPY . .
