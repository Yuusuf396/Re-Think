from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import re
from .auth_models import UserProfile, UserSession, SecurityLog, AuthenticationSettings

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Enhanced user registration with comprehensive validation"""
    
    password = serializers.CharField(write_only=True, min_length=3)  # Reduced from 8
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    terms_accepted = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'terms_accepted']
        extra_kwargs = {
            'username': {'min_length': 2, 'max_length': 30},  # Reduced from 3
        }
    
    def validate_username(self, value):
        """Validate username format and uniqueness"""
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        
        return value
    
    def validate_email(self, value):
        """Validate email format and uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value
    
    def validate_password(self, value):
        """Validate password strength - LENIENT FOR DEVELOPMENT"""
        settings = AuthenticationSettings.get_settings()
        
        # Check minimum length only
        if len(value) < settings.min_password_length:
            raise serializers.ValidationError(
                f"Password must be at least {settings.min_password_length} characters long."
            )
        
        # Skip complex validation in development mode
        if settings.is_development_mode and settings.allow_weak_passwords:
            return value
        
        # Only apply complex validation if not in development mode
        if not settings.is_development_mode:
            # Check password complexity requirements
            if settings.require_uppercase and not re.search(r'[A-Z]', value):
                raise serializers.ValidationError("Password must contain at least one uppercase letter.")
            
            if settings.require_lowercase and not re.search(r'[a-z]', value):
                raise serializers.ValidationError("Password must contain at least one lowercase letter.")
            
            if settings.require_numbers and not re.search(r'\d', value):
                raise serializers.ValidationError("Password must contain at least one number.")
            
            if settings.require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
                raise serializers.ValidationError("Password must contain at least one special character.")
            
            # Validate using Django's password validation
            try:
                validate_password(value)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages[0])
        
        return value
    
    def validate(self, data):
        """Validate form data"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        
        if not data.get('terms_accepted'):
            raise serializers.ValidationError("You must accept the terms and conditions.")
        
        return data
    
    def create(self, validated_data):
        """Create user and profile"""
        # Remove confirmation fields
        validated_data.pop('password_confirm')
        validated_data.pop('terms_accepted')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            password_changed_at=timezone.now()
        )
        
        return user

class LoginSerializer(serializers.Serializer):
    """Enhanced login serializer with security features"""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)
    
    def validate(self, data):
        """Validate login credentials and check account status"""
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")
        
        # Get user and profile
        try:
            user = User.objects.get(username=username)
            profile = user.profile
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")
        
        # Check if account is locked
        if profile.is_account_locked():
            raise serializers.ValidationError(
                f"Account is locked until {profile.account_locked_until.strftime('%Y-%m-%d %H:%M')}. "
                "Please try again later."
            )
        
        # Check if account is active
        if not user.is_active or not profile.is_active:
            raise serializers.ValidationError("Account is deactivated.")
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            # Log failed attempt
            profile.increment_failed_attempts()
            raise serializers.ValidationError("Invalid credentials.")
        
        # Reset failed attempts on successful login
        profile.reset_failed_attempts()
        
        data['user'] = user
        return data

class PasswordChangeSerializer(serializers.Serializer):
    """Password change serializer with validation"""
    
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=3)  # Reduced from 8
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate_current_password(self, value):
        """Validate current password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
    
    def validate_new_password(self, value):
        """Validate new password strength - LENIENT FOR DEVELOPMENT"""
        settings = AuthenticationSettings.get_settings()
        
        # Check minimum length only
        if len(value) < settings.min_password_length:
            raise serializers.ValidationError(
                f"Password must be at least {settings.min_password_length} characters long."
            )
        
        # Skip complex validation in development mode
        if settings.is_development_mode and settings.allow_weak_passwords:
            return value
        
        # Only apply complex validation if not in development mode
        if not settings.is_development_mode:
            # Check password complexity requirements
            if settings.require_uppercase and not re.search(r'[A-Z]', value):
                raise serializers.ValidationError("Password must contain at least one uppercase letter.")
            
            if settings.require_lowercase and not re.search(r'[a-z]', value):
                raise serializers.ValidationError("Password must contain at least one lowercase letter.")
            
            if settings.require_numbers and not re.search(r'\d', value):
                raise serializers.ValidationError("Password must contain at least one number.")
            
            if settings.require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
                raise serializers.ValidationError("Password must contain at least one special character.")
            
            # Validate using Django's password validation
            try:
                validate_password(value)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages[0])
        
        return value
    
    def validate(self, data):
        """Validate form data"""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        
        if data['current_password'] == data['new_password']:
            raise serializers.ValidationError("New password must be different from current password.")
        
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    """Password reset request serializer"""
    
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """Validate email exists"""
        if not User.objects.filter(email=value).exists():
            # Don't reveal if email exists or not for security
            raise serializers.ValidationError("If this email is registered, you will receive a reset link.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    """Password reset confirmation serializer"""
    
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate_token(self, value):
        """Validate reset token"""
        try:
            profile = UserProfile.objects.get(password_reset_token=value)
            if not profile.is_password_reset_token_valid():
                raise serializers.ValidationError("Reset token has expired.")
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Invalid reset token.")
        return value
    
    def validate_new_password(self, value):
        """Validate new password strength - LENIENT FOR DEVELOPMENT"""
        settings = AuthenticationSettings.get_settings()
        
        # Check minimum length only
        if len(value) < settings.min_password_length:
            raise serializers.ValidationError(
                f"Password must be at least {settings.min_password_length} characters long."
            )
        
        # Skip complex validation in development mode
        if settings.is_development_mode and settings.allow_weak_passwords:
            return value
        
        # Only apply complex validation if not in development mode
        if not settings.is_development_mode:
            # Check password complexity requirements
            if settings.require_uppercase and not re.search(r'[A-Z]', value):
                raise serializers.ValidationError("Password must contain at least one uppercase letter.")
            
            if settings.require_lowercase and not re.search(r'[a-z]', value):
                raise serializers.ValidationError("Password must contain at least one lowercase letter.")
            
            if settings.require_numbers and not re.search(r'\d', value):
                raise serializers.ValidationError("Password must contain at least one number.")
            
            if settings.require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
                raise serializers.ValidationError("Password must contain at least one special character.")
        
        return value
    
    def validate(self, data):
        """Validate form data"""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'username', 'email', 'date_joined', 'last_login',
            'email_verified', 'two_factor_enabled', 'is_active',
            'notification_preferences', 'privacy_settings', 'theme_preference',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class SecurityLogSerializer(serializers.ModelSerializer):
    """Security log serializer for admin/audit purposes"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    
    class Meta:
        model = SecurityLog
        fields = [
            'id', 'username', 'event_type', 'event_type_display',
            'ip_address', 'location', 'details', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']

class TwoFactorSetupSerializer(serializers.Serializer):
    """Two-factor authentication setup serializer"""
    
    method = serializers.ChoiceField(choices=[
        ('totp', 'Time-based One-Time Password'),
        ('sms', 'SMS'),
        ('email', 'Email')
    ])
    
    def validate_method(self, value):
        """Validate 2FA method is supported"""
        settings = AuthenticationSettings.get_settings()
        if value not in settings.two_factor_methods:
            raise serializers.ValidationError("This 2FA method is not supported.")
        return value

class TwoFactorVerifySerializer(serializers.Serializer):
    """Two-factor authentication verification serializer"""
    
    code = serializers.CharField(min_length=6, max_length=6)
    remember_device = serializers.BooleanField(default=False)
    
    def validate_code(self, value):
        """Validate 2FA code format"""
        if not value.isdigit():
            raise serializers.ValidationError("Code must contain only numbers.")
        return value 