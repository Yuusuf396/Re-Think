from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """Custom exception handler to ensure all responses are JSON"""
    
    # Call the default exception handler
    response = exception_handler(exc, context)
    
    if response is None:
        # If DRF didn't handle it, create a JSON response
        return Response({
            'error': str(exc),
            'detail': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Ensure the response is JSON
    if not isinstance(response.data, dict):
        response.data = {
            'error': str(response.data),
            'detail': 'An error occurred'
        }
    
    return response 