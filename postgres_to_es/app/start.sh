#!/bin/sh

./entrypoint.sh &&
./create_superuser.sh &&
gunicorn config.wsgi:application
