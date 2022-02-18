from django.urls import path, re_path

from . import views

urlpatterns = (
    path('movies/<int:page>/', views.MoviesListApi.as_view()),
)
