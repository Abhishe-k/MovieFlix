from django.db import models
from django.contrib.auth.models import User
from django_random_id_model import RandomIDModel
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
    price = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return self.title


class actor(models.Model):
    movieId = models.ForeignKey(movie, on_delete=models.CASCADE, primary_key=True)
    actor1 = models.CharField(max_length=50, null=True)
    actor2 = models.CharField(max_length=50, null=True)
    actor3 = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.movieId.title


class topmovie(models.Model):
    topId = models.ForeignKey(movie, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)

    def __str__(self):
        return str(self.rank)


class profile(models.Model):
    username = models.CharField(default='none', max_length=50, primary_key=True)
    image = models.ImageField(upload_to='profile_images')

    def __str__(self):
        return self.username


class order(RandomIDModel):
    username = models.CharField(max_length=50)
    choices = [('A', 'Approved'), ('P', 'Pending')]
    title = models.CharField(max_length=100)
    ordered_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=choices, default='P')

    def __str__(self):
        return "1)Requested By: "+str(self.username) + " " + "2)Title requested: "+str(self.title) + " "  + "3)Status: "+str(self.status)+ " "  + "4)Request Date: "+str(self.ordered_at)


class Comment(models.Model):
    movie_Id = models.ForeignKey(movie, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    username = models.CharField(max_length=50)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.username)


class usertoken(RandomIDModel):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    requested_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "1)Email:" + self.email + " 2)Username: " + self.username


class userlikes(models.Model):
    movie_id = models.ForeignKey(movie, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    likes = models.BooleanField(default=False)
    movie = models.CharField(max_length=100)

    def __str__(self):
        return 'User {} likes Movie {} : {}'.format(self.username, self.movie_id,self.likes)


class Contact(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name

class MovieOrder(models.Model):
    username = models.CharField(max_length=10)
    movie_Id = models.ForeignKey(movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie_Id.title