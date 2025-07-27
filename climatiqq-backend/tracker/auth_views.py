from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
import logging
from datetime import timedelta
import ipaddress
from .auth_serializers import (
    UserRegistrationSerializer, LoginSerializer, PasswordChangeSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    UserProfileSerializer, SecurityLogSerializer, TwoFactorSetupSerializer,
    TwoFactorVerifySerializer
)
from .auth_models import UserProfile, UserSession, SecurityLog, AuthenticationSettings

User = get_user_model()
logger = logging.getLogger(__name__)

class RateLimitMixin:
    """Mixin for rate limiting API endpoints"""
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_rate_limit(self, request, key_prefix, max_attempts, window_minutes):
        """Check rate limit for an action"""
        ip = self.get_client_ip(request)
        cache_key = f"{key_prefix}:{ip}"
        
        attempts = cache.get(cache_key, 0)
        if attempts >= max_attempts:
            return False
        
        cache.set(cache_key, attempts + 1, window_minutes * 60)
        return True

class SecurityLogMixin:
    """Mixin for logging security events"""
    
    def log_security_event(self, user, event_type, request, details=None):
        """Log a security event"""
        try:
            SecurityLog.objects.create(
                user=user,
                event_type=event_type,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                location=self.get_location_from_ip(request),
                details=details or {}
            )
        except Exception as e:
            logger.error(f"Failed to log security event: {e}")
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_location_from_ip(self, request):
        """Get location from IP (placeholder for geolocation service)"""
        # This would integrate with a geolocation service
        return "Unknown"

class EnhancedRegisterView(generics.CreateAPIView, RateLimitMixin, SecurityLogMixin):
    """Enhanced user registration with security features"""
    
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create user with enhanced security"""
        # Check rate limit
        settings = AuthenticationSettings.get_settings()
        if not self.check_rate_limit(request, 'register', 5, 60):  # 5 attempts per hour
            return Response(
                {'error': 'Too many registration attempts. Please try again later.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        try:
            with transaction.atomic():
                # Create user
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                
                # Send welcome email
                self.send_welcome_email(user)
                
                # Log security event
                self.log_security_event(user, 'account_created', request)
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                return Response({
                    'message': 'Account created successfully!',
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'email_verified': user.profile.email_verified
                    },
                    'tokens': {
                        'access': access_token,
                        'refresh': refresh_token
                    }
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return Response(
                {'error': 'Registration failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def send_welcome_email(self, user):
        """Send welcome email to new user"""
        try:
            subject = "Welcome to Rethink! 🌱"
            message = f"""
            Hello {user.username}!
            
            Welcome to Rethink - your personal climate impact tracker!
            
            🎉 Your account has been successfully created.
            
            What you can do now:
            • Track your carbon footprint
            • Monitor water and energy usage
            • Get personalized AI suggestions
            • View your environmental impact over time
            
            Start your journey to a more sustainable lifestyle!
            
            Best regards,
            The Rethink Team
            
            ---
            This is an automated message. Please do not reply to this email.
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            logger.info(f"Welcome email sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")

class EnhancedLoginView(APIView, RateLimitMixin, SecurityLogMixin):
    """Enhanced login with security features"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Handle login with enhanced security"""
        # Check rate limit
        settings = AuthenticationSettings.get_settings()
        if not self.check_rate_limit(request, 'login', settings.login_rate_limit, 1):
            return Response(
                {'error': 'Too many login attempts. Please try again later.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Update user profile
            profile = user.profile
            profile.last_login_ip = self.get_client_ip(request)
            profile.last_login_location = self.get_location_from_ip(request)
            profile.save()
            
            # Log successful login
            self.log_security_event(user, 'login_success', request)
            
            # Create session record
            UserSession.objects.create(
                user=user,
                session_key=request.session.session_key or 'api_session',
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                location=self.get_location_from_ip(request),
                expires_at=timezone.now() + timedelta(hours=settings.session_timeout_hours)
            )
            
            return Response({
                'message': 'Login successful!',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'email_verified': profile.email_verified,
                    'two_factor_enabled': profile.two_factor_enabled
                },
                'tokens': {
                    'access': access_token,
                    'refresh': refresh_token
                }
            })
            
        except serializers.ValidationError as e:
            # Log failed login attempt
            username = request.data.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                    self.log_security_event(user, 'login_failed', request, {'reason': str(e)})
                except User.DoesNotExist:
                    pass
            
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EnhancedPasswordChangeView(APIView, SecurityLogMixin):
    """Enhanced password change with security features"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Handle password change"""
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        
        try:
            serializer.is_valid(raise_exception=True)
            
            # Change password
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Update profile
            profile = user.profile
            profile.password_changed_at = timezone.now()
            profile.save()
            
            # Log security event
            self.log_security_event(user, 'password_change', request)
            
            # Send notification email
            self.send_password_change_notification(user)
            
            return Response({
                'message': 'Password changed successfully!'
            })
            
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def send_password_change_notification(self, user):
        """Send password change notification email"""
        try:
            subject = "Password Changed - Rethink Security Alert"
            message = f"""
            Hello {user.username},
            
            Your password has been successfully changed.
            
            If you did not make this change, please contact support immediately.
            
            Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
            IP Address: {self.get_client_ip(self.request)}
            
            Best regards,
            The Rethink Security Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send password change notification: {e}")

class EnhancedPasswordResetRequestView(APIView, RateLimitMixin, SecurityLogMixin):
    """Enhanced password reset request"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Handle password reset request"""
        # Check rate limit
        settings = AuthenticationSettings.get_settings()
        if not self.check_rate_limit(request, 'password_reset', settings.password_reset_rate_limit, 60):
            return Response(
                {'error': 'Too many password reset requests. Please try again later.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        serializer = PasswordResetRequestSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                profile = user.profile
                
                # Generate reset token
                token = profile.generate_password_reset_token()
                
                # Send reset email
                self.send_password_reset_email(user, token)
                
                # Log security event
                self.log_security_event(user, 'password_reset_requested', request)
                
                return Response({
                    'message': 'If this email is registered, you will receive a password reset link.'
                })
                
            except User.DoesNotExist:
                # Don't reveal if email exists or not
                return Response({
                    'message': 'If this email is registered, you will receive a password reset link.'
                })
                
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def send_password_reset_email(self, user, token):
        """Send password reset email"""
        try:
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
            
            subject = "Password Reset Request - Rethink"
            message = f"""
            Hello {user.username},
            
            You have requested to reset your password.
            
            Click the following link to reset your password:
            {reset_url}
            
            This link will expire in 1 hour.
            
            If you did not request this reset, please ignore this email.
            
            Best regards,
            The Rethink Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send password reset email: {e}")

class EnhancedPasswordResetConfirmView(APIView, SecurityLogMixin):
    """Enhanced password reset confirmation"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Handle password reset confirmation"""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            
            # Get user profile
            profile = UserProfile.objects.get(password_reset_token=serializer.validated_data['token'])
            user = profile.user
            
            # Change password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Clear reset token
            profile.clear_password_reset_token()
            
            # Log security event
            self.log_security_event(user, 'password_reset_completed', request)
            
            return Response({
                'message': 'Password reset successful! You can now login with your new password.'
            })
            
        except UserProfile.DoesNotExist:
            return Response({'error': 'Invalid reset token.'}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView, SecurityLogMixin):
    """User profile management"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user.profile
    
    def retrieve(self, request, *args, **kwargs):
        """Get user profile"""
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        
        # Log profile access
        self.log_security_event(request.user, 'profile_accessed', request)
        
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update user profile"""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # Log profile update
            self.log_security_event(request.user, 'profile_updated', request)
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView, SecurityLogMixin):
    """Enhanced logout with session cleanup"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Handle logout"""
        user = request.user
        
        # Log security event
        self.log_security_event(user, 'logout', request)
        
        # Deactivate current session
        try:
            session = UserSession.objects.get(
                user=user,
                session_key=request.session.session_key or 'api_session',
                is_active=True
            )
            session.deactivate()
        except UserSession.DoesNotExist:
            pass
        
        return Response({'message': 'Logged out successfully!'})

class SecurityLogView(generics.ListAPIView):
    """View security logs (admin only)"""
    
    permission_classes = [permissions.IsAdminUser]
    serializer_class = SecurityLogSerializer
    queryset = SecurityLog.objects.all()
    
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) 