# We import the APIView base class from rest_framework.views to build custom class-based endpoints
from rest_framework.views import APIView
# We import the Response class to wrap and send standard JSON responses back to the client
from rest_framework.response import Response
# We import status codes to return standard HTTP status responses (like 201 Created, 400 Bad Request)
from rest_framework import status
# We import our database models from the local models.py file
from .models import Cuisine, Ingredient
# We import our serializers from the local serializers.py file
from .serializers import CuisineSerializer, IngredientSerializer

# CuisineListAPIView handles the /api/cuisines/ endpoint for listing and creating cuisines
class CuisineListAPIView(APIView):
    
    # get handles incoming HTTP GET requests to fetch all cuisines in the database
    def get(self, request):
        # Fetch all cuisine objects from our database using raw Django ORM query: objects.all()
        cuisines = Cuisine.objects.all()
        # Pass the queryset to the CuisineSerializer, setting many=True because we are serializing a list of items
        serializer = CuisineSerializer(cuisines, many=True)
        # Return the serialized data in a Response wrapper, which automatically handles conversion to JSON (defaults to 200 OK)
        return Response(serializer.data)

    # post handles incoming HTTP POST requests to create a new cuisine in the database
    def post(self, request):
        # Instantiate the serializer with the incoming JSON data from request.data
        serializer = CuisineSerializer(data=request.data)
        # Check if the incoming data is valid (e.g., checks max length, non-empty, and unique constraints)
        if serializer.is_valid():
            # Save the new cuisine record directly to the database
            serializer.save()
            # Return the created cuisine JSON along with a standard 201 Created status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If validation fails, return the validation errors and a 400 Bad Request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# IngredientListAPIView handles the /api/ingredients/ endpoint for listing and creating ingredients
class IngredientListAPIView(APIView):
    
    # get handles incoming HTTP GET requests to fetch all ingredients in the database
    def get(self, request):
        # Fetch all ingredient objects from our database using raw Django ORM query: objects.all()
        ingredients = Ingredient.objects.all()
        # Pass the queryset to the IngredientSerializer, setting many=True because we are serializing a list of items
        serializer = IngredientSerializer(ingredients, many=True)
        # Return the serialized data in a Response wrapper (defaults to 200 OK)
        return Response(serializer.data)

    # post handles incoming HTTP POST requests to create a new ingredient in the database
    def post(self, request):
        # Instantiate the serializer with the incoming JSON data from request.data
        serializer = IngredientSerializer(data=request.data)
        # Check if the incoming data is valid according to our model field constraints
        if serializer.is_valid():
            # Save the new ingredient record directly to the database
            serializer.save()
            # Return the created ingredient JSON along with a standard 201 Created status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If validation fails, return the validation errors and a 400 Bad Request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

