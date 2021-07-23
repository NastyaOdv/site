from rest_framework import status , authentication,viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
import jwt
from django.conf import settings
from .serializers import RegistrationSerializer, LoginSerializer, RefreshSerializer
from .renderers import UserJSONRenderer
from .task import longtime_add
from os import path
from .models import User
from django.http import Http404


class RegistrationAPIView(viewsets.ViewSet,GenericAPIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def registration(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user2 = User.objects.get(pk=serializer.data.get('id'))
        A = [request.get_host(),"api","users",str(user2.verification_uuid)]
        result = longtime_add.delay(user2.email, " http://"+"/".join(A))
        result.wait()
        print(result.result)
        return Response({"result":"email send"}, status=status.HTTP_201_CREATED)

    def verify(self,request, uuid):
        try:
            user = User.objects.get(verification_uuid=uuid, is_verified=False)
        except User.DoesNotExist:
            return Response({"error": "User does not exist or is already verified"}, status=status.HTTP_404_NOT_FOUND)
        user.is_verified = True
        user.save()
        serializer= self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
# Create your views here.
class RefreshAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RefreshSerializer

    def get(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"], options={"verify_exp":False})
        print(payload)
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)