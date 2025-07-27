from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
import uuid

User = get_user_model()

class UserProfile(models.Model):
    """Extended user profile with additional authentication and security features"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Security & Authentication
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Password Security
    password_changed_at = models.DateTimeField(null=True, blank=True)
    password_reset_token = models.UUIDField(null=True, blank=True)
    password_reset_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Account Security
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_location = models.CharField(max_length=200, blank=True)
    
    # Two-Factor Authentication
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True)
    backup_codes = models.JSONField(default=list, blank=True)
    
    # Session Management
    max_concurrent_sessions = models.IntegerField(default=5)
    session_timeout_hours = models.IntegerField(default=24)
    
    # User Preferences
    notification_preferences = models.JSONField(default=dict)
    privacy_settings = models.JSONField(default=dict)
    theme_preference = models.CharField(max_length=20, default='dark')
    
    # Account Status
    is_active = models.BooleanField(default=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    deactivation_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    def is_account_locked(self):
        """Check if account is currently locked"""
        if self.account_locked_until and self.account_locked_until > timezone.now():
            return True
        return False
    
    def lock_account(self, duration_minutes=30):
        """Lock account for specified duration"""
        self.account_locked_until = timezone.now() + timedelta(minutes=duration_minutes)
        self.save()
    
    def unlock_account(self):
        """Unlock account and reset failed attempts"""
        self.account_locked_until = None
        self.failed_login_attempts = 0
        self.save()
    
    def increment_failed_attempts(self):
        """Increment failed login attempts and lock if threshold reached"""
        self.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.lock_account(duration_minutes=30)
        else:
            self.save()
    
    def reset_failed_attempts(self):
        """Reset failed login attempts on successful login"""
        self.failed_login_attempts = 0
        self.save()
    
    def generate_email_verification_token(self):
        """Generate new email verification token"""
        self.email_verification_token = uuid.uuid4()
        self.email_verification_sent_at = timezone.now()
        self.save()
        return self.email_verification_token
    
    def generate_password_reset_token(self):
        """Generate password reset token with expiration"""
        self.password_reset_token = uuid.uuid4()
        self.password_reset_expires_at = timezone.now() + timedelta(hours=1)
        self.save()
        return self.password_reset_token
    
    def is_password_reset_token_valid(self):
        """Check if password reset token is still valid"""
        if not self.password_reset_token or not self.password_reset_expires_at:
            return False
        return self.password_reset_expires_at > timezone.now()
    
    def clear_password_reset_token(self):
        """Clear password reset token after use"""
        self.password_reset_token = None
        self.password_reset_expires_at = None
        self.save()

class UserSession(models.Model):
    """Track user sessions for security and analytics"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    
    # Session metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session for {self.user.username} - {self.session_key[:8]}"
    
    def is_expired(self):
        """Check if session has expired"""
        return timezone.now() > self.expires_at
    
    def extend_session(self, hours=24):
        """Extend session expiration"""
        self.expires_at = timezone.now() + timedelta(hours=hours)
        self.save()
    
    def deactivate(self):
        """Deactivate session"""
        self.is_active = False
        self.save()

class SecurityLog(models.Model):
    """Log security events for monitoring and audit"""
    
    EVENT_TYPES = [
        ('login_success', 'Successful Login'),
        ('login_failed', 'Failed Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Changed'),
        ('email_verification', 'Email Verified'),
        ('account_locked', 'Account Locked'),
        ('account_unlocked', 'Account Unlocked'),
        ('password_reset_requested', 'Password Reset Requested'),
        ('password_reset_completed', 'Password Reset Completed'),
        ('two_factor_enabled', 'Two-Factor Enabled'),
        ('two_factor_disabled', 'Two-Factor Disabled'),
        ('session_created', 'Session Created'),
        ('session_expired', 'Session Expired'),
        ('suspicious_activity', 'Suspicious Activity'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_logs')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'event_type']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.user.username} - {self.timestamp}"

class AuthenticationSettings(models.Model):
    """Global authentication settings"""
    
    # Password Policy - REDUCED FOR DEVELOPMENT
    min_password_length = models.IntegerField(default=3)  # Reduced from 8
    require_uppercase = models.BooleanField(default=False)  # Disabled
    require_lowercase = models.BooleanField(default=False)  # Disabled
    require_numbers = models.BooleanField(default=False)  # Disabled
    require_special_chars = models.BooleanField(default=False)  # Disabled
    password_expiry_days = models.IntegerField(default=365)  # Increased from 90
    
    # Login Security - REDUCED FOR DEVELOPMENT
    max_failed_attempts = models.IntegerField(default=10)  # Increased from 5
    lockout_duration_minutes = models.IntegerField(default=5)  # Reduced from 30
    session_timeout_hours = models.IntegerField(default=168)  # Increased to 1 week
    max_concurrent_sessions = models.IntegerField(default=10)  # Increased from 5
    
    # Email Verification - DISABLED FOR DEVELOPMENT
    require_email_verification = models.BooleanField(default=False)  # Disabled
    email_verification_expiry_hours = models.IntegerField(default=24)
    
    # Two-Factor Authentication - DISABLED FOR DEVELOPMENT
    require_two_factor = models.BooleanField(default=False)  # Disabled
    two_factor_methods = models.JSONField(default=list)  # ['totp', 'sms', 'email']
    
    # Rate Limiting - REDUCED FOR DEVELOPMENT
    login_rate_limit = models.IntegerField(default=20)  # Increased from 5
    password_reset_rate_limit = models.IntegerField(default=10)  # Increased from 3
    
    # Security Headers
    enable_csrf_protection = models.BooleanField(default=True)
    enable_xss_protection = models.BooleanField(default=True)
    enable_content_security_policy = models.BooleanField(default=True)
    
    # Audit & Monitoring
    enable_security_logging = models.BooleanField(default=True)
    log_retention_days = models.IntegerField(default=90)
    
    # Development Settings
    is_development_mode = models.BooleanField(default=True)  # New field
    allow_weak_passwords = models.BooleanField(default=True)  # New field
    skip_email_verification = models.BooleanField(default=True)  # New field
    auto_verify_emails = models.BooleanField(default=True)  # New field
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Authentication Settings"
        verbose_name_plural = "Authentication Settings"
    
    def __str__(self):
        return f"Auth Settings (Dev: {self.is_development_mode})"
    
    @classmethod
    def get_settings(cls):
        """Get or create default settings"""
        settings, created = cls.objects.get_or_create(
            id=1,
            defaults={
                'min_password_length': 3,
                'require_uppercase': False,
                'require_lowercase': False,
                'require_numbers': False,
                'require_special_chars': False,
                'max_failed_attempts': 10,
                'lockout_duration_minutes': 5,
                'require_email_verification': False,
                'require_two_factor': False,
                'is_development_mode': True,
                'allow_weak_passwords': True,
                'skip_email_verification': True,
                'auto_verify_emails': True,
            }
        )
        return settings 