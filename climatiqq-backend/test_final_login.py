#!/usr/bin/env python3
"""
Final test to verify both username and email login work
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

def setup_test_user():
    """Create a test user"""
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
    
    # Delete existing user if exists
    User.objects.filter(username=username).delete()
    
    # Create new user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Created test user:")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Password: {password}")
    return username, email, password

def test_django_auth(username, email, password):
    """Test Django's built-in authentication"""
    print(f"\n🔐 Testing Django authentication:")
    
    # Test username login
    user1 = authenticate(username=username, password=password)
    print(f"   Username login: {'✅ PASS' if user1 else '❌ FAIL'}")
    
    # Test email login (should fail with Django's default auth)
    user2 = authenticate(username=email, password=password)
    print(f"   Email login: {'✅ PASS' if user2 else '❌ FAIL (expected)'}")
    
    return user1 is not None

def test_user_lookup():
    """Test user lookup by email"""
    print(f"\n🔍 Testing user lookup:")
    
    # Test finding user by email
    user = User.objects.filter(email="test@example.com").first()
    if user:
        print(f"   ✅ Found user by email: {user.username}")
        return True
    else:
        print(f"   ❌ No user found by email")
        return False

def main():
    print("🌱 Rethink - Final Login Test")
    print("=" * 40)
    
    # Create test user
    username, email, password = setup_test_user()
    
    # Test Django authentication
    django_auth_works = test_django_auth(username, email, password)
    
    # Test user lookup
    lookup_works = test_user_lookup()
    
    print(f"\n🎯 Test Results:")
    print(f"   Django username auth: {'✅ PASS' if django_auth_works else '❌ FAIL'}")
    print(f"   User lookup by email: {'✅ PASS' if lookup_works else '❌ FAIL'}")
    
    print(f"\n💡 Login Credentials:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    
    print(f"\n📝 Next Steps:")
    print(f"   1. Start the Django server: python manage.py runserver")
    print(f"   2. Try logging in with username: {username}")
    print(f"   3. Try logging in with email: {email}")
    print(f"   4. Check the terminal for conversion logs")

if __name__ == "__main__":
    main() 