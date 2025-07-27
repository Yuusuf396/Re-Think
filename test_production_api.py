#!/usr/bin/env python3
"""
Test Production API
Checks if the deployed backend is working correctly
"""

import requests
import json

def test_production_api():
    """Test the production API endpoints"""
    base_url = "https://green-track.onrender.com/api/v1"
    
    print("🧪 Testing Production API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health/")
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type')}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Registration
    print("2. Testing Registration...")
    try:
        data = {
            "username": "testuser123",
            "password": "testpass123",
            "email": "test@example.com"
        }
        response = requests.post(f"{base_url}/register/", json=data)
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type')}")
        if response.status_code == 201:
            print(f"   Success: User registered")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Login
    print("3. Testing Login...")
    try:
        data = {
            "username": "testuser123",
            "password": "testpass123"
        }
        response = requests.post(f"{base_url}/login/", json=data)
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type')}")
        if response.status_code == 200:
            print(f"   Success: Login successful")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("=" * 50)
    print("✅ Production API Test Complete")

if __name__ == "__main__":
    test_production_api() 