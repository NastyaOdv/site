import pika
import os
import sys
import json
sys.path.append('..')
print(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE','admin_likes.settings')
import django
django.setup()
from django.conf import settings
from likes.serializers import PostSerializers
from likes.models import Post
def callback(ch, method,properties,body):
    if properties.content_type=='create_post':
        serializer = PostSerializers(data=json.loads(body))
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif properties.content_type=='delete_post':
        try:
            post = Post.objects.get(id_post=json.loads(body)["id"])
        except Exception as exp:
            print(exp)
        post.delete()
    print(body)
params=pika.URLParameters(settings.AMQURL)
connection = pika.BlockingConnection(params)
channel = connection.channel()
result = channel.queue_declare(queue='likes',durable=True)
channel.queue_bind(queue='likes',exchange='posts',routing_key='likes')
queue_name = result.method.queue
channel.basic_consume(queue=queue_name,on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()