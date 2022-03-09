import time

from datetime import datetime, timedelta

from etl.extract import extract
from etl.transform import transform
from etl.load import load


TIMEOUT_SECONDS = 2
prev = datetime.min
now = datetime.now()

if __name__ == '__main__':
    while True:
        extracted = extract(prev, now)
        transformed = transform(extracted)
        load(transformed)
        time.sleep(TIMEOUT_SECONDS)
        prev = now
        now += timedelta(seconds=TIMEOUT_SECONDS)
