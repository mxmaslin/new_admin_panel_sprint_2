import json

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
        return JsonResponse({'results': context})

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        from django.core.serializers.json import DjangoJSONEncoder
        serialized = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        serialized = json.loads(serialized)
        return serialized
