from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','admin_pic.settings')

import django
django.setup()
app = Celery('admin_pic',
             broker=settings.AMQURL,
             backend='rpc://',
             include=['pictures.task'])

