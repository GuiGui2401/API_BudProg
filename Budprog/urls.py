"""
Definition of urls for Budprog.
"""
from django.urls import path, include
from django.contrib import admin




urlpatterns = [
    path('api/', include('api.urls', namespace='api_route')),
    path('admin/', admin.site.urls),
]