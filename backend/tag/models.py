from django.conf import settings
from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    '''Модель тегов.'''
    name = models.CharField(
        verbose_name='Название тега',
        max_length=settings.MAX_LENGTH_NAME
    )
    color = ColorField(
        verbose_name='Цвет тега',
        format='hex',
        max_length=settings.MAX_LENGHT_COLOR
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор тега'
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'tags'
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
