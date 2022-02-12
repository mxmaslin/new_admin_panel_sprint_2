FROM postgres:13.5

COPY ./app/movies_database.ddl /docker-entrypoint-initdb.d/movies_database.ddl

COPY . .
