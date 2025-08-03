"""
URL patterns for vehicle management
"""
from django.urls import path
from vehicles.views import (
    VehicleListView,
    VehicleDetailView,
    VehicleSearchView
)

app_name = 'vehicles'

urlpatterns = [
    # Vehicle CRUD operations
    path('', VehicleListView.as_view(), name='vehicle-list'),
    path('<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    
    # Vehicle search
    path('search/', VehicleSearchView.as_view(), name='vehicle-search'),
] 