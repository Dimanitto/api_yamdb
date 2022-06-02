from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import SignUpSerializer, GetTokenSerializer
from reviews.models import User, UserAuth
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.core.exceptions import PermissionDenied


class SignUpCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


"""class GetToken(TokenObtainPairView):
    queryset = UserAuth.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer"""


def get_tokens_for_user(user) -> str:
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return token['access']


class GetToken(generics.CreateAPIView):
    queryset = UserAuth.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer

    def perform_update(self, serializer):
        if user := UserAuth.objects.get(username=self.username):
            print(user,'-------------------------------------------------')
            user.confirm_code = get_tokens_for_user(user)
            #user.confirm_code = user.get_tokens_for_user()
            user.save(update_fields=["confirm_code"])
            serializer.save()
            #user = serializer.save()
        else:
            raise PermissionDenied('Изменение чужого контента запрещено!')

    """def perform_create(self, serializer):
        if user := UserAuth.objects.get(username=serializer.username):
            token = get_tokens_for_user(user)
            print(token['access'])
        serializer.save(username=serializer.username)"""

#class GetToken(generics.CreateAPIView):
    ...


def send_message(email: str, username: str) -> None:
    """Отправка кода подтверждения на почту."""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    # Сгенерируем код активации
    secret_key = get_random_string(6, chars)

    print(username)
    user = User.objects.get(username=username)
    print(user.pk)
    UserAuth.objects.create(
        username_id=user.pk,
        confirmation_code=secret_key
    )

    print(UserAuth.objects.all())

    send_mail(
            'Авторизация на сайтe',
            (f'Уважаемый {username}, '
            f'Kод подтверждения = {secret_key}'),
            'yamdb@yandex.ru',  # Это поле "От кого"
            [email],  # Это поле "Кому"
    )


"""def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }"""
