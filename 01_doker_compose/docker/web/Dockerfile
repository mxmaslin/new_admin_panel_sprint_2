FROM python:3.10.1-alpine3.14
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./app/requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
