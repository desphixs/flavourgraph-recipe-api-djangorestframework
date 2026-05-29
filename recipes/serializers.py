# We import the serializers module from django rest framework to convert our database records to and from JSON format
from rest_framework import serializers
# We import our Cuisine and Ingredient models to link them with our serializers
from .models import Cuisine, Ingredient

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
