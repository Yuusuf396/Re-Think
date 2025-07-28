#!/usr/bin/env python3
"""
Test login functionality
"""

import os
import sys
import django
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

def main():
    """Test login functionality"""
    print("🧪 Testing login functionality...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    User = get_user_model()
    
    # Check if test user exists
    try:
        user = User.objects.get(username='adebayoayomide')
        print(f"✅ Test user exists: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Is active: {user.is_active}")
        
        # Test authentication
        auth_user = authenticate(username='adebayoayomide', password='123')
        if auth_user:
            print("✅ Authentication successful!")
        else:
            print("❌ Authentication failed!")
            return False
            
    except User.DoesNotExist:
        print("❌ Test user does not exist!")
        return False
    except Exception as e:
        print(f"❌ Error testing login: {e}")
        return False
    
    print("✅ Login test passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 