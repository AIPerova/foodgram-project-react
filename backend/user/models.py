from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
