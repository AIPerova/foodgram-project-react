from django_filters.rest_framework import FilterSet, filters

from .models import Ingredient


class IngredientFilter(FilterSet):
    '''Поиск игредиента на началу названия.'''
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']
