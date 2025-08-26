#!/usr/bin/env python
"""
Test script for SendGrid integration
Run this script to test if SendGrid is properly configured and working.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tracker.services.sendgrid_service import sendgrid_service
from django.contrib.auth import get_user_model

User = get_user_model()

def test_sendgrid_configuration():
    """Test SendGrid configuration"""
    print("🔍 Testing SendGrid Configuration...")
    
    # Check if API key is set
    api_key = getattr(settings, 'SENDGRID_API_KEY', None)
    if not api_key:
        print("❌ SENDGRID_API_KEY not found in settings")
        print("   Please set SENDGRID_API_KEY in your .env file")
        return False
    
    if api_key == 'your_sendgrid_api_key_here':
        print("❌ SENDGRID_API_KEY is still set to placeholder value")
        print("   Please update with your actual SendGrid API key")
        return False
    
    print(f"✅ SENDGRID_API_KEY found: {api_key[:10]}...")
    
    # Check other settings
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    print(f"✅ DEFAULT_FROM_EMAIL: {from_email}")
    
    app_name = getattr(settings, 'APP_NAME', None)
    print(f"✅ APP_NAME: {app_name}")
    
    return True

def test_sendgrid_service():
    """Test SendGrid service initialization"""
    print("\n🔍 Testing SendGrid Service...")
    
    try:
        # Check if service is properly initialized
        if sendgrid_service.sg is None:
            print("❌ SendGrid service not properly initialized")
            return False
        
        print("✅ SendGrid service initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing SendGrid service: {str(e)}")
        return False

def test_email_templates():
    """Test email template rendering"""
    print("\n🔍 Testing Email Templates...")
    
    try:
        from django.template.loader import render_to_string
        
        # Test registration welcome template
        context = {
            'user': type('MockUser', (), {
                'username': 'testuser',
                'email': 'test@example.com'
            })(),
            'app_name': 'GreenTrack - Climatiqq',
            'frontend_url': 'http://localhost:3000',
            'support_email': 'support@climatiqq.com'
        }
        
        html_content = render_to_string('emails/registration_welcome.html', context)
        if html_content:
            print("✅ Registration welcome template renders successfully")
        else:
            print("❌ Registration welcome template failed to render")
            return False
        
        # Test password reset template
        context['reset_url'] = 'http://localhost:3000/reset-password?uid=test&token=test'
        html_content = render_to_string('emails/password_reset.html', context)
        if html_content:
            print("✅ Password reset template renders successfully")
        else:
            print("❌ Password reset template failed to render")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing email templates: {str(e)}")
        return False

def test_sendgrid_connection():
    """Test actual SendGrid connection (optional)"""
    print("\n🔍 Testing SendGrid Connection...")
    
    # Check if we should test actual connection
    test_connection = input("Do you want to test actual SendGrid connection? (y/n): ").lower().strip()
    
    if test_connection != 'y':
        print("⏭️  Skipping SendGrid connection test")
        return True
    
    try:
        # Try to send a test email
        test_email = input("Enter test email address: ").strip()
        
        if not test_email:
            print("❌ No email address provided")
            return False
        
        # Create a mock user for testing
        mock_user = type('MockUser', (), {
            'username': 'testuser',
            'email': test_email
        })()
        
        # Try to send registration email
        result = sendgrid_service.send_registration_email(mock_user, None)
        
        if result['success']:
            print("✅ Test email sent successfully!")
            print(f"   Status Code: {result['status_code']}")
            print(f"   Message ID: {result.get('message_id', 'N/A')}")
            return True
        else:
            print(f"❌ Failed to send test email: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing SendGrid connection: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 SendGrid Integration Test Suite")
    print("=" * 50)
    
    # Run all tests
    tests = [
        test_sendgrid_configuration,
        test_sendgrid_service,
        test_email_templates,
        test_sendgrid_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SendGrid integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
