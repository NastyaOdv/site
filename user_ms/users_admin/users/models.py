from django.db import models
import jwt

import hashlib
import os
from datetime import datetime, timedelta
import uuid
from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, username, email, password):

        if  username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField( unique=True)
    password = models.CharField(max_length=200)
    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'email']

    objects = UserManager()
    def __str__(self):
        return self.email
    @property
    def token(self):
        return self._generate_jwt_token()
    @property
    def get_email(self):
        return self.email
    @property
    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username


    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(minutes=15)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())  # CHANGE HERE
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')
