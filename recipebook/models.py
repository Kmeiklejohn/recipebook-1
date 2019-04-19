from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """update to the model for the favorites"""
    name = models.CharField(max_length=45)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    favorites = models.ManyToManyField('Recipe', related_name='favorites', blank=True)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    time = models.IntegerField()
    instructions = models.TextField()
