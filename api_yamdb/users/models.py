from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    """
    user (default)
    может читать всё,
    может публиковать отзывы,
    ставить оценку,
    комментировать чужие отзывы,
    может редактировать и удалять
    свои отзывы и комментарии.

    Moderator
    те же права, что и у user,
    плюс право удалять любые отзывы и комментарии.

    admin
    полные права на управление всем контентом проекта.
    Может создавать и удалять произведения, категории и жанры.
    Может назначать роли пользователям.
    """
    username = models.CharField(
        'Имя пользователя',
        unique=True,
        help_text=(
            'Обязательное поле. Не более 150 символов.'
            'Только: буквы, цифры и @/./+/-/_'
        ),
        validators=[validate_username],
        max_length=150,
    )
    email = models.EmailField(
        'Email адрес',
        unique=True,
        help_text=('Обязательное поле. Не более 254 символов.'),
        max_length=254,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    role = models.CharField(
        'Роль',
        max_length=50,
        choices=ROLES,
        default=USER,
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
