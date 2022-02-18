from abc import ABC, abstractmethod

from django.core import serializers
from django.http import JsonResponse

from ...models import Filmwork


class MoviesApiMixin(ABC):
    model = Filmwork
    http_method_names = ['get']

    @abstractmethod
    def get_queryset(self):
        pass

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        count, page, is_paginated, queryset = [
            x[1] for x in self.get_queryset().items()
        ]
        serialized = serializers.serialize('json', queryset)
        context = {
            'results': serialized,
        }
        return context
