import logging
import sqlite3

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch

from models import Movie, Person, Genre, PersonFilmWork, GenreFilmWork


Log_Format = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename='logfile.log',
                    filemode='w',
                    format=Log_Format,
                    level=logging.ERROR)
logger = logging.getLogger()

PAGE_SIZE = 1000


tables = {
    'film_work': {
        'class': Movie,
        'columns': (
            'id', 'title', 'description', 'creation_date', 'certificate',
            'file_path', 'rating', 'type', 'created', 'modified'
        ),
        'purge': ('certificate', 'file_path')
    },
    'person': {
        'class': Person,
        'columns': ('id', 'full_name', 'birth_date', 'created', 'modified'),
        'purge': ('birth_date',)
    },
    'genre': {
        'class': Genre,
        'columns': ('id', 'name', 'description', 'created', 'modified'),
        'purge': ()
    },
    'person_film_work': {
        'class': PersonFilmWork,
        'columns': ('id', 'person_id', 'film_work_id', 'role', 'created'),
        'purge': ()
    },
    'genre_film_work': {
        'class': GenreFilmWork,
        'columns': ('id', 'genre_id', 'film_work_id', 'created'),
        'purge': ()
    }
}


def purge(record, table):
    return {
        k: v for k, v in record.items()
        if k not in tables[table]['purge']
    }


class SQLiteLoader:
    def __init__(self, connection):
        self.conn = connection
        self.offset = 0

    def reset_offset(self):
        self.offset = 0

    def load(self, table):
        cursor = self.conn.cursor()
        sql = f'select * from {table} limit {PAGE_SIZE} offset {self.offset};'
        try:
            cursor.execute(sql)
        except sqlite3.OperationalError as e:
            logger.exception(f'Failed to execute the sql:\n{sql}')
        fetched = cursor.fetchall()
        if not fetched:
            return False, None
        records = []
        for record in fetched:
            dictified = dict(zip(tables[table]['columns'], record))
            purged = purge(dictified, table)
            prepared = tables[table]['class'](**purged)
            records.append(prepared)
        self.offset += PAGE_SIZE
        return True, records


class PostgresSaver:
    def __init__(self, pg_conn):
        self.conn = pg_conn

    def save_all_data(self, data, table):
        table_columns = [
            x for x in tables[table]['columns']
            if x not in tables[table]['purge']
        ]
        num_columns = len(table_columns)
        num_records = len(data)
        values = [
            tuple(
                data[i].__dict__[column]
                for column in table_columns
            )
            for i in range(num_records)
        ]
        table_columns = ', '.join(table_columns)
        values_placeholder = ', '.join(['%s' for _ in range(num_columns)])

        query = f'INSERT INTO {table} ({table_columns}) values ' \
                f'({values_placeholder}) on conflict(id) do nothing;'
        try:
            execute_batch(
                self.conn.cursor(), query, values, page_size=PAGE_SIZE
            )
        except Exception as e:
            logger.exception(e)
        self.conn.commit()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_loader = SQLiteLoader(connection)
    postgres_saver = PostgresSaver(pg_conn)

    for table in tables:
        sqlite_loader.reset_offset()
        while True:
            proceed, records = sqlite_loader.load(table)
            if not proceed:
                break
            if records:
                postgres_saver.save_all_data(records, table)
