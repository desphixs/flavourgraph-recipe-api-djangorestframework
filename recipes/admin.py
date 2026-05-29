# We import the admin module from django.contrib to register our models in the administration panel
from django.contrib import admin
# We import our Cuisine, Ingredient, Recipe, and Review models from the current directory's models.py file
from .models import Cuisine, Ingredient, Recipe, Review

# Register the Cuisine model so it shows up in the admin control board for creation and management
@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    # list_display defines which fields are visible in the admin list view
    list_display = ('id', 'name')

# Register the Ingredient model so it shows up in the admin control board for creation and management
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    # list_display defines which fields are visible in the admin list view
    list_display = ('id', 'name')

# Register the Recipe model so it shows up in the admin control board for creation and management
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # list_display defines which fields are visible in the admin list view
    list_display = ('id', 'title', 'cuisine')

# Register the Review model so it shows up in the admin control board for creation and management
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # list_display defines which fields are visible in the admin list view
    list_display = ('id', 'recipe', 'tip', 'created_at')


