#!/usr/bin/env python3
"""
Simple test to verify basic setup
"""
import os
import django
from django.conf import settings

def test_setup():
    """Test basic Django setup"""
    print("🧪 Testing Django setup...")
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        print("✅ Django setup successful!")
        print(f"📊 Database: {settings.DATABASES['default']['ENGINE']}")
        print(f"🌐 Debug mode: {settings.DEBUG}")
        print(f"🔑 Secret key: {settings.SECRET_KEY[:20]}...")
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful!")
            
        # Test models
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_count = User.objects.count()
        print(f"👥 Users in database: {user_count}")
        
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_setup()




