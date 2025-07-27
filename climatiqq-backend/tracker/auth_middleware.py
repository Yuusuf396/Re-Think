from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging
from .auth_models import UserSession, SecurityLog, AuthenticationSettings

logger = logging.getLogger(__name__)

class SecurityMiddleware(MiddlewareMixin):
    """Middleware for security monitoring and session management"""
    
    def process_request(self, request):
        """Process incoming request for security checks"""
        # Skip for static files and admin
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return None
        
        # Get client IP
        ip = self.get_client_ip(request)
        
        # Check for suspicious activity
        if self.is_suspicious_ip(ip):
            logger.warning(f"Suspicious IP detected: {ip}")
            return JsonResponse(
                {'error': 'Access denied due to suspicious activity.'},
                status=403
            )
        
        # Rate limiting for API endpoints
        if request.path.startswith('/api/'):
            if not self.check_api_rate_limit(request):
                return JsonResponse(
                    {'error': 'Too many requests. Please try again later.'},
                    status=429
                )
        
        return None
    
    def process_response(self, request, response):
        """Process outgoing response for security headers"""
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Add CSP header if enabled
        settings_obj = AuthenticationSettings.get_settings()
        if settings_obj.enable_content_security_policy:
            response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_suspicious_ip(self, ip):
        """Check if IP is suspicious (placeholder for IP reputation service)"""
        # This would integrate with an IP reputation service
        # For now, just check against a simple blacklist
        suspicious_ips = cache.get('suspicious_ips', [])
        return ip in suspicious_ips
    
    def check_api_rate_limit(self, request):
        """Check API rate limiting"""
        ip = self.get_client_ip(request)
        cache_key = f"api_rate_limit:{ip}"
        
        # Get current request count
        requests = cache.get(cache_key, 0)
        
        # Check if limit exceeded
        if requests >= 100:  # 100 requests per minute
            return False
        
        # Increment request count
        cache.set(cache_key, requests + 1, 60)  # 1 minute window
        return True

class SessionMiddleware(MiddlewareMixin):
    """Middleware for session management and cleanup"""
    
    def process_request(self, request):
        """Process request for session management"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Check if user has active sessions
            active_sessions = UserSession.objects.filter(
                user=request.user,
                is_active=True
            )
            
            # Clean up expired sessions
            expired_sessions = active_sessions.filter(expires_at__lt=timezone.now())
            expired_sessions.update(is_active=False)
            
            # Check session limit
            settings_obj = AuthenticationSettings.get_settings()
            if active_sessions.count() > settings_obj.max_concurrent_sessions:
                # Deactivate oldest sessions
                oldest_sessions = active_sessions.order_by('created_at')[
                    settings_obj.max_concurrent_sessions:
                ]
                oldest_sessions.update(is_active=False)
    
    def process_response(self, request, response):
        """Process response for session tracking"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Update session activity
            try:
                session = UserSession.objects.get(
                    user=request.user,
                    session_key=request.session.session_key or 'api_session',
                    is_active=True
                )
                session.last_activity = timezone.now()
                session.save()
            except UserSession.DoesNotExist:
                pass
        
        return response

class AuthenticationAuditMiddleware(MiddlewareMixin):
    """Middleware for authentication audit logging"""
    
    def process_request(self, request):
        """Log authentication events"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Log successful authentication
            try:
                SecurityLog.objects.create(
                    user=request.user,
                    event_type='session_accessed',
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    location=self.get_location_from_ip(request),
                    details={'path': request.path}
                )
            except Exception as e:
                logger.error(f"Failed to log authentication event: {e}")
        
        return None
    
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

class PasswordExpiryMiddleware(MiddlewareMixin):
    """Middleware for password expiry checks"""
    
    def process_request(self, request):
        """Check password expiry"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                profile = request.user.profile
                settings_obj = AuthenticationSettings.get_settings()
                
                # Check if password has expired
                if profile.password_changed_at:
                    expiry_date = profile.password_changed_at + timedelta(
                        days=settings_obj.password_expiry_days
                    )
                    
                    if timezone.now() > expiry_date:
                        # Password has expired
                        return JsonResponse({
                            'error': 'Your password has expired. Please change it.',
                            'password_expired': True
                        }, status=401)
                
            except Exception as e:
                logger.error(f"Password expiry check failed: {e}")
        
        return None

class TwoFactorMiddleware(MiddlewareMixin):
    """Middleware for two-factor authentication"""
    
    def process_request(self, request):
        """Check two-factor authentication requirements"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                profile = request.user.profile
                settings_obj = AuthenticationSettings.get_settings()
                
                # Check if 2FA is required
                if settings_obj.require_two_factor and not profile.two_factor_enabled:
                    # 2FA is required but not set up
                    return JsonResponse({
                        'error': 'Two-factor authentication is required.',
                        'two_factor_required': True
                    }, status=401)
                
                # Check if 2FA is enabled and verification is needed
                if profile.two_factor_enabled:
                    # This would check if 2FA verification is complete for this session
                    # For now, we'll skip this check
                    pass
                
            except Exception as e:
                logger.error(f"Two-factor authentication check failed: {e}")
        
        return None

class AccountLockoutMiddleware(MiddlewareMixin):
    """Middleware for account lockout checks"""
    
    def process_request(self, request):
        """Check if account is locked"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                profile = request.user.profile
                
                # Check if account is locked
                if profile.is_account_locked():
                    return JsonResponse({
                        'error': f'Account is locked until {profile.account_locked_until.strftime("%Y-%m-%d %H:%M")}.',
                        'account_locked': True
                    }, status=401)
                
                # Check if account is deactivated
                if not profile.is_active:
                    return JsonResponse({
                        'error': 'Account is deactivated.',
                        'account_deactivated': True
                    }, status=401)
                
            except Exception as e:
                logger.error(f"Account lockout check failed: {e}")
        
        return None 