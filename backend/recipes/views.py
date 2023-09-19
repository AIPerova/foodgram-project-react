from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientToRecipe, Recipe,
                     ShoppingCart, Tag)
from .permissions import IsAuthorOrReadOnly
from api.pagination import LimitPageNumberPagination
from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                             RecipeShortSerializer, RecipeWriteSerializer,
                             TagSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    '''Вьюсет для ингредиентов.'''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    '''Вьюсет для тегов.'''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    '''Вьюсет для рецептов.'''
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            model.objects.filter(user=user, recipe__id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        '''Метод для добавления,удаления рецепов в избранное.'''
        if request.method == 'POST':
            return self.add_to(Favorite, request.user, pk)
        return self.delete_from(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        '''Метод для добавления удаления рецептов в список покупок.'''
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        return self.delete_from(ShoppingCart, request.user, pk)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        '''Загрузка списка игридиентов для покупок.'''
        ingredients = IngredientToRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount')
        shop_list = {}
        for item in ingredients:
            name = item[0]
            if name not in shop_list:
                shop_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]}
            else:
                shop_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('DejaVuSerif', size=25)
        today = datetime.today()
        page.drawString(100, 700, f'Список покупок на {today:%d.%m}:')
        page.setFont('DejaVuSerif', size=15)
        height = 600
        for i, k in shop_list.items():
            page.drawString(
                50, height,
                (f'{i}  - {k["amount"]} ({k["measurement_unit"]})')
            )
            height -= 20
        page.showPage()
        page.save()
        return response
