from django.http import HttpResponse
from django.shortcuts import render
from .actors import Actor
from .models import actor
# Create your views here.

def actors(request):
    a = Actor()
    actors = a.get_actors()
    print(len(actors))
    print(actors)
    for a in actors:
        if a:
            if a['birthYear'] == '\\N':
                a['birthYear'] = 0
            if a['deathYear'] == '\\N':
                a['deathYear'] = 0
            # print(a['deathYear'])
            if not actor.objects.filter(id=a['id']):
                temp = actor(a['id'], a['name'], a['birthYear'], a['deathYear'], a['movie1'], a['movie2'], a['movie3'], a['movie4'])
                temp.save()

    return HttpResponse("Saved")
