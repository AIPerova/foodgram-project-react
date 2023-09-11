from django.contrib.auth import get_user_model

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from tag.models import Tag
from ingredient.models import Ingredient

User = get_user_model()


class Recipe(models.Model):
    '''Модель для рецепта.'''
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientToRecipe',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagToRecipe',
        verbose_name='Тег'
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/images',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=settings.MAX_LENGTH_NAME
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Не менее одной минуты'),
        ],
    )

    class Meta:
        ordering = ('-id',)
        default_related_name = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientToRecipe(models.Model):
    '''Промежуточная модель отношения рецепта и ингредиента.'''
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredienttorecipe'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Не менее 1 единицы продукта'),
        ],
    )

    class Meta:
        verbose_name = 'ингредиент/рецепт'
        verbose_name_plural = 'Ингредиенты/Рецепты'
        ordering = ('recipe',)

    def __str__(self):
        return f'Для {self.recipe} необходим ингредиент {self.ingredient}'


class TagToRecipe(models.Model):
    '''Промежуточная модель отношения рецепта и тега.'''
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'тег/рецепт'
        verbose_name_plural = 'Теги/Рецепты'

    def __str__(self):
        return f'Рецепт {self.recipe} с тегом {self.tag}'
