from __future__ import absolute_import
from users_admin.celery import app
from django.core.mail import send_mail
from users_admin.settings import EMAIL_HOST_USER
import os
from django.core.mail import send_mail
os.environ.setdefault('DJANGO_SETTINGS_MODULE','users_admin.settings')

import django
django.setup()
from django.conf import settings
from django.shortcuts import render
import time


@app.task
def longtime_add(email,url):
    subject = 'Welcome to DataFlair'
    message = f'Tap here {url}'
    send_mail(subject,
              message, EMAIL_HOST_USER, [f'{email}'], fail_silently=False)
    return "Ok"
