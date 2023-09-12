from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from user.models import User


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
        default_related_name = 'ingredients'
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


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
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
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
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe',
            )
        ]

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


class BaseRecipeList(models.Model):
    '''Базовый класс для списка рецептов.'''
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        ordering = ('recipe',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe'
            )
        ]


class Favorite(BaseRecipeList):
    '''Модель избранных рецептов.'''

    class Meta:
        default_related_name = 'fav_recipe'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном {self.user}'


class ShoppingCart(BaseRecipeList):
    '''Модель списка покупок.'''

    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f"Рецепт {self.recipe} в списке покупок {self.user}"
