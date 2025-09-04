from django.urls import path
from .views import (
    RegisterView, CustomTokenObtainPairView, ProfileView,
    ImpactEntryListCreateView, ImpactEntryDetailView, ImpactStatsView,
    AISuggestionsView, 
    ChangePasswordView, TestUserView, HealthCheckView, SimpleTestView, 
    PasswordResetRequestView, PasswordResetConfirmView,
    dashboard_view, entries_list_view, stats_view, UserProfileView
)

# Simple logout view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import ImpactEntry

class LogoutView(APIView):
    def post(self, request):
        # Simple logout - just return success
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

urlpatterns = [
    # Health check endpoint
    path('health/', HealthCheckView.as_view(), name='health_check'),
    
    # Simple test endpoint (no auth models dependency)
    path('test-simple/', SimpleTestView.as_view(), name='test_simple'),
    
    # Legacy Authentication Endpoints (for backward compatibility)
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Added missing logout endpoint
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Password Reset Endpoints
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Impact Entry Endpoints
    path('entries/', ImpactEntryListCreateView.as_view(), name='entries'),
    path('entries/<int:pk>/', ImpactEntryDetailView.as_view(), name='entry_detail'),
    path('stats/', ImpactStatsView.as_view(), name='stats'),
    
    # AI Suggestions Endpoints
    path('ai-suggestions/', AISuggestionsView.as_view(), name='ai_suggestions'),
    
    # Test Endpoints
    path('test-user/', TestUserView.as_view(), name='test_user'),
    
    # Legacy Template Views (for backward compatibility)
    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('entries-list/', entries_list_view, name='entries_list_view'),
    path('stats-view/', stats_view, name='stats_view'),

    # User Profile Endpoint
    path('user-profile/', UserProfileView.as_view(), name='user_profile'),
] 