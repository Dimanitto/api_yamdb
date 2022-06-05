from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import User, UserAuth

from .permissions import IsAdmin
from .serializers import (GetTokenSerializer, SignUpSerializer,
                          UserProfileSerializer, UserSerializer)


class SignUpCreate(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirm_code = serializer.validated_data['confirmation_code']
    username = serializer.validated_data['username']
    if (
        confirm_code == UserAuth.objects.get(
            username__username=username
        ).confirmation_code
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(
        {'Ошибка': 'Некорректно указано поле'},
        status=status.HTTP_400_BAD_REQUEST
    )


def send_message(email: str, username: str) -> None:
    """Отправка кода подтверждения на почту."""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    # Сгенерируем код активации
    secret_key = get_random_string(6, chars)
    user = User.objects.get(username=username)

    UserAuth.objects.create(
        username_id=user.pk,
        confirmation_code=secret_key
    )

    send_mail(
        'Авторизация на сайтe',
        (f'Уважаемый {username}, '
         f'Kод подтверждения = {secret_key}'),
        'yamdb@yandex.ru',  # Это поле "От кого"
        [email],  # Это поле "Кому"
    )


class UserProfileViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=UserProfileSerializer
    )
    def user_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True,   # частичное обновление полей
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'Ошибка': 'Некорректно указано поле'},
            status=status.HTTP_400_BAD_REQUEST
        )
