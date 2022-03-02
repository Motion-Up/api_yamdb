from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=200
    )
    slug = models.SlugField(
        'Уник. фрагмент url',
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=200
    )
    slug = models.SlugField(
        'Уник. фрагмент url',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.title


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=200
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManytomanyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
