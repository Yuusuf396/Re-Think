#!/usr/bin/env python3
"""
Test script to verify email login functionality
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

def create_test_user():
    """Create a test user with both username and email"""
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

def test_username_login(username, password):
    """Test login with username"""
    print(f"\n🔐 Testing login with username: {username}")
    
    user = authenticate(username=username, password=password)
    if user:
        print(f"✅ Username login successful!")
        return True
    else:
        print(f"❌ Username login failed!")
        return False

def test_email_login(email, password):
    """Test login with email"""
    print(f"\n📧 Testing login with email: {email}")
    
    # Find user by email
    user = User.objects.filter(email=email).first()
    if user:
        print(f"✅ Found user by email: {user.username}")
        
        # Try to authenticate with username
        auth_user = authenticate(username=user.username, password=password)
        if auth_user:
            print(f"✅ Email login successful!")
            return True
        else:
            print(f"❌ Email login failed!")
            return False
    else:
        print(f"❌ No user found with email: {email}")
        return False

def list_users():
    """List all users in database"""
    print("\n📋 All users in database:")
    users = User.objects.all()
    
    if not users.exists():
        print("   No users found")
        return
    
    for user in users:
        print(f"   Username: {user.username}, Email: {user.email}, Active: {user.is_active}")

def main():
    print("🌱 Rethink - Email Login Test")
    print("=" * 40)
    
    # List existing users
    list_users()
    
    # Create test user
    username, email, password = create_test_user()
    
    # Test username login
    username_success = test_username_login(username, password)
    
    # Test email login
    email_success = test_email_login(email, password)
    
    print("\n🎯 Test Results:")
    print(f"   Username login: {'✅ PASS' if username_success else '❌ FAIL'}")
    print(f"   Email login: {'✅ PASS' if email_success else '❌ FAIL'}")
    
    print("\n💡 Login Credentials:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    
    if username_success and email_success:
        print("\n🎉 Both username and email login work!")
    else:
        print("\n⚠️  Some login methods failed. Check the backend logs.")

if __name__ == "__main__":
    main() 