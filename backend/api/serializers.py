from django.db.models import F

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from drf_extra_fields.fields import Base64ImageField


from recipes.models import Ingredient, Recipe, Tag


class UserSerializer(ModelSerializer):
    pass


class IngredientSerializer(ModelSerializer):
    '''Сериализатор для ингредиентов.'''
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(ModelSerializer):
    '''Сериализатор для тегов.'''
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeShortSerializer(ModelSerializer):
    '''Сериализатор для вывода краткого содержания рецепта.'''
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeReadSerializer(ModelSerializer):
    '''Сериализатор для просмотра рецептов.'''
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredienttorecipe__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.fav_recipe.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class RecipeWriteSerializer(ModelSerializer):
    pass