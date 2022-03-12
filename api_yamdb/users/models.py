from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    ]
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
        choices=USER_ROLE,
        default=USER
    )

    def save(self, *args, **kwargs):
        if self.role == self.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        if self.role == self.ADMIN:
            return True
        return False

    @property
    def is_moderator(self):
        if self.role == self.MODERATOR:
            return True
        return False
