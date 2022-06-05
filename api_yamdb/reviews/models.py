from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"
    ROLES_CHOICES = (
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
    )

    username = models.CharField(max_length=150, unique=True)
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

    REQUIRED_FIELDS = ['email', ]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


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

    def __str__(self):
        return f'{self.username}={self.confirmation_code}'
