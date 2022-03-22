from django.http import HttpResponse
from django.shortcuts import render
from .models import actor, movie
from .data import Data
import datetime
import imdb

# # Create your views here.
#
#
# def actors(request):
#     a = Actor()
#     actors = a.get_actors()
#     print(len(actors))
#     print(actors)
#     for a in actors:
#         if a:
#             if a['birthYear'] == '\\N':
#                 a['birthYear'] = 0
#             if a['deathYear'] == '\\N':
#                 a['deathYear'] = 0
#             # print(a['deathYear'])
#             if not actor.objects.filter(id=a['id']):
#                 temp = actor(a['id'], a['name'], a['birthYear'], a['deathYear'], a['movie1'], a['movie2'], a['movie3'], a['movie4'])
#                 temp.save()
#
#     return HttpResponse("Actors are saved to database.")


def movies(request):
    d = Data()

    d.get_movies()

    return HttpResponse('Movies are saved to database.')

def top_250(request):
    ia = imdb.IMDb()

    top = ia.get_top250_movies()


#
#
# def genres(request):
#     g = Genre()
#
#     g.get_genres()
#
#     return HttpResponse('genres were added to movies.')
