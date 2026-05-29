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

# The Recipe model represents a structured dish (e.g., Spaghetti, Tacos)
class Recipe(models.Model):
    # The title field stores the name of the dish
    title = models.CharField(
        max_length=200 # Set a max length of 200 characters for the recipe title
    )
    # The instructions field stores step-by-step preparation guidelines
    instructions = models.TextField()
    
    # The cuisine field links this recipe to a specific style of cooking
    # ForeignKey creates a One-to-Many relationship (each recipe has one cuisine)
    # on_delete=models.CASCADE means if a cuisine is deleted, all its recipes are deleted too
    cuisine = models.ForeignKey(
        Cuisine, 
        on_delete=models.CASCADE,
        related_name='recipes' # Allows us to fetch all recipes of a cuisine using cuisine.recipes.all()
    )
    
    # The ingredients field links this recipe to multiple pantry items
    # ManyToManyField creates a join table connecting recipes and ingredients together
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes' # Allows us to fetch all recipes containing an ingredient using ingredient.recipes.all()
    )

    # The __str__ method defines how this model displays as a simple string representation
    def __str__(self):
        # We return the title field when printing the recipe object
        return self.title


# The Review model represents a cooking tip or review left for a specific recipe
class Review(models.Model):
    # The tip field stores the user's cooking tip or review comment text
    # TextField allows for long, multi-line blocks of text
    tip = models.TextField()

    # The created_at field records exactly when the review was created in the database
    # auto_now_add=True automatically sets the current date and time when the row is first created
    created_at = models.DateTimeField(auto_now_add=True)

    # The recipe field links this review to a specific recipe in our database
    # ForeignKey creates a One-to-Many relationship (each recipe can have many reviews)
    # on_delete=models.CASCADE means if a recipe is deleted, all reviews for that recipe are deleted too
    # related_name='reviews' allows us to fetch all reviews of a recipe using recipe.reviews.all()
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    # The __str__ method defines how this model displays as a simple string representation
    def __str__(self):
        # We show a preview of the tip (first 30 characters) and which recipe it is for
        return f"Tip for '{self.recipe.title}': {self.tip[:30]}..."



