from django.contrib import admin
from django.urls import  path
from .views import LikeViewSet
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('likes/',LikeViewSet.as_view({
        'get': 'list_likes',
        'post': 'create_like'
    })),
    path('likes/<int:id_post>/' ,LikeViewSet.as_view({
        'get': 'get_like',
        'delete': 'delete_like'
    })),
url(r'^$', schema_view)
]