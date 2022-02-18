import json

from django.core import serializers
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from .mixins import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_queryset(self):
        queryset = self.model.objects.all()
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
