from django.contrib import admin
from django.contrib.admin import display

from .models import (Favorite, Ingredient, IngredientToRecipe, Recipe,
                     ShoppingCart, Tag, TagToRecipe)


class TagTagAdminInline(admin.TabularInline):
    model = TagToRecipe
    extra = 1


class IngredientTagAdminInLine(admin.StackedInline):
    model = IngredientToRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    readonly_fields = ('fav_recipes',)
    list_filter = ('author', 'name', 'tags')
    inlines = (TagTagAdminInline, IngredientTagAdminInLine)

    @display(description='Количество в избранных')
    def fav_recipes(self, obj):
        return obj.fav_recipe.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(IngredientToRecipe)
class IngredientToRecipe(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(TagToRecipe)
class TagToRecipeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'recipe')
