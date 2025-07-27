from django.contrib import admin
from .models import ImpactEntry
from .auth_models import UserProfile, UserSession, SecurityLog, AuthenticationSettings

# Register your models here.

@admin.register(ImpactEntry)
class ImpactEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'metric_type', 'value', 'description', 'created_at']
    list_filter = ['metric_type', 'created_at', 'user']
    search_fields = ['user__username', 'description']
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_verified', 'two_factor_enabled', 'is_active', 'created_at']
    list_filter = ['email_verified', 'two_factor_enabled', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'ip_address', 'is_active', 'created_at', 'expires_at']
    list_filter = ['is_active', 'created_at', 'expires_at']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['created_at', 'last_activity']

@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_type', 'ip_address', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

@admin.register(AuthenticationSettings)
class AuthenticationSettingsAdmin(admin.ModelAdmin):
    list_display = ['min_password_length', 'require_uppercase', 'require_lowercase', 'require_numbers']
    readonly_fields = ['id']
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not AuthenticationSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False
