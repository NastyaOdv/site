from django.db import models
from django.db import models
from django.contrib.auth.models import AnonymousUser

class ServerUser(AnonymousUser):
    @property
    def is_authenticated(self):
        return True

class Artist(models.Model):
    url_ava = models.URLField()
    name = models.CharField(max_length=200)
    secondName = models.CharField(max_length=200)
    birthday = models.DateField()


class Picture(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200)
    timePost = models.DateTimeField()
    id_user = models.PositiveIntegerField()

class Subscriber(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)


