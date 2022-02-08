from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_movie_year(value):
    if value < 1896:
        raise ValidationError(_(f'{value} is not a valid year'))


def validate_film_work_rating(value):
    if 1 <= value >= 5:
        raise ValidationError(_(f'{value} is not a valid rating'))
