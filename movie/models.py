from django.db import models

# Create your models here.

class actor(models.Model):
    id = models.CharField(unique=True, primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    birthYear = models.IntegerField()
    deathYear = models.IntegerField()
    movie1 = models.CharField(max_length=100)
    movie2 = models.CharField(max_length=100)
    movie3 = models.CharField(max_length=100)
    movie4 = models.CharField(max_length=100)

    def __str__(self):
        return self.name


