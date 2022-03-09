import logging
# import os
import psycopg2

# from psycopg2.extras import DictCursor

# from dotenv import load_dotenv


# load_dotenv('../app/.env')

Log_Format = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(
    filename='logfile.log',
    filemode='w',
    format=Log_Format,
    level=logging.ERROR
)
logger = logging.getLogger()


schema = [
    {
        'id': 'uuid',
        'imdb_rating': 10.0,
        'genre': 'genre_name',
        'title': 'title',
        'description': 'description',
        'director': 'director',
        'actors_names': [],
        'writers_names': [],
        'actors': [
            {
                'id': 'uuid',
                'name': 'actor_name'
            }
        ],
        'writers': [
            {
                'id': 'uuid',
                'name': 'actor_name'
            }
        ]
    }
]

# if not etl:
#     mapping['directors'] = ArrayAgg(
#         'persons__full_name',
#         filter=Q(personfilmwork__role=PersonFilmwork.RoleChoices.DIRECTOR),
#         distinct=True
#     )
#     mapping['actors'] = ArrayAgg(
#         'persons__full_name',
#         filter=Q(personfilmwork__role=PersonFilmwork.RoleChoices.ACTOR),
#         distinct=True
#     )
#     mapping['writers'] = ArrayAgg(
#         'persons__full_name',
#         filter=Q(personfilmwork__role=PersonFilmwork.RoleChoices.WRITER),
#         distinct=True
#     )
#     mapping['genres'] = ArrayAgg('genre__name', distinct=True)
# else:
#     mapping['director'] = StringAgg(
#         'persons__full_name',
#         filter=Q(personfilmwork__role=PersonFilmwork.RoleChoices.DIRECTOR),
#         distinct=True,
#         delimiter=' '
#     )
#     mapping['actors_names'] = ArrayAgg(
#         'persons__full_name',
#         filter=Q(personfilmwork__role=PersonFilmwork.RoleChoices.ACTOR),
#         distinct=True
#     )
#     mapping['writers_names'] = ArrayAgg(
#         'persons__full_name',
#         filter=Q(personfilmwork__role=PersonFilmwork.RoleChoices.WRITER),
#         distinct=True
#     )
#     mapping['actors'] = JSONBAgg(
#         # Func(
#         #     Value('persons__id'), 'persons__id',
#         #     Value('persons__full_name'), 'persons__full_name'
#         # ),
#         ('persons__full_name', 'persons__id'),
#         # Func(
#         #     F('persons__id'),
#         #     F('persons__full_name')
#         # ),
#         filter=Q(personfilmwork__role=PersonFilmwork.RoleChoices.ACTOR),
#         distinct=True
#     )
#     # mapping['actors'] = ArrayAgg(
#     #     id=F('persons__id').filter(
#     #         Q(personfilmwork__role=PersonFilmwork.RoleChoices.ACTOR)
#     #     ).distinct(),
#     #     name=F('persons__full_name').filter(
#     #         Q(personfilmwork__role=PersonFilmwork.RoleChoices.ACTOR)
#     #     ).distinct()
#     # )
#     # mapping['writers'] = ArrayAgg(
#     #     id=F('persons__id').filter(
#     #         Q(personfilmwork__role=PersonFilmwork.RoleChoices.WRITER)
#     #     ).distinct(),
#     #     name=F('persons__full_name').filter(
#     #         Q(personfilmwork__role=PersonFilmwork.RoleChoices.WRITER)
#     #     ).distinct()
#     # )
#     mapping['genre'] = StringAgg(
#         'genre__name', distinct=True, delimiter=' '
#     )
# return mapping[aggregate_this]


def extract(conn, prev, now):
    query = 'select * from content.film_work;'
    # query = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'"
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        logger.exception(e)
    fetched = cursor.fetchall()
    for entry in fetched:
        print('yay ' * 10)
        print(entry)
