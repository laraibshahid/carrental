"""
URL patterns for booking management
"""
from django.urls import path
from bookings.views import (
    BookingListView,
    BookingDetailView,
    BookingCancelView,
    BookingConfirmView,
    BookingSearchView
)

app_name = 'bookings'

urlpatterns = [
    # Booking CRUD operations
    path('', BookingListView.as_view(), name='booking-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    
    # Booking actions
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
    path('<int:pk>/confirm/', BookingConfirmView.as_view(), name='booking-confirm'),
    
    # Booking search
    path('search/', BookingSearchView.as_view(), name='booking-search'),
] 