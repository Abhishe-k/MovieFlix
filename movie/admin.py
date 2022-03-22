from django.contrib import admin
from .models import actor, movie

# Register your models here.

admin.site.register(actor)
admin.site.register(movie)