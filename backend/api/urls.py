from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredient.views import IngredientViewSet
from tag.views import TagViewSet
# from recipes.views import

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag'),
router.register('ingredients', IngredientViewSet, basename='ingredient'),

urlpatterns = [
    path('v1/', include(router.urls)),
    ]
