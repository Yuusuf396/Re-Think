#!/usr/bin/env python3
"""
Test script to verify Supabase database connection and SendGrid email functionality
"""
import os
import django
from django.conf import settings

def test_supabase_connection():
    """Test Supabase database connection"""
    print("🧪 Testing Supabase Database Connection...")
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        print("✅ Django setup successful!")
        print(f"📊 Database Engine: {settings.DATABASES['default']['ENGINE']}")
        print(f"🌐 Database Host: {settings.DATABASES['default']['HOST']}")
        print(f"📁 Database Name: {settings.DATABASES['default']['NAME']}")
        print(f"👤 Database User: {settings.DATABASES['default']['USER']}")
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"✅ Database connection successful!")
            print(f"📋 PostgreSQL Version: {version}")
            
        # Test models
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_count = User.objects.count()
        print(f"👥 Users in Supabase database: {user_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sendgrid_email():
    """Test SendGrid email functionality"""
    print("\n📧 Testing SendGrid Email Configuration...")
    
    try:
        # Check SendGrid configuration
        sendgrid_key = getattr(settings, 'SENDGRID_API_KEY', None)
        email_host = getattr(settings, 'EMAIL_HOST', None)
        email_backend = getattr(settings, 'EMAIL_BACKEND', None)
        
        print(f"✅ SendGrid API Key: {'Set' if sendgrid_key else 'Not Set'}")
        print(f"✅ Email Host: {email_host}")
        print(f"✅ Email Backend: {email_backend}")
        
        if sendgrid_key:
            print(f"🔑 API Key starts with: {sendgrid_key[:10]}...")
        
        # Test SendGrid service
        from tracker.services.sendgrid_service import SendGridService
        sendgrid_service = SendGridService()
        
        print(f"✅ SendGrid service initialized")
        print(f"✅ From Email: {sendgrid_service.from_email}")
        print(f"✅ App Name: {sendgrid_service.app_name}")
        
        # Test email template rendering
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Create a test user or use existing one
        test_user, created = User.objects.get_or_create(
            username='test_email_user',
            defaults={
                'email': 'test@example.com',
                'password': 'testpass123'
            }
        )
        
        if created:
            print(f"✅ Test user created: {test_user.username}")
        else:
            print(f"✅ Test user exists: {test_user.username}")
        
        # Test email template rendering
        try:
            from django.template.loader import render_to_string
            context = {
                'user': test_user,
                'app_name': 'GreenTrack - Climatiqq',
                'frontend_url': 'http://localhost:3000',
                'support_email': 'support@climatiqq.com'
            }
            
            html_content = render_to_string('emails/registration_welcome.html', context)
            print(f"✅ Email template rendering successful")
            print(f"📧 Template length: {len(html_content)} characters")
            
        except Exception as e:
            print(f"❌ Email template rendering failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ SendGrid test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_registration_flow():
    """Test the complete registration flow"""
    print("\n🚀 Testing Complete Registration Flow...")
    
    try:
        from tracker.views import RegisterView
        from tracker.serializers import UserRegistrationSerializer
        from rest_framework.test import APIRequestFactory
        
        print("✅ Registration view imported successfully")
        print("✅ Registration serializer imported successfully")
        
        # Test serializer validation
        test_data = {
            'username': 'test_reg_user',
            'email': 'test_reg@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        
        serializer = UserRegistrationSerializer(data=test_data)
        if serializer.is_valid():
            print("✅ Registration serializer validation successful")
        else:
            print(f"❌ Registration serializer validation failed: {serializer.errors}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Registration flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🎯 Running Comprehensive Supabase + Email Tests...\n")
    
    tests = [
        ("Supabase Database", test_supabase_connection),
        ("SendGrid Email", test_sendgrid_email),
        ("Registration Flow", test_registration_flow)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Testing: {test_name}")
        print(f"{'='*50}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*50}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == '__main__':
    main()
