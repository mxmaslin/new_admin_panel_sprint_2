import os
import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

from dotenv import load_dotenv

from loaders import load_from_sqlite

ENV_PATH = '../.env'
PATH_TO_SQLITE = './sqlite_to_postgres/db.sqlite'

load_dotenv(ENV_PATH)


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    with sqlite3.connect(PATH_TO_SQLITE) as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
