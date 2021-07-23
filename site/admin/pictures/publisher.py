# from kombu import Connection, Exchange, Producer, Queue
import json
import pika
from django.conf import settings

url=settings.AMQURL
connection = pika.BlockingConnection(
    pika.URLParameters(url))
channel = connection.channel()

channel.exchange_declare(exchange='posts',exchange_type='direct')
def publisher(method,body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='posts', routing_key='likes', body=json.dumps(body),properties=properties)
    print(" [x] Sent 'Public'")
def delete_post(id):
    channel.basic_publish(exchange='posts', routing_key='likes', body=json.dumps({"id": id, "method": "delete_post"}))
    print(" [x] Sent 'Delete'")