from django.db import models

# Create your models here.


class movie(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=10)
    title = models.CharField(max_length=100)
    imageUrl = models.URLField()
    director = models.CharField(max_length=100, null=True)
    releaseDate = models.CharField(max_length=100)
    genre1 = models.CharField(max_length=20, null=True)
    genre2 = models.CharField(max_length=20, null=True)
    plot = models.CharField(max_length=100000, null=True)
    rating = models.DecimalField(decimal_places=1, max_digits=3, null=True)
    votes = models.IntegerField(null=True)
    runtime = models.CharField(max_length=3, null=True)
    year = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class actor(models.Model):
    movieId = models.ForeignKey(movie, on_delete=models.CASCADE, primary_key=True)
    actor1 = models.CharField(max_length=50, null=True)
    actor2 = models.CharField(max_length=50, null=True)
    actor3 = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.movieId.title