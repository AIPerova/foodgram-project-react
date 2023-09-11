from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, TagViewSet

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag'),
router.register('ingredients', IngredientViewSet, basename='ingredient'),

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    ]
