import os
import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

from dotenv import load_dotenv

from loaders import load_from_sqlite


load_dotenv('../app/.env')

if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        # 'host': 'localhost',
        'port': 5432
    }
    print('yay ' * 10000)
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
