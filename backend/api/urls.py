from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag'),
router.register('ingredients', IngredientViewSet, basename='ingredient'),
router.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('user.urls')),
]
