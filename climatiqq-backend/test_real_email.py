#!/usr/bin/env python3
"""
Test Real Email Sending
Checks if your email configuration is working
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

def test_real_email():
    """Test if real email sending is working"""
    print("📧 Testing Real Email Sending")
    print("=" * 50)
    
    # Check configuration
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"SMTP Host: {settings.EMAIL_HOST}")
    print(f"SMTP Port: {settings.EMAIL_PORT}")
    print(f"TLS Enabled: {settings.EMAIL_USE_TLS}")
    print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"Username: {settings.EMAIL_HOST_USER}")
    
    # Check if API key is configured
    api_key = os.getenv('RESEND_API_KEY')
    if api_key and api_key != 'your-resend-api-key-here':
        print("✅ Resend API key is configured")
    else:
        print("❌ Resend API key not configured")
        print("   Run: python setup_email.py")
        return False
    
    # Test email
    test_email = input("\nEnter your email address to test: ").strip()
    
    if not test_email:
        print("❌ No email address provided")
        return False
    
    print(f"\n📧 Sending test email to: {test_email}")
    
    try:
        # Send test email
        result = send_mail(
            subject="🧪 Rethink Email Test",
            message=f"""
            Hello!
            
            This is a test email from your Rethink application.
            
            ✅ If you receive this email, your email configuration is working!
            
            📧 Email backend: {settings.EMAIL_BACKEND}
            📧 SMTP host: {settings.EMAIL_HOST}
            📧 From: {settings.DEFAULT_FROM_EMAIL}
            
            Your Rethink application can now send real emails!
            
            Best regards,
            Rethink Team 🌱
            """,
            from_email=None,  # Use DEFAULT_FROM_EMAIL
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print(f"✅ Email sent successfully! Result: {result}")
        print("📧 Check your email inbox for the test message")
        print("📧 Also check the console above for the printed version")
        
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        print("\n📧 Troubleshooting:")
        print("1. Check your API key in .env file")
        print("2. Make sure you're using a valid email address")
        print("3. Check your internet connection")
        print("4. Try running: python setup_email.py")
        
        return False

def check_configuration():
    """Check current email configuration"""
    print("\n📧 Current Email Configuration:")
    print("=" * 40)
    
    # Check .env file
    if os.path.exists('.env'):
        print("✅ .env file exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'RESEND_API_KEY' in content:
                print("✅ RESEND_API_KEY found in .env")
            else:
                print("❌ RESEND_API_KEY not found in .env")
    else:
        print("❌ .env file not found")
        print("   Run: python setup_email.py")
    
    # Check settings
    print(f"\nEmail Backend: {settings.EMAIL_BACKEND}")
    print(f"SMTP Host: {settings.EMAIL_HOST}")
    print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")

if __name__ == "__main__":
    check_configuration()
    
    choice = input("\nTest real email sending? (y/n): ").strip().lower()
    if choice == 'y':
        test_real_email()
    else:
        print("Test cancelled.") 