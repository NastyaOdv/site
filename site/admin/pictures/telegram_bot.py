import telebot
import types
import os
import sys
import json
sys.path.append('..')
print()
os.environ.setdefault('DJANGO_SETTINGS_MODULE','admin_pic.settings')
import django
django.setup()
from django.conf import settings
from pictures.serializers import SubscriberSerializers
from pictures.models import Subscriber
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
print("telegram run")

telegbot=settings.TELEGBOT
bot = telebot.TeleBot(telegbot)
def send_notification(ids,picture):
    ms=f"Новая картинка {picture['title']},{picture['url']}"
    for id in ids:
        bot.send_message(chat_id=id.id,text=ms)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}'
                          )
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, f'Я бот, который отслеживает активность на сайте Pictures. Так сказать бот оповещение'
                          f'/subscribe - подписаться на оповещение'
                          f'/unsubscribe - отписаться')
@bot.message_handler(commands=['subscribe'])
def send_subscribe(message):
    try:
        serializer = SubscriberSerializers(data={"id":message.from_user.id})
        serializer.is_valid(raise_exception=True)
    except Exception:
        bot.send_message(chat_id=message.from_user.id,text="вы уже подписаны")
    else:
        bot.reply_to(message, f'Вы подписались')

        serializer.save()

@bot.message_handler(commands=['unsubscribe'])
def send_welcome(message):
    try:
        subscriber = Subscriber.objects.get(id=message.from_user.id)
    except ObjectDoesNotExist:
        bot.send_message(chat_id=message.from_user.id,text="вы не были подписаны")
    else:
        subscriber.delete()
        return bot.reply_to(message, f'Вы отписались')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')

bot.polling()
