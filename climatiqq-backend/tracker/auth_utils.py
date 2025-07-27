import jwt
import hashlib
import secrets
import string
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth import get_user_model
from .auth_models import UserProfile, SecurityLog

User = get_user_model()

class TokenManager:
    """Utility class for JWT token management"""
    
    @staticmethod
    def generate_access_token(user, expires_in=3600):
        """Generate access token for user"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def generate_refresh_token(user, expires_in=86400):
        """Generate refresh token for user"""
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def get_user_from_token(token):
        """Get user from JWT token"""
        payload = TokenManager.verify_token(token)
        if payload and 'user_id' in payload:
            try:
                return User.objects.get(id=payload['user_id'])
            except User.DoesNotExist:
                return None
        return None

class PasswordUtils:
    """Utility class for password management"""
    
    @staticmethod
    def generate_secure_password(length=12):
        """Generate a secure random password"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    @staticmethod
    def validate_password_strength(password):
        """Validate password strength"""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter.")
        
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter.")
        
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number.")
        
        if not any(c in string.punctuation for c in password):
            errors.append("Password must contain at least one special character.")
        
        return errors
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        return PasswordUtils.hash_password(password) == hashed

class SecurityUtils:
    """Utility class for security functions"""
    
    @staticmethod
    def generate_secure_token(length=32):
        """Generate a secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_backup_codes(count=10):
        """Generate backup codes for 2FA"""
        codes = []
        for _ in range(count):
            code = ''.join(secrets.choice(string.digits) for _ in range(8))
            codes.append(code)
        return codes
    
    @staticmethod
    def hash_backup_code(code):
        """Hash backup code for storage"""
        return hashlib.sha256(code.encode()).hexdigest()
    
    @staticmethod
    def verify_backup_code(code, hashed_codes):
        """Verify backup code"""
        code_hash = SecurityUtils.hash_backup_code(code)
        return code_hash in hashed_codes
    
    @staticmethod
    def is_suspicious_activity(user, request):
        """Check for suspicious activity patterns"""
        # Check for rapid login attempts
        cache_key = f"login_attempts:{user.id}"
        attempts = cache.get(cache_key, 0)
        
        if attempts > 5:  # More than 5 attempts in 5 minutes
            return True
        
        # Check for login from unusual location
        # This would integrate with geolocation service
        return False
    
    @staticmethod
    def log_security_event(user, event_type, request, details=None):
        """Log security event"""
        try:
            SecurityLog.objects.create(
                user=user,
                event_type=event_type,
                ip_address=SecurityUtils.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                location=SecurityUtils.get_location_from_ip(request),
                details=details or {}
            )
        except Exception as e:
            print(f"Failed to log security event: {e}")
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def get_location_from_ip(request):
        """Get location from IP (placeholder for geolocation service)"""
        # This would integrate with a geolocation service
        return "Unknown"

class SessionUtils:
    """Utility class for session management"""
    
    @staticmethod
    def create_user_session(user, request, expires_in=24):
        """Create a new user session"""
        try:
            session = UserSession.objects.create(
                user=user,
                session_key=request.session.session_key or 'api_session',
                ip_address=SecurityUtils.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                location=SecurityUtils.get_location_from_ip(request),
                expires_at=timezone.now() + timedelta(hours=expires_in)
            )
            return session
        except Exception as e:
            print(f"Failed to create user session: {e}")
            return None
    
    @staticmethod
    def deactivate_user_sessions(user, session_key=None):
        """Deactivate user sessions"""
        try:
            if session_key:
                UserSession.objects.filter(
                    user=user,
                    session_key=session_key,
                    is_active=True
                ).update(is_active=False)
            else:
                UserSession.objects.filter(
                    user=user,
                    is_active=True
                ).update(is_active=False)
        except Exception as e:
            print(f"Failed to deactivate user sessions: {e}")
    
    @staticmethod
    def cleanup_expired_sessions():
        """Clean up expired sessions"""
        try:
            expired_sessions = UserSession.objects.filter(
                expires_at__lt=timezone.now(),
                is_active=True
            )
            expired_sessions.update(is_active=False)
            return expired_sessions.count()
        except Exception as e:
            print(f"Failed to cleanup expired sessions: {e}")
            return 0

class EmailUtils:
    """Utility class for email management"""
    
    @staticmethod
    def send_verification_email(user, token):
        """Send email verification email"""
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
            
            subject = "Verify Your Email - Rethink"
            message = f"""
            Hello {user.username},
            
            Please verify your email address by clicking the link below:
            {verification_url}
            
            This link will expire in 24 hours.
            
            If you did not create an account, please ignore this email.
            
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
            return True
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            return False
    
    @staticmethod
    def send_password_reset_email(user, token):
        """Send password reset email"""
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
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
            return True
        except Exception as e:
            print(f"Failed to send password reset email: {e}")
            return False

class ValidationUtils:
    """Utility class for validation functions"""
    
    @staticmethod
    def validate_username(username):
        """Validate username format"""
        import re
        
        if not username:
            return False, "Username is required."
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long."
        
        if len(username) > 30:
            return False, "Username must be no more than 30 characters long."
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores."
        
        return True, None
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        import re
        
        if not email:
            return False, "Email is required."
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Please enter a valid email address."
        
        return True, None
    
    @staticmethod
    def is_email_available(email):
        """Check if email is available"""
        return not User.objects.filter(email=email).exists()
    
    @staticmethod
    def is_username_available(username):
        """Check if username is available"""
        return not User.objects.filter(username=username).exists() 