from django.contrib import admin
from django.urls import  path
from .views import PictureViewSet, ArtistViewSet
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')
urlpatterns = [
    path('pictures/',PictureViewSet.as_view({
        'get': 'list_pictures',
        'post': 'create_picture'
    })),
    path('pictures/user/', PictureViewSet.as_view({
        'get': 'list_user_pictures',
    })),
    path('pictures/<int:pk>/' ,PictureViewSet.as_view({
        'get': 'get_picture',
        'delete': 'delete_picture'
    })),

    url(r'^$', schema_view)
]