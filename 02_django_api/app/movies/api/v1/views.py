from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from .mixins import MoviesApiMixin


class MoviesListApi(BaseListView, MoviesApiMixin):
    def get_queryset(self):
        return []

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()

        context = {
            'results': list(self.get_queryset()),
        }
        return context

        # paginator, page, queryset, is_paginated = self.paginate_queryset(
        #     queryset,
        #     self.paginate_by
        # )
        # return {
        #     'count': paginator.count,
        #     'page': page
        # }



class MoviesDetailApi(BaseDetailView, MoviesApiMixin):
    def get_queryset(self):
        return []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset()),
        }
        return context
