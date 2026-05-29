# We import the serializers module from django rest framework to convert our database records to and from JSON format
from rest_framework import serializers
# We import our Cuisine, Ingredient, and Recipe models to link them with our serializers
from .models import Cuisine, Ingredient, Recipe

# CuisineSerializer handles mapping the Cuisine database fields to JSON text
class CuisineSerializer(serializers.ModelSerializer):
    # The Meta class defines instructions for the ModelSerializer
    class Meta:
        # We specify the model this serializer is linked to
        model = Cuisine
        # We list all the fields we want to expose in our API: id and name
        fields = ['id', 'name']

# IngredientSerializer handles mapping the Ingredient database fields to JSON text
class IngredientSerializer(serializers.ModelSerializer):
    # The Meta class defines instructions for the ModelSerializer
    class Meta:
        # We specify the model this serializer is linked to
        model = Ingredient
        # We list all the fields we want to expose in our API: id and name
        fields = ['id', 'name']

# RecipeSerializer maps the Recipe database fields, nesting the related cuisine and ingredients in detail
class RecipeSerializer(serializers.ModelSerializer):
    # We override the cuisine field to return its full serialized details rather than just its numeric database ID
    # read_only=True ensures this detailed nesting is strictly used for outputting (reading) data
    cuisine = CuisineSerializer(read_only=True)
    
    # We override the ingredients field to return a list of full serialized details rather than a list of ID numbers
    # many=True signals that a recipe contains multiple ingredients (a list of objects)
    # read_only=True ensures this nested mapping is strictly used for outputting (reading) data
    ingredients = IngredientSerializer(many=True, read_only=True)

    # The Meta class defines instructions for the ModelSerializer
    class Meta:
        # We link this serializer to our Recipe model blueprint
        model = Recipe
        # We specify the exact fields to map to JSON: id, title, instructions, cuisine, and ingredients
        fields = ['id', 'title', 'instructions', 'cuisine', 'ingredients']

