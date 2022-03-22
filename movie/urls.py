from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
#     path('getactors', views.actors, name='actor'),
    path('getmovies', views.movies, name='movie'),
#     path('addgenres', views.genres, name='genre'),
#
]