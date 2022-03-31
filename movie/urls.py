from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
#     path('getactors', views.actors, name='actor'),
    path('getmovies', views.movies, name='movie'),
    path('top250', views.top_250, name='top250'),
#     path('addgenres', views.genres, name='genre'),
    path('updateimage', views.update_image, name= 'updateimage'),
#
]