#!/usr/bin/env python3
"""
Create test user for the application
"""

import os
import django
from django.contrib.auth import get_user_model

def main():
    """Create test user"""
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    User = get_user_model()
    
    # Create test user
    username = 'adebayoayomide'
    email = 'adebayo@example.com'
    password = '123'
    
    if not User.objects.filter(username=username).exists():
        print(f"👤 Creating test user: {username}")
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Test user created: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
    else:
        print(f"👤 Test user already exists: {username}")
    
    # List all users
    print("\n📋 All users:")
    for user in User.objects.all():
        print(f"   - {user.username} ({user.email})")

if __name__ == "__main__":
    main() 