from django.conf import settings
from django.db import models


class Ingredient(models.Model):
    '''Модель для ингредиентов.'''
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=settings.MAX_LENGTH_NAME
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения ингредиента',
        max_length=settings.MAX_LENGTH_NAME
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'ingredient'
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
