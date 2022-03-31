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

    d.get_movies(False)

    return HttpResponse('Movies are saved to database.')

def top_250(request):

    d = Data()

    top250 = d.get_movies(True)

    # print(top250)
    print(len(top250))

    return render(request, 'home.html', {'top250': top250})

def update_image(request):
    d = Data()

    d.update_image()

    return HttpResponse('All images are updated.')