"""
Custom exception handler for better error responses
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def custom_exception_handler(exc, context):
    """
    Custom exception handler for better error responses
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the error response format
        if isinstance(response.data, dict):
            error_data = {
                'error': True,
                'message': response.data.get('detail', 'An error occurred'),
                'code': response.status_code,
                'details': response.data
            }
        else:
            error_data = {
                'error': True,
                'message': str(response.data),
                'code': response.status_code,
                'details': response.data
            }
        response.data = error_data
    
    # Handle Django ValidationError
    elif isinstance(exc, ValidationError):
        error_data = {
            'error': True,
            'message': 'Validation error',
            'code': status.HTTP_400_BAD_REQUEST,
            'details': exc.message_dict if hasattr(exc, 'message_dict') else str(exc)
        }
        response = Response(error_data, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle Django Http404
    elif isinstance(exc, Http404):
        error_data = {
            'error': True,
            'message': 'Resource not found',
            'code': status.HTTP_404_NOT_FOUND,
            'details': 'The requested resource was not found'
        }
        response = Response(error_data, status=status.HTTP_404_NOT_FOUND)
    
    # Handle other exceptions
    elif exc:
        error_data = {
            'error': True,
            'message': 'Internal server error',
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'details': str(exc) if settings.DEBUG else 'An unexpected error occurred'
        }
        response = Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response 