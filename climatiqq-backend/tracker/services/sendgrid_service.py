import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, HtmlContent
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class SendGridService:
    def __init__(self):
        self.api_key = getattr(settings, 'SENDGRID_API_KEY', None)
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@climatiqq.com')
        self.app_name = getattr(settings, 'APP_NAME', 'GreenTrack - Climatiqq')
        self.frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        
        if self.api_key:
            self.sg = sendgrid.SendGridAPIClient(api_key=self.api_key)
        else:
            self.sg = None
            logger.warning("SendGrid API key not configured")

    def send_email(self, to_email, subject, html_content, text_content=None):
        """Send email using SendGrid"""
        if not self.sg:
            logger.error("SendGrid not configured")
            return {
                'success': False,
                'error': 'SendGrid not configured',
                'status_code': None
            }

        try:
            # Create email message
            from_email = Email(self.from_email)
            to_email_obj = To(to_email)
            
            # Create content objects
            html_content_obj = HtmlContent(html_content)
            content_objects = [html_content_obj]
            
            if text_content:
                text_content_obj = Content("text/plain", text_content)
                content_objects.append(text_content_obj)
            
            # Create mail object
            mail = Mail(from_email, to_email_obj, subject, content_objects[0])
            
            # Add additional content if text version exists
            if len(content_objects) > 1:
                mail.add_content(content_objects[1])
            
            # Send email
            response = self.sg.send(mail)
            
            logger.info(f"Email sent successfully to {to_email}. Status: {response.status_code}")
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message_id': response.headers.get('X-Message-Id'),
                'to_email': to_email
            }
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'status_code': None,
                'to_email': to_email
            }

    def send_registration_email(self, user, request):
        """Send welcome email after user registration"""
        try:
            subject = f"Welcome to {self.app_name}!"
            
            # Prepare context for template
            context = {
                'user': user,
                'app_name': self.app_name,
                'frontend_url': self.frontend_url,
                'support_email': getattr(settings, 'SUPPORT_EMAIL', 'support@climatiqq.com')
            }
            
            # Render HTML template
            html_content = render_to_string('emails/registration_welcome.html', context)
            
            # Create plain text version
            text_content = strip_tags(html_content)
            
            # Send email
            return self.send_email(user.email, subject, html_content, text_content)
            
        except Exception as e:
            logger.error(f"Failed to send registration email to {user.email}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'status_code': None
            }

    def send_password_reset_email(self, user, request):
        """Send password reset email"""
        try:
            # Generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # Create reset URL
            reset_url = f"{self.frontend_url}/reset-password?uid={uid}&token={token}"
            
            subject = f"Password Reset Request - {self.app_name}"
            
            # Prepare context for template
            context = {
                'user': user,
                'reset_url': reset_url,
                'app_name': self.app_name,
                'frontend_url': self.frontend_url,
                'support_email': getattr(settings, 'SUPPORT_EMAIL', 'support@climatiqq.com')
            }
            
            # Render HTML template
            html_content = render_to_string('emails/password_reset.html', context)
            
            # Create plain text version
            text_content = strip_tags(html_content)
            
            # Send email
            return self.send_email(user.email, subject, html_content, text_content)
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'status_code': None
            }

    def send_password_change_confirmation(self, user):
        """Send confirmation email after password change"""
        try:
            subject = f"Password Changed Successfully - {self.app_name}"
            
            # Prepare context for template
            context = {
                'user': user,
                'app_name': self.app_name,
                'frontend_url': self.frontend_url,
                'support_email': getattr(settings, 'SUPPORT_EMAIL', 'support@climatiqq.com')
            }
            
            # Render HTML template
            html_content = render_to_string('emails/password_changed.html', context)
            
            # Create plain text version
            text_content = strip_tags(html_content)
            
            # Send email
            return self.send_email(user.email, subject, html_content, text_content)
            
        except Exception as e:
            logger.error(f"Failed to send password change confirmation to {user.email}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'status_code': None
            }

    def validate_reset_token(self, uid, token):
        """Validate password reset token"""
        try:
            # Decode user ID
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            
            # Check if token is valid
            if default_token_generator.check_token(user, token):
                return {
                    'valid': True,
                    'user': user
                }
            else:
                return {
                    'valid': False,
                    'error': 'Invalid or expired token'
                }
                
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return {
                'valid': False,
                'error': 'Invalid user ID'
            }

# Create a singleton instance
sendgrid_service = SendGridService()
