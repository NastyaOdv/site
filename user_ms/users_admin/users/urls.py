from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, RefreshAPIView
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url

schema_view = get_swagger_view(title='Pastebin API')

app_name = 'authentication'
urlpatterns = [
    path('users/' ,RegistrationAPIView.as_view({
        'post': 'registration',
    })),
    path('users/login/', LoginAPIView.as_view()),
    path('users/refresh/', RefreshAPIView.as_view()),
    path('users/<uuid:uuid>', RegistrationAPIView.as_view({
        'get': 'verify',
    })),
    url(r'^$', schema_view)
]