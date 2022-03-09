import os
import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

from dotenv import load_dotenv

from loaders import load_from_sqlite


load_dotenv('../app/.env')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': 5432
    }
    with sqlite3.connect(os.path.join(CURRENT_DIR, 'db.sqlite')) as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        query = [
            "create role etl with password '123qwe'",
            'alter role etl with login',
            # 'grant all privileges on all tables in schema public to etl',
            'grant all privileges on all tables in schema content to etl',
            # 'alter role etl set search_path to content, public',
        ]
        query = ';'.join(query)
        pg_conn.cursor().execute(query)
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
