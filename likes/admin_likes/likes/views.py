from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Like
from .serializers import LikeSerializers
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication, exceptions
from rest_framework.generics import GenericAPIView
from django.conf import settings
import jwt

class LikeViewSet(viewsets.ViewSet,GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializers
    def list_likes(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY)
        print(payload['id'])
        likes = Like.objects.filter(id_user=payload['id'])
        serializer = self.serializer_class(likes, many=True)
        return Response(serializer.data)
    def create_like(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY)
        try:
            Like.objects.get(id_user=payload['id'],id_post=request.data['id_post'])

        except ObjectDoesNotExist:
            serializer = self.serializer_class(data={"id_user":payload["id"],"id_post":request.data["id_post"]})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error":"like already exist"},status.HTTP_400_BAD_REQUEST)
    def get_like(self,request,id_post=None):
        try:
            auth_header = authentication.get_authorization_header(request).split()
            token = auth_header[1].decode('utf-8')
            payload = jwt.decode(token, settings.SECRET_KEY)
            like = Like.objects.get(id_post=id_post,id_user=payload['id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(like)
        return Response(serializer.data)
    def delete_picture(self, request, id_post=None):
        try:
            auth_header = authentication.get_authorization_header(request).split()
            token = auth_header[1].decode('utf-8')
            payload = jwt.decode(token, settings.SECRET_KEY)
            like = Like.objects.get(id_post=id_post,id_user=payload['id'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

