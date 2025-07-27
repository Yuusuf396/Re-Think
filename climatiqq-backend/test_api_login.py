#!/usr/bin/env python3
"""
Test the actual API login endpoint with both username and email
"""

import requests
import json

def test_api_login(username_or_email, password):
    """Test the API login endpoint"""
    url = "http://127.0.0.1:8000/api/v1/auth/login/"
    
    data = {
        "username": username_or_email,
        "password": password
    }
    
    print(f"🔐 Testing API login with: {username_or_email}")
    
    try:
        response = requests.post(url, json=data)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Login successful!")
            print(f"   Access token: {result.get('access', 'N/A')[:20]}...")
            return True
        else:
            print(f"   ❌ Login failed!")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection error - make sure the server is running!")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    print("🌱 Rethink - API Login Test")
    print("=" * 40)
    
    # Test credentials
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
    
    print("\n📋 Testing API login endpoints...")
    
    # Test username login
    username_success = test_api_login(username, password)
    
    # Test email login
    email_success = test_api_login(email, password)
    
    print("\n🎯 API Test Results:")
    print(f"   Username login: {'✅ PASS' if username_success else '❌ FAIL'}")
    print(f"   Email login: {'✅ PASS' if email_success else '❌ FAIL'}")
    
    print("\n💡 Test Credentials:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    
    if username_success and email_success:
        print("\n🎉 Both username and email API login work!")
    else:
        print("\n⚠️  Some API login methods failed.")
        print("   Make sure the Django server is running on http://127.0.0.1:8000")

if __name__ == "__main__":
    main() 