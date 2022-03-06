from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import password_validation


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

    def save(self, *args, **kwargs):
        if self.is_staff is True:
            self.is_moderator = True
        elif self.is_staff is not True:
            self.is_moderator = False
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
