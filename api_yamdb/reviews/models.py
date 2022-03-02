from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=200
    )
    slug = models.SlugField(
        'Уник. фрагмент url',
        unique=True,
        db_index=True
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
        unique=True,
        db_index=True
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        max_length=200,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        max_length=200,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст отзыва',
                            help_text="Введите текст отзыва",
                            )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата публикации'
                                   )
    rating = models.IntegerField(
        choices=list(zip(range(1, 11), range(1, 11))),
        unique=True,
        default=1
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(
            fields=['author', 'title'],
            name='unique_review'
        )]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        max_length=200,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        max_length=200,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария',
                            help_text="Введите текст комментария",
                            )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата публикации'
                                   )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
