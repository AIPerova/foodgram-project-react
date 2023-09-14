from django.contrib import admin

from .models import (Favorite,
                     Ingredient,
                     IngredientToRecipe,
                     Tag,
                     TagToRecipe,
                     Recipe,
                     ShoppingCart
                     )

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(TagToRecipe)
admin.site.register(IngredientToRecipe)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
