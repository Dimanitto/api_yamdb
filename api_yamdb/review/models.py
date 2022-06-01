from django.db import models
from django.core.validators import (
    RegexValidator, MinValueValidator, MaxValueValidator)

from datetime import datetime


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
