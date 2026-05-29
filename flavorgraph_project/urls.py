"""
URL configuration for flavorgraph_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# We import path and include from django.urls to route our web pages
from django.urls import path, include

# This list holds the core entry points for our entire Django project.
urlpatterns = [
    # The default administrative panel provided by Django
    path('admin/', admin.site.urls),
    # This redirects all web requests that start with 'api/' into our custom recipes app's URL settings.
    # include() works like a portal, passing the rest of the URL to recipes.urls to handle!
    path('api/', include('recipes.urls')),
]
