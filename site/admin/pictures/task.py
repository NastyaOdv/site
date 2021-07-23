from __future__ import absolute_import

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','admin_pic.settings')

import django
django.setup()
from django.conf import settings
from django.shortcuts import render

from admin_pic.celery import app
from .telegram_bot import send_notification

@app.task
def send_mes_telegram(ids,pictures):
    print("Hello Mother")
    send_notification(ids,pictures)
    return "Ok"
