from rest_framework import  serializers
from .models import Like, Post
class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
