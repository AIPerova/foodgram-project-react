from rest_framework.serializers import ModelSerializer

from recipes.models import Ingredient, Tag


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
