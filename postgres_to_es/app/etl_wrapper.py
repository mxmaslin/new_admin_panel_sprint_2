import os
import time

from datetime import datetime, timedelta

import psycopg2

from etl.extract import extract
from etl.transform import transform
from etl.load import load

from dotenv import load_dotenv

load_dotenv('../app/.env')

TIMEOUT_SECONDS = 2
prev = datetime.min
now = datetime.now()


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': 5432
    }
    with psycopg2.connect(**dsl) as conn:
        while True:
            extracted = extract(conn, prev, now)
            transformed = transform(extracted)
            load(transformed)
            time.sleep(TIMEOUT_SECONDS)
            prev = now
            now += timedelta(seconds=TIMEOUT_SECONDS)
