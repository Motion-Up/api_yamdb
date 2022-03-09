from django.contrib.auth import password_validation
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
    confirmation_code = models.CharField(
        'confirmation code',
        max_length=128,
        blank=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=20,
        default='user'
    )

    def save(self, *args, **kwargs):
        if self.is_staff is True:
            self.is_moderator = True
        elif self.is_staff is not True:
            self.is_moderator = False
        if self.is_staff is True:
            self.role = 'admin'
        elif self.is_moderator is True:
            self.role = 'moderator'
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
