from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import (
    RegexValidator, MinValueValidator, MaxValueValidator)

from datetime import datetime


User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(datetime.now().year)]
    )
    description = models.CharField(blank=True, max_length=256)
    genre = models.ManyToManyField(
        'Genre',
        through='TitleGenre',
        related_name='titles'
    )
    category = models.ManyToManyField(
        'Category',
        through='TitleCategory',
        related_name='category'
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )


class TitleCategory(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимые значения 1-10'),
            MaxValueValidator(10, 'Допустимые значения 1-10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)
