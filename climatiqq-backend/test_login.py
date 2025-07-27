#!/usr/bin/env python3
"""
Simple script to test login functionality and create test users
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
    """Create a test user for login testing"""
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists")
        return username, password
    
    # Create new user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Created test user: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    return username, password

def test_login(username, password):
    """Test login with given credentials"""
    print(f"\n🔐 Testing login with: {username}")
    
    # Test Django authentication
    user = authenticate(username=username, password=password)
    if user:
        print(f"✅ Authentication successful!")
        print(f"   User ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Is Active: {user.is_active}")
        return True
    else:
        print(f"❌ Authentication failed!")
        return False

def list_all_users():
    """List all users in the database"""
    print("\n📋 All users in database:")
    users = User.objects.all()
    
    if not users.exists():
        print("   No users found")
        return
    
    for user in users:
        print(f"   ID: {user.id}, Username: {user.username}, Email: {user.email}, Active: {user.is_active}")

def main():
    print("🌱 Rethink - Login Test Script")
    print("=" * 40)
    
    # List existing users
    list_all_users()
    
    # Create test user
    username, password = create_test_user()
    
    # Test login
    test_login(username, password)
    
    print("\n🎯 Test Credentials:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   Email: test@example.com")
    
    print("\n💡 Try logging in with these credentials in your app!")

if __name__ == "__main__":
    main() 