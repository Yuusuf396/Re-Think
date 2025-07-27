#!/usr/bin/env python
"""
Script to create a test user for testing login functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from tracker.models import ImpactEntry

User = get_user_model()

def create_test_user():
    """Create a test user for login testing"""
    try:
        # Check if test user already exists
        username = 'adebayoayomide'
        if User.objects.filter(username=username).exists():
            print(f"✅ Test user '{username}' already exists")
            user = User.objects.get(username=username)
            print(f"   User ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Is Active: {user.is_active}")
            return user
        
        # Create test user
        user = User.objects.create_user(
            username=username,
            email='adebayo@example.com',
            password='123'  # Simple password for testing
        )
        
        print(f"✅ Created test user '{username}'")
        print(f"   User ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Password: 123")
        
        return user
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return None

def test_login():
    """Test login functionality"""
    try:
        from django.contrib.auth import authenticate
        
        # Test authentication
        user = authenticate(username='adebayoayomide', password='123')
        
        if user:
            print("✅ Login test successful!")
            print(f"   Authenticated user: {user.username}")
            return True
        else:
            print("❌ Login test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing login: {e}")
        return False

if __name__ == "__main__":
    print("Creating test user...")
    user = create_test_user()
    
    if user:
        print("\nTesting login...")
        test_login()
    
    print("\nTest user credentials:")
    print("Username: adebayoayomide")
    print("Password: 123")
    print("Email: adebayo@example.com") 