from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"
    ROLES_CHOICES = (
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
    )
    
    username = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        'Роль',
        choices=ROLES_CHOICES,
        default=USER,
        max_length=50,
        help_text='Пользовательские роли'
    )

    REQUIRED_FIELDS = ['email',]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

def get_tokens_for_user(user) -> str:
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return token['access']

        """return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }"""


class UserAuth(models.Model):
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='auth'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6
    )
    #confirm_code = models.CharField('Код подтверждения', blank=True , default=get_tokens_for_user(username), max_length=150)
    confirm_code = models.CharField('Token', blank=True, max_length=150)

    """def get_tokens_for_user(self) -> str:
        refresh = RefreshToken.for_user(self.pk)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return token['access']

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }"""

    def __str__(self):
        return f'{self.username}={self.confirmation_code}'
