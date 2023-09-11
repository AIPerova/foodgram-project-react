from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientFilter
from .models import Ingredient


class IngredientViewSet(ReadOnlyModelViewSet):
    '''Класс для ингредиентов.'''
    queryset = Ingredient.objects.all()
    # serializer_class = IngredientSerializers
    # permission_classes
    filter_backends = (DjangoFilterBackend,)
    filter = IngredientFilter
