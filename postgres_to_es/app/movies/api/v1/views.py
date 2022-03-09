from django.contrib.postgres.aggregates import ArrayAgg, StringAgg, JSONBAgg
from django.db.models import Q, F, Func, Value, CharField, JSONField
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from ...models import PersonFilmwork

from .mixins import MoviesApiMixin


def get_aggregation(aggregate_this):
    mapping = {
        'actors': ArrayAgg(
            'persons__full_name',
            filter=Q(personfilmwork__role=PersonFilmwork.RoleChoices.ACTOR),
            distinct=True
        ),
        'directors': ArrayAgg(
            'persons__full_name',
            filter=Q(
                personfilmwork__role=PersonFilmwork.RoleChoices.DIRECTOR),
            distinct=True
        ),
        'writers': ArrayAgg(
            'persons__full_name',
            filter=Q(
                personfilmwork__role=PersonFilmwork.RoleChoices.WRITER),
            distinct=True
        ),
        'genres': ArrayAgg('genre__name', distinct=True)
    }
    return mapping[aggregate_this]


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 1

    def get_queryset(self):
        queryset = self.model.objects.all().values().annotate(
            actors=get_aggregation('actors'),
            directors=get_aggregation('directors'),
            writers=get_aggregation('writers'),
            genres=get_aggregation('genres')
        ).order_by('title')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        movies_qs = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            movies_qs, self.get_paginate_by(movies_qs))
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(page.object_list),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = self.model.objects.filter(pk=pk).values().annotate(
            actors=get_aggregation('actors'),
            directors=get_aggregation('directors'),
            writers=get_aggregation('writers'),
            genres=get_aggregation('genres')
        ).order_by('title')
        return queryset
