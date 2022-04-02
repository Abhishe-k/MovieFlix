from django.contrib import admin
from .models import actor, movie, topmovie, profile, order

# Register your models here.

admin.site.register(actor)
admin.site.register(movie)
admin.site.register(topmovie)
admin.site.register(profile)
admin.site.register(order)