from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from ...models import PersonFilmwork

from .mixins import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 1

    def get_queryset(self):
        queryset = self.model.objects.all().values().annotate(
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
        page_number = self.request.GET.get('page')
        if not page_number:
            self.paginate_by = queryset.count()
        paginator = Paginator(queryset, self.paginate_by)
        try:
            movies = paginator.get_page(page_number)
        except PageNotAnInteger:
            movies = paginator.get_page(1)
        return movies


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = self.model.objects.filter(pk=pk).values().annotate(
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(
                    personfilmwork__role=PersonFilmwork.RoleChoices.ACTOR),
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
        return queryset
