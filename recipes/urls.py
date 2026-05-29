from django.urls import path
# We import path from django.urls to define URL routes for our API

# We import the views we created so we can map them to specific web addresses
from .views import CuisineListAPIView, IngredientListAPIView, RecipeListAPIView

# This list holds all the URL patterns/routes for the recipes application.
urlpatterns = [
    # Map the address '/api/cuisines/' to the CuisineListAPIView view class
    # .as_view() is a built-in DRF function that configures our class-based view to listen for web requests
    path('cuisines/', CuisineListAPIView.as_view(), name='cuisine-list'),
    
    # Map the address '/api/ingredients/' to the IngredientListAPIView view class
    path('ingredients/', IngredientListAPIView.as_view(), name='ingredient-list'),
    
    # Map the address '/api/recipes/' to the RecipeListAPIView view class
    path('recipes/', RecipeListAPIView.as_view(), name='recipe-list'),
]


