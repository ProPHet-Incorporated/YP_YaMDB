from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import NAME_LENGTH

User = get_user_model()


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=settings.NAME_LENGTH)
    slug = models.SlugField(
        'Адрес',
        max_length=settings.SLUG_LENGTH,
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Categories(models.Model):
    name = models.CharField('Категория', max_length=settings.NAME_LENGTH)
    slug = models.SlugField(
        'Адрес',
        max_length=settings.SLUG_LENGTH,
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField('Название', max_length=settings.NAME_LENGTH)
    year = models.IntegerField('Год')
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.DO_NOTHING
    )
    genre = models.ManyToManyField(Genre, through='TitleGenre')

    class Meta:
        ordering = ('name',)


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(
                1,
                message=(
                    'Введенная оценка ниже допустимой(минимальная оценка 1)'
                )
            ),
            MaxValueValidator(
                10,
                message=(
                    'Введенная оценка выше допустимой(максимальная оценка 10)'
                )
            ),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )

    class Meta:
        unique_together = ('author', 'title')
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:settings.TEXT_SLICE]


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='author',
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('pub_date',)
