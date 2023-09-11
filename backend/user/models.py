from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Модель переопреляющая пользователя.'''
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    email = models.EmailField(
        'email address',
        max_length=settings.MAX_EMAIL_LENGHT,
        unique=True,
    )

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
        related_name='follower',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Избранный автор',
    )

    class Meta:
        verbose_name = 'избранный автор'
        verbose_name_plural = 'Избранные авторы'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
                violation_error_message='За этим автором уже следим!'
            ),
            models.CheckConstraint(
                name='not_self_follow',
                check=~models.Q(user=models.F('author')),
                violation_error_message='Никаких самоподписок!'
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.author}'
