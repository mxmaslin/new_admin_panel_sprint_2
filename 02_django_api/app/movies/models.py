from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Filmwork(UUIDMixin, TimeStampedMixin):
    class MovieTypeChoices(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')

    title = models.CharField(
        max_length=255, verbose_name=_('Title')
    )
    description = models.CharField(
        max_length=255, blank=True, verbose_name=_('Description')
    )
    creation_date = models.DateField(verbose_name=_('Film created'))
    rating = models.FloatField(
        verbose_name=_('Rating'), blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(100)
        ]
    )
    type = models.CharField(
        max_length=10, default=_('Movie'), choices=MovieTypeChoices.choices,
        verbose_name=_('Type')
    )
    genres = models.ManyToManyField(
        'Genre', through='GenreFilmwork', verbose_name=_('Genres')
    )
    persons = models.ManyToManyField(
        'Person', through='PersonFilmwork', blank=True
    )
    objects = models.Manager()

    def __str__(self):
        return str(self.title) + ': ' + str(self.creation_date)

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('1. Filmworks')
        ordering = ['title', 'creation_date']
        indexes = (
            models.Index(
                name="film_work_idx",
                fields=(
                    'title', 'creation_date', 'rating', 'type'
                ),
            ),
        )


class Person(UUIDMixin, TimeStampedMixin):
    class Gender(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')

    full_name = models.CharField(
        max_length=255, verbose_name=_('Full name')
    )
    film_works = models.ManyToManyField(
        Filmwork, through='PersonFilmwork', blank=True
    )
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)
    objects = models.Manager()

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('2. Persons')
        ordering = ['full_name']
        indexes = (
            models.Index(
                name="person_idx",
                fields=('full_name',),
            ),
        )

    def __str__(self):
        return str(self.full_name)


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(
        max_length=255, verbose_name=_('Genre name')
    )
    description = models.CharField(
        max_length=255, blank=True, verbose_name=_('Description')
    )
    objects = models.Manager()

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('3. Genres')
        indexes = (
            models.Index(
                name="genre_name_idx",
                fields=('name',),
            ),
        )

    def __str__(self):
        return str(self.name)


class PersonFilmwork(UUIDMixin):
    class RoleChoices(models.TextChoices):
        ACTOR = 'actor', _('Actor')
        DIRECTOR = 'director', _('Director')
        PRODUCER = 'producer', _('Producer')

    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name=_('Persons')
    )
    film_work = models.ForeignKey(
        Filmwork, on_delete=models.CASCADE, verbose_name=_('Film works')
    )
    role = models.CharField(
        default=_(RoleChoices.ACTOR), max_length=200, choices=RoleChoices.choices
    )
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = "content\".\"person_film_work"
        unique_together = ('person', 'film_work', 'role',)
        indexes = (
            models.Index(
                name='person_film_work_idx',
                fields=('person_id', 'film_work_id', 'role'),
            ),
        )

    def __str__(self):
        return f'{str(self.film_work)}: {str(self.person)}: {self.role}'


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        Filmwork, on_delete=models.CASCADE, verbose_name=_('Film works')
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name=_('Genres')
    )
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = (
            models.Index(
                name='genre_film_work_idx',
                fields=('film_work_id', 'genre_id', 'created'),
            ),
        )

    def __str__(self):
        return f'{str(self.film_work)}: {str(self.genre)}'
