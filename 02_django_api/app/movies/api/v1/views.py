from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Count
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from ...models import GenreFilmwork

from .mixins import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_queryset(self):
        queryset = self.model.objects.all().annotate(
            movie_persons=ArrayAgg('persons')
        ).order_by('title')
        # for v in queryset.values():
        #     print(v['movie_genres'], type(v['movie_genres']))

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
