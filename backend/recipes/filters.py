from django.db.models import Q
from django_filters.rest_framework import FilterSet, filters

from .models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    '''Поиск игредиента на началу названия.'''
    name = filters.CharFilter(
        field_name='name', method='get_name_or_contains'
    )

    def get_name_or_contains(self, queryset, name, value):
        return queryset.filter(
            Q(name__istartswith=value) | Q(name__icontains=value)
        ).distinct()

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    '''Фильтрация рецептов.'''
    # tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(fav_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
