FROM postgres:13-alpine3.15

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

ADD ./movies_database.sql /docker-entrypoint-initdb.d

COPY . .
