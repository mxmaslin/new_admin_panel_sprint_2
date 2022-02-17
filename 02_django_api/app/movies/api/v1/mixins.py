from django.http import JsonResponse

from ...models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
