from __future__ import absolute_import
from celery import Celery
from django.conf import settings
app = Celery('users_admin',
             broker=settings.AMQURL,
             backend='rpc://',
             include=['users.task'])

