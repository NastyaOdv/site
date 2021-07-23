from rest_framework import  serializers
from .models import Picture, Artist,  Subscriber
class PictureSerializers(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
class ArtistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'
class SubscriberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'