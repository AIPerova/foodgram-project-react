from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Модель переопреляющая пользователя.'''
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=settings.MAX_EMAIL_LENGHT,
        unique=True,
    )
    first_name = models.CharField(max_length=settings.MAX_USER_NAME,
                                  blank=True)
    last_name = models.CharField(max_length=settings.MAX_USER_NAME,
                                 blank=True)
    USERNAME_FIELD = 'email'
    LOGIN_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    '''Модель для избранных авторов.'''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Избранный автор',
    )

    class Meta:
        verbose_name = 'избранный автор'
        verbose_name_plural = 'Избранные авторы'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            ),
            models.CheckConstraint(
                name='not_self_follow',
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.author}'
