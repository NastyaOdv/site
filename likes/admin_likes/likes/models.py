from django.db import models
from django.contrib.auth.models import AnonymousUser
class ServerUser(AnonymousUser):
    @property
    def is_authenticated(self):
        return True
class Post(models.Model):
    id = models.PositiveIntegerField(primary_key=True,unique=True)
class Like(models.Model):
    id_post = models.ForeignKey(to=Post,on_delete=models.CASCADE)
    id_user = models.PositiveIntegerField()


