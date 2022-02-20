from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Count
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from ...models import PersonFilmwork, GenreFilmwork

from .mixins import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_queryset(self):
        queryset = self.model.objects.all().annotate(
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleChoices.ACTOR),
                distinct=True
            ),
            directors=ArrayAgg(
                'persons__full_name',
                filter=Q(
                    personfilmwork__role=PersonFilmwork.RoleChoices.DIRECTOR),
                distinct=True
            ),
            writers=ArrayAgg(
                'persons__full_name',
                filter=Q(
                    personfilmwork__role=PersonFilmwork.RoleChoices.WRITER),
                distinct=True
            ),
            genres=ArrayAgg('genre__name', distinct=True)
        ).order_by('title')

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {
            'count': paginator.count,
            'page': page,
            'is_paginated': is_paginated,
            'queryset': queryset
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_queryset(self):
        return self.model.objects.first()
