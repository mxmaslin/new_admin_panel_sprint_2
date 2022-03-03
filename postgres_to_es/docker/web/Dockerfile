FROM python:3.10.1-alpine3.14
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip --no-cache-dir

COPY ./app/requirements.txt ./app/start.sh ./app/entrypoint.sh ./app/create_superuser.sh ./sqlite_to_postgres ./

RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh && chmod +x /usr/src/app/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/create_superuser.sh && chmod +x /usr/src/app/create_superuser.sh
RUN sed -i 's/\r$//g' /usr/src/app/start.sh && chmod +x /usr/src/app/start.sh

RUN pip install -r requirements.txt

RUN mkdir -p /gunicorn/

COPY . .

EXPOSE 8000

CMD ["./start.sh"]
