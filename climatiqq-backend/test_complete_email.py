#!/usr/bin/env python3
"""
Complete Email System Test
Tests all email functionality and identifies issues
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
from django.contrib.auth import get_user_model
from tracker.models import ImpactEntry
from datetime import datetime

User = get_user_model()

def test_email_configuration():
    """Test email configuration"""
    print("📧 Testing Email Configuration")
    print("=" * 50)
    
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"SMTP Host: {settings.EMAIL_HOST}")
    print(f"SMTP Port: {settings.EMAIL_PORT}")
    print(f"TLS Enabled: {settings.EMAIL_USE_TLS}")
    print(f"Username: {settings.EMAIL_HOST_USER}")
    print(f"Password: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'None'}")
    print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
    
    # Check API key
    api_key = os.getenv('RESEND_API_KEY')
    if api_key and api_key != 'your-resend-api-key':
        print("✅ Resend API key is configured")
    else:
        print("❌ Resend API key not configured")
    
    return True

def test_basic_email():
    """Test basic email sending"""
    print("\n📧 Testing Basic Email Sending")
    print("=" * 50)
    
    test_email = input("Enter your email address to test: ").strip()
    
    if not test_email:
        print("❌ No email address provided")
        return False
    
    try:
        result = send_mail(
            subject="🧪 Rethink Email Test",
            message=f"""
            Hello!
            
            This is a test email from your Rethink application.
            
            ✅ If you receive this email, your email configuration is working!
            
            📧 Email backend: {settings.EMAIL_BACKEND}
            📧 SMTP host: {settings.EMAIL_HOST}
            📧 From: {settings.DEFAULT_FROM_EMAIL}
            📧 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            
            Your Rethink application can now send real emails!
            
            Best regards,
            Rethink Team 🌱
            """,
            from_email=None,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print(f"✅ Email sent successfully! Result: {result}")
        print("📧 Check your email inbox for the test message")
        print("📧 Also check the console above for the printed version")
        
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

def test_password_change_email():
    """Test password change email functionality"""
    print("\n🔐 Testing Password Change Email")
    print("=" * 50)
    
    # Create or get a test user
    try:
        user, created = User.objects.get_or_create(
            username='testuser_email',
            defaults={
                'email': 'test@example.com',
                'password': 'testpass123'
            }
        )
        
        if created:
            print(f"✅ Created test user: {user.username}")
        else:
            print(f"✅ Using existing test user: {user.username}")
        
        # Simulate password change email
        from tracker.views import ChangePasswordView
        
        # Create a mock request
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        
        factory = RequestFactory()
        request = factory.post('/change-password/')
        request.user = user
        request.META = {
            'HTTP_X_FORWARDED_FOR': '192.168.1.1',
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Test Browser)',
            'REMOTE_ADDR': '192.168.1.1'
        }
        
        # Test the password change notification
        view = ChangePasswordView()
        view.request = request
        view.send_password_change_notification(user)
        
        print("✅ Password change email test completed")
        print("📧 Check console above for email output")
        
        return True
        
    except Exception as e:
        print(f"❌ Password change email test failed: {e}")
        return False

def test_welcome_email():
    """Test welcome email functionality"""
    print("\n🎉 Testing Welcome Email")
    print("=" * 50)
    
    try:
        # Create a test user for welcome email
        user, created = User.objects.get_or_create(
            username='testuser_welcome',
            defaults={
                'email': 'welcome@example.com',
                'password': 'testpass123'
            }
        )
        
        if created:
            print(f"✅ Created test user: {user.username}")
        else:
            print(f"✅ Using existing test user: {user.username}")
        
        # Simulate welcome email
        from tracker.views import RegisterView
        
        view = RegisterView()
        view.send_welcome_email(user)
        
        print("✅ Welcome email test completed")
        print("📧 Check console above for email output")
        
        return True
        
    except Exception as e:
        print(f"❌ Welcome email test failed: {e}")
        return False

def check_database():
    """Check database for any issues"""
    print("\n🗄️ Checking Database")
    print("=" * 50)
    
    try:
        # Check users
        user_count = User.objects.count()
        print(f"✅ Users in database: {user_count}")
        
        # Check impact entries
        entry_count = ImpactEntry.objects.count()
        print(f"✅ Impact entries in database: {entry_count}")
        
        # Check if test users exist
        test_users = User.objects.filter(username__startswith='testuser')
        print(f"✅ Test users found: {test_users.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Complete Email System Test")
    print("=" * 50)
    
    tests = [
        ("Email Configuration", test_email_configuration),
        ("Database Check", check_database),
        ("Basic Email", test_basic_email),
        ("Password Change Email", test_password_change_email),
        ("Welcome Email", test_welcome_email),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Email system is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for issues.")

if __name__ == "__main__":
    main() 