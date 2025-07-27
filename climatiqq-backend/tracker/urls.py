from django.urls import path
from .views import (
    RegisterView, CustomTokenObtainPairView, ProfileView, 
    ImpactEntryListCreateView, ImpactEntryDetailView, ImpactStatsView, 
    dashboard_view, entries_list_view, stats_view, ChatGPTSuggestionsView,
    PasswordResetRequestView, PasswordResetConfirmView, 
    EmailVerificationView, EmailVerificationConfirmView, ChangePasswordView,
    TestUserView
)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/email-verification/', EmailVerificationView.as_view(), name='email-verification'),
    path('auth/email-verification/confirm/', EmailVerificationConfirmView.as_view(), name='email-verification-confirm'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # Test endpoint
    path('test-users/', TestUserView.as_view(), name='test-users'),
    
    # Impact entries endpoints
    path('impact-entries/', ImpactEntryListCreateView.as_view(), name='impactentry-list-create'),
    path('impact-entries/<int:pk>/', ImpactEntryDetailView.as_view(), name='impactentry-detail'),
    path('impact-stats/', ImpactStatsView.as_view(), name='impact-stats'),
    path('suggestions/', ChatGPTSuggestionsView.as_view(), name='chatgpt-suggestions'),
    
    # Web views (for browser) - these were added but then the user shifted to React
    path('dashboard/', dashboard_view, name='dashboard'),
    path('entries/', entries_list_view, name='entries-list'),
    path('stats/', stats_view, name='stats'),
] 