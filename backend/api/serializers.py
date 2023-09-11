from rest_framework.serializers import ModelSerializer

from tag.models import Tag
from ingredient.models import Ingredient


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
