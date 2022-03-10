from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_moderator = models.BooleanField(
        'moderator status',
        default=False,
        help_text='Указывает является пользователь модераторм',
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField('email address', unique=True)
    password = models.CharField(
        'password',
        max_length=128,
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=20,
        default='user'
    )

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
        super().save(*args, **kwargs)
