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

    def save(self, *args, **kwargs):
        if self.is_staff is True:
            self.is_moderator = True
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
