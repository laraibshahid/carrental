"""
URL patterns for user authentication and profile management
"""
from django.urls import path
from users.views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    ChangePasswordView,
    LogoutView,
    RefreshTokenView
)

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    
    # Profile management
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
] 