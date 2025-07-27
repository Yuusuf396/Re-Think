#!/usr/bin/env python
"""
Script to test email functionality
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

def test_email_sending():
    """Test email sending functionality"""
    try:
        print("📧 Testing email functionality...")
        print(f"📧 Email backend: {settings.EMAIL_BACKEND}")
        print(f"📧 Email host: {settings.EMAIL_HOST}")
        print(f"📧 Email port: {settings.EMAIL_PORT}")
        print(f"📧 From email: {settings.DEFAULT_FROM_EMAIL}")
        
        # Send test email
        send_mail(
            subject="🧪 Email Test - Rethink API",
            message="""
            Hello!
            
            This is a test email from your Rethink API.
            
            📧 Email functionality is working!
            
            If you're seeing this in the terminal, email backend is working correctly.
            To send real emails, configure SMTP settings in your .env file.
            
            Best regards,
            Rethink Team
            """,
            from_email=None,  # Use DEFAULT_FROM_EMAIL
            recipient_list=['adebayoayomide396@gmail.com'],
            fail_silently=False,
        )
        
        print("✅ Test email sent successfully!")
        print("📧 Check your terminal/console for the email content")
        
        return True
        
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

def show_email_config():
    """Show current email configuration"""
    print("\n📧 Current Email Configuration:")
    print(f"   Backend: {settings.EMAIL_BACKEND}")
    print(f"   Host: {settings.EMAIL_HOST}")
    print(f"   Port: {settings.EMAIL_PORT}")
    print(f"   TLS: {settings.EMAIL_USE_TLS}")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   User: {settings.EMAIL_HOST_USER}")
    print(f"   Password: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Not set'}")
    
    print("\n📧 To send real emails:")
    print("1. Create a .env file in climatiqq-backend/")
    print("2. Add your email credentials:")
    print("   EMAIL_HOST_USER=your-email@gmail.com")
    print("   EMAIL_HOST_PASSWORD=your-app-password")
    print("3. Change EMAIL_BACKEND to 'django.core.mail.backends.smtp.EmailBackend' in settings.py")

if __name__ == "__main__":
    show_email_config()
    test_email_sending() 