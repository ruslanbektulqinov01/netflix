from django.db import models

from .movie import Movie


class Actor(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    gender = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie, related_name="actors", blank=True)
