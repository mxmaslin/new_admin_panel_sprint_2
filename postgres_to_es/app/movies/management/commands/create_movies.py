from django.core.management.base import BaseCommand

from ...models import Filmwork, Person, Genre, PersonFilmwork, GenreFilmwork


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bred = Person.objects.create(full_name='Bred Pit',
                                     gender=Person.Gender.MALE)
        angelo = Person.objects.create(full_name='Angelica Vroom',
                                       gender=Person.Gender.FEMALE)
        boober = Person.objects.create(full_name='Justine Boober',
                                       gender=Person.Gender.FEMALE)
        pomelo = Person.objects.create(full_name='Pomelo Underdog',
                                       gender=Person.Gender.FEMALE)
        leo = Person.objects.create(full_name='Leo Dikaprio',
                                     gender=Person.Gender.MALE)

        romcom = Genre.objects.create(name='Romcom')
        sitcom = Genre.objects.create(name='Sitcom')
        sci_fi = Genre.objects.create(name='Sci Fi')

        star_wars = Filmwork.objects.create(
            title='Star wars', creation_date='2001-11-29',
            type=Filmwork.MovieTypeChoices.MOVIE
        )
        star_wars.genre.add(sitcom, romcom)
        star_wars.persons.add(bred, angelo, boober, pomelo, leo)

        PersonFilmwork.objects.create(
            person=bred, film_work=star_wars,
            role=PersonFilmwork.RoleChoices.DIRECTOR
        )
        PersonFilmwork.objects.create(
            person=bred, film_work=star_wars,
            role=PersonFilmwork.RoleChoices.ACTOR
        )
        PersonFilmwork.objects.create(
            person=leo, film_work=star_wars,
            role=PersonFilmwork.RoleChoices.ACTOR
        )

        titanic = Filmwork.objects.create(
            title='Titanic', creation_date='2000-12-01',
            type=Filmwork.MovieTypeChoices.TV_SHOW
        )
        titanic.genre.add(sci_fi)
        star_wars.persons.add(angelo, pomelo, leo)

        PersonFilmwork.objects.create(
            person=angelo, film_work=titanic,
            role=PersonFilmwork.RoleChoices.ACTOR
        )
        PersonFilmwork.objects.create(
            person=pomelo, film_work=titanic,
            role=PersonFilmwork.RoleChoices.ACTOR
        )
        PersonFilmwork.objects.create(
            person=leo, film_work=titanic,
            role=PersonFilmwork.RoleChoices.DIRECTOR
        )
