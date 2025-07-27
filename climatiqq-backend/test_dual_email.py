#!/usr/bin/env python
"""
Script to test dual email functionality (print + send)
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_dual_email():
    """Test dual email functionality (print + send)"""
    print("📧 Testing Dual Email Functionality")
    print("=" * 50)
    print(f"Email backend: {settings.EMAIL_BACKEND}")
    print(f"SMTP host: {settings.EMAIL_HOST}")
    print(f"SMTP port: {settings.EMAIL_PORT}")
    print(f"From email: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    # Test email that will be both printed and sent
    subject = "🧪 Dual Email Test - Print + Send"
    message = f"""
    Hello!
    
    This is a test email to demonstrate dual functionality.
    
    📧 What should happen:
    ✅ Email will be printed to console (always)
    ✅ Email will be sent via SMTP (if configured)
    
    📧 Email backend: {settings.EMAIL_BACKEND}
    🕒 Sent at: {django.utils.timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
    
    If you see this in the console AND receive it in your email:
    🎉 Dual email functionality is working perfectly!
    
    If you only see it in console:
    ⚠️ SMTP not configured - check your email settings
    
    Best regards,
    Rethink Team 🌱
    """
    
    try:
        # Send email (will be both printed and sent)
        result = send_mail(
            subject=subject,
            message=message,
            from_email=None,  # Use DEFAULT_FROM_EMAIL
            recipient_list=['test@example.com'],
            fail_silently=False,
        )
        
        print(f"✅ Email sent successfully! Result: {result}")
        print()
        print("📧 Check above for console output")
        print("📧 Check your email inbox (if SMTP configured)")
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

def show_email_status():
    """Show current email configuration status"""
    print("\n📧 Email Configuration Status:")
    print("=" * 40)
    print(f"Backend: {settings.EMAIL_BACKEND}")
    print(f"SMTP Host: {settings.EMAIL_HOST}")
    print(f"SMTP Port: {settings.EMAIL_PORT}")
    print(f"TLS: {settings.EMAIL_USE_TLS}")
    print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"Username: {settings.EMAIL_HOST_USER}")
    print(f"Password: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Not set'}")
    
    # Check if Resend API key is set
    api_key = os.getenv('RESEND_API_KEY')
    if api_key and api_key != 'your-resend-api-key':
        print("✅ Resend API key is configured")
    else:
        print("⚠️ Resend API key not configured")
        print("   Set RESEND_API_KEY in .env file for real email sending")

if __name__ == "__main__":
    show_email_status()
    print()
    test_dual_email() 