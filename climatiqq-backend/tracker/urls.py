from django.urls import path
from .views import (
    RegisterView, CustomTokenObtainPairView, ProfileView,
    ImpactEntryListCreateView, ImpactEntryDetailView, ImpactStatsView,
    AISuggestionsView, ChatGPTSuggestionsView, 
    # PasswordResetRequestView,  # Disabled
    # PasswordResetConfirmView,  # Disabled
    # EmailVerificationView,  # Disabled
    # EmailVerificationConfirmView,  # Disabled
    ChangePasswordView, TestUserView, HealthCheckView, SimpleTestView, 
    # EmailTestView,  # Disabled
    dashboard_view, entries_list_view, stats_view
)
# Temporarily comment out auth_views to isolate the issue
# from .auth_views import (
#     EnhancedRegisterView, EnhancedLoginView, EnhancedPasswordChangeView,
#     EnhancedPasswordResetRequestView, EnhancedPasswordResetConfirmView,
#     UserProfileView, LogoutView, SecurityLogView
# )

# Simple logout view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogoutView(APIView):
    def post(self, request):
        # Simple logout - just return success
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

urlpatterns = [
    # Health check endpoint
    path('health/', HealthCheckView.as_view(), name='health_check'),
    
    # Simple test endpoint (no auth models dependency)
    path('test-simple/', SimpleTestView.as_view(), name='test_simple'),
    
    # Email test endpoint
    # path('test-email/', EmailTestView.as_view(), name='test_email'), # Disabled
    
    # Temporarily comment out enhanced auth endpoints
    # # Enhanced Authentication Endpoints
    # path('auth/register/', EnhancedRegisterView.as_view(), name='enhanced_register'),
    # path('auth/login/', EnhancedLoginView.as_view(), name='enhanced_login'),
    # path('auth/logout/', LogoutView.as_view(), name='enhanced_logout'),
    # path('auth/password/change/', EnhancedPasswordChangeView.as_view(), name='enhanced_password_change'),
    # path('auth/password/reset/', EnhancedPasswordResetRequestView.as_view(), name='enhanced_password_reset'),
    # path('auth/password/reset/confirm/', EnhancedPasswordResetConfirmView.as_view(), name='enhanced_password_reset_confirm'),
    # path('auth/profile/', UserProfileView.as_view(), name='enhanced_profile'),
    # path('auth/security-logs/', SecurityLogView.as_view(), name='security_logs'),
    
    # Legacy Authentication Endpoints (for backward compatibility)
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Added missing logout endpoint
    path('profile/', ProfileView.as_view(), name='profile'),
    # path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'), # Disabled
    # path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # Disabled
    # path('email-verification/', EmailVerificationView.as_view(), name='email_verification'), # Disabled
    # path('email-verification/confirm/', EmailVerificationConfirmView.as_view(), name='email_verification_confirm'), # Disabled
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Impact Entry Endpoints
    path('entries/', ImpactEntryListCreateView.as_view(), name='entries'),
    path('entries/<int:pk>/', ImpactEntryDetailView.as_view(), name='entry_detail'),
    path('stats/', ImpactStatsView.as_view(), name='stats'),
    
    # AI Suggestions Endpoints
    path('ai-suggestions/', AISuggestionsView.as_view(), name='ai_suggestions'),
    path('chatgpt-suggestions/', ChatGPTSuggestionsView.as_view(), name='chatgpt_suggestions'),
    
    # Test Endpoints
    path('test-user/', TestUserView.as_view(), name='test_user'),
    
    # Legacy Template Views (for backward compatibility)
    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('entries-list/', entries_list_view, name='entries_list_view'),
    path('stats-view/', stats_view, name='stats_view'),
] 