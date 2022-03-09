from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # is_moderator = models.BooleanField(
    #     'moderator status',
    #     default=False,
    #     help_text='Указывает является пользователь модераторм',
    # )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'роль',
        max_length=100,
        choices=[
            ('user', 'User'),
            ('admin', 'Admin'),
            ('moderator', 'Moderator'),
        ],
        blank=True
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

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    # def save(self, *args, **kwargs):
    #     if self.is_admin:
    #         return self.role == 'admin'
    #     elif self.is_moderator:
    #         return self.role == 'moderator'
    #     elif self.is_user:
    #         return self.role == 'user'
    #     super().save(*args, **kwargs)
    #     if self._password is not None:
    #         password_validation.password_changed(self._password, self)
    #         self._password = None
