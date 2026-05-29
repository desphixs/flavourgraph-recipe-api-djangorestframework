# We import the models module from django.db, which provides the tools to create database tables
from django.db import models

# The Cuisine model represents a style of cooking (e.g., Italian, Mexican)
class Cuisine(models.Model):
    # The name field stores the name of the cuisine (e.g., "Italian")
    # CharField represents a short text string in the database
    name = models.CharField(
        max_length=100, # Limit the cuisine name to 100 characters max
        unique=True     # Ensure each cuisine name is registered only once to avoid duplicates
    )

    # The __str__ method defines how this model displays as a simple string representation
    def __str__(self):
        # We return the name field when printing the cuisine object
        return self.name

# The Ingredient model represents a raw item used in cooking (e.g., Tomato, Garlic)
class Ingredient(models.Model):
    # The name field stores the name of the ingredient (e.g., "Tomato")
    name = models.CharField(
        max_length=100, # Limit the ingredient name to 100 characters max
        unique=True     # Ensure each ingredient name is registered only once
    )

    # The __str__ method defines how this model displays as a simple string representation
    def __str__(self):
        # We return the name field when printing the ingredient object
        return self.name

