import abc
import json
import redis
import time

import psycopg2

from psycopg2.extras import DictCursor
from typing import Any, Optional
from pathlib import Path
from functools import wraps


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        file = Path(self.file_path)
        file.touch()

    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        with open(self.file_path, 'w') as f:
            j = json.dumps(state)
            f.write(j)

    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        with open(self.file_path, 'r') as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)


class RedisStorage(BaseStorage):
    def __init__(self):
        self.r = redis.StrictRedis(decode_responses=True)

    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        key = [*state]
        try:
            key = key[0]
        except IndexError:
            pass
        else:
            self.r.set(key, state[key])

    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        keys = [x for x in self.r.keys() if not x.startswith('_kombu')]
        try:
            key = keys[0]
        except IndexError:
            return {}
        return {key: self.r.get(key)}


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state()
        if key in state.keys():
            return state[key]
        return None


storage = RedisStorage()

state = State(storage)
# state.set_state('my_key', 666)
print(state.get_state('my_key'))
print(state.get_state('other_key'))



# def backoff(f):
#     """
#     Функция для повторного выполнения функции через некоторое время, если возникла ошибка. Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)
#
#     Формула:
#         t = start_sleep_time * 2^(n) if t < border_sleep_time
#         t = border_sleep_time if t >= border_sleep_time
#     :param f: decorated
#     :param start_sleep_time: начальное время повтора
#     :param factor: во сколько раз нужно увеличить время ожидания
#     :param border_sleep_time: граничное время ожидания
#     :return: результат выполнения функции
#     """
#     @wraps(f)
#     def inner(start_sleep_time=0.1, factor=2, border_sleep_time=10):
#         connected = False
#         t = 0
#         dsl = {
#             'dbname': 'postgres',
#             'user': 'app',
#             'password': '123qwe',
#             'host': '127.0.0.1',
#             'port': 5432
#         }
#         while connected is False:
#             if t < border_sleep_time:
#                 t += start_sleep_time * float(2 ** factor)
#             if t >= border_sleep_time:
#                 t = border_sleep_time
#             try:
#                 with psycopg2.connect(
#                     **dsl, cursor_factory=DictCursor
#                 ) as pg_conn:
#                     query = 'select * from content.genre limit 1'
#                     pg_conn.cursor().execute(query)
#             except Exception:
#                 time.sleep(t)
#             else:
#                 connected = True
#     return inner
#
#
# @backoff
# def start():
#     time.sleep(0.1)
#
#
# start()
