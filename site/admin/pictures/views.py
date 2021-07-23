from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Picture, Artist, Subscriber
from .serializers import PictureSerializers, ArtistSerializers
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication, exceptions
from django.conf import settings
from.publisher import publisher
from .task import send_mes_telegram
import jwt
from rest_framework.generics import GenericAPIView

class PictureViewSet(viewsets.ViewSet,GenericAPIView):
    permission_classes_by_action = {
        'list_pictures': [AllowAny],
        'get_picture': [AllowAny],
        'default': [IsAuthenticated]
    }
    serializer_class=PictureSerializers
    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes_by_action['default']]

    def list_pictures(self, request):
        pictures = Picture.objects.all()
        serializer = self.serializer_class(pictures, many=True)
        return Response(serializer.data)
    def create_picture(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY,algorithms="HS256")

        request.data.update({"id_user":payload["id"]})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publisher("create_post",{"id":serializer.data["id"]})
        send_mes_telegram(Subscriber.objects.all(),serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_picture(self,request,pk=None):
        try:
            picture = Picture.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(picture)
        return Response(serializer.data)
    def delete_picture(self, request, pk=None):
        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY,algorithms="HS256")
        try:
            picture = Picture.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if picture.id_user == payload['id']:
            picture.delete()
            publisher("delete_post",{"id":picture.id})
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def list_user_pictures(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        pictures = Picture.objects.filter(id_user=payload['id'])
        serializer = self.serializer_class(pictures, many=True)
        return Response(serializer.data)

class ArtistViewSet(viewsets.ViewSet):
    def list_artists(self, request):
        pictures = Artist.objects.all()
        serializer = ArtistSerializers(pictures, many=True)
        return Response(serializer.data)

    def create_artist(self, request):
        serializer = ArtistSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_artist(self, request, pk=None):
        try:
            picture = Artist.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ArtistSerializers(picture)
        return Response(serializer.data)

    def delete_artist(self, request, pk=None):
        try:
            picture = Artist.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# Create your views here.
# {
#    "url":"https://st2.depositphotos.com/1064024/10769/i/600/depositphotos_107694484-stock-photo-little-boy.jpg",
#    "title":"some",
#    "timePost":"2002-01-02 00:00:00"
#
# }