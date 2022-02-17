import os

from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/', include('movies.api.urls')),
    prefix_default_language=False
)

if os.getenv('DEBUG'):
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
