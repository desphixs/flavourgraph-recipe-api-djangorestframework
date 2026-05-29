# We import the APIView base class from rest_framework.views to build custom class-based endpoints
from rest_framework.views import APIView
# We import the Response class to wrap and send standard JSON responses back to the client
from rest_framework.response import Response
# We import status codes to return standard HTTP status responses (like 201 Created, 400 Bad Request)
from rest_framework import status
# We import the standard PageNumberPagination class to handle pagination cleanly
from rest_framework.pagination import PageNumberPagination
# We import our database models from the local models.py file
from .models import Cuisine, Ingredient, Recipe
# We import our serializers from the local serializers.py file
from .serializers import CuisineSerializer, IngredientSerializer, RecipeSerializer

# We create a custom pagination class to define pagination settings for recipes
class RecipePagination(PageNumberPagination):
    # Set the default number of items to show per page
    page_size = 10
    # Enable users to ask for a custom page size using a query parameter (e.g. ?page_size=5)
    page_size_query_param = 'page_size'
    # Cap the maximum number of items a user can ever request per page
    max_page_size = 50


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

# RecipeListAPIView handles the /api/recipes/ endpoint for listing and creating recipes
class RecipeListAPIView(APIView):
    
    # get handles incoming HTTP GET requests to fetch all recipes with standard pagination metadata
    def get(self, request):
        # Fetch all recipe objects from our database using raw Django ORM query: objects.all()
        # We order by ID to ensure consistent, stable pagination slices across requests
        recipes = Recipe.objects.all().order_by('id')
        
        # Get the search term for specific ingredients from request query parameters (e.g. ?ingredient=tomato)
        ingredient_param = request.query_params.get('ingredient')
        
        # If the search parameter was provided by the user:
        if ingredient_param:
            # We filter the recipe queryset to only return recipes that contain this ingredient
            # We use the double-underscore join (ingredients__name__icontains) to query the related Ingredient name case-insensitively
            # We use distinct() to prevent duplicate recipe entries in the results list if multiple ingredients match the query
            recipes = recipes.filter(ingredients__name__icontains=ingredient_param).distinct()
            
        # Create an instance of our custom RecipePagination page slicer
        paginator = RecipePagination()
        
        # Tell the paginator to slice our queryset based on the request URL query parameters
        page = paginator.paginate_queryset(recipes, request, view=self)
        
        # If pagination successfully sliced the list:
        if page is not None:
            # Serialize only the sliced page, not the entire database list!
            serializer = RecipeSerializer(page, many=True)
            # Return a special paginated response that automatically embeds standard links and count metadata
            return paginator.get_paginated_response(serializer.data)
            
        # Fallback: if pagination is disabled or fails, serialize all recipes and return them directly
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    # post handles incoming HTTP POST requests to manually create a new recipe and set its relationships
    def post(self, request):
        # Extract the basic title string from the incoming POST payload data
        title = request.data.get('title')
        # Extract the instructions text from the incoming POST payload data
        instructions = request.data.get('instructions')
        # Extract the cuisine ID integer from the incoming POST payload data
        cuisine_id = request.data.get('cuisine')
        # Extract the list of ingredient ID numbers from the incoming POST payload data
        ingredient_ids = request.data.get('ingredients', [])

        # Validate that all required properties were sent in the request, returning a clean 400 Bad Request error if missing
        if not title or not instructions or not cuisine_id:
            return Response(
                {"error": "Title, instructions, and cuisine fields are all required!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Attempt to retrieve the linked Cuisine object from the database using its ID
        try:
            # We query the database to find the single Cuisine record matching our cuisine_id
            cuisine = Cuisine.objects.get(id=cuisine_id)
        except Cuisine.DoesNotExist:
            # If no Cuisine matches the ID, we return a helpful validation error response
            return Response(
                {"error": f"Cuisine with ID {cuisine_id} does not exist!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the new Recipe instance in the database using raw ORM create commands
        recipe = Recipe.objects.create(
            title=title,
            instructions=instructions,
            cuisine=cuisine
        )

        # Check if the user passed an ingredients list in their payload
        if ingredient_ids:
            # Fetch all Ingredient objects whose IDs match the numbers in our ingredient_ids list
            # We use the __in operator to perform an SQL matching query: SELECT * WHERE id IN (...)
            ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
            # Use the .set() manager to pair the fetched ingredients to our recipe in the M2M join table
            recipe.ingredients.set(ingredients)

        # Pass the completed, saved recipe object to our serializer to output the nested JSON format
        serializer = RecipeSerializer(recipe)
        # Return the beautiful serialized object to the user along with a standard 201 Created status code
        return Response(serializer.data, status=status.HTTP_201_CREATED)



