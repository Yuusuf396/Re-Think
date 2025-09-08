"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def test_view(request):
    """Simple test view to debug 400 errors"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Backend is working!',
        'allowed_hosts': request.get_host(),
        'debug': request.META.get('DEBUG', 'False')
    })

def db_test_view(request):
    """Test database connection and tables"""
    try:
        from django.db import connection
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_connected = True
            
        # Test if auth_user table exists
        try:
            user_count = User.objects.count()
            auth_table_exists = True
        except Exception as e:
            auth_table_exists = False
            user_count = 0
            
        # Test if our app table exists
        try:
            from tracker.models import ImpactEntry
            entry_count = ImpactEntry.objects.count()
            tracker_table_exists = True
        except Exception as e:
            tracker_table_exists = False
            entry_count = 0
            
        return JsonResponse({
            'status': 'ok',
            'database': {
                'connected': db_connected,
                'auth_user_table_exists': auth_table_exists,
                'tracker_table_exists': tracker_table_exists,
                'user_count': user_count,
                'entry_count': entry_count
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)

class LogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('tracker.urls')),
    path('test/', test_view, name='test'),
    path('', test_view, name='root'),
    path('db-test/', db_test_view, name='db_test'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Commented out email-related views
    # path('api/v1/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    # path('api/v1/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('api/v1/email-verification/', EmailVerificationView.as_view(), name='email_verification'),
    # path('api/v1/email-verification/confirm/', EmailVerificationConfirmView.as_view(), name='email_verification_confirm'),
    # path('api/v1/email-test/', EmailTestView.as_view(), name='email_test'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
