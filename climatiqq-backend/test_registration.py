#!/usr/bin/env python3
"""
Test script to debug user registration
"""
import requests
import json

def test_registration():
    """Test the registration endpoint"""
    url = "http://localhost:8000/api/v1/register/"
    
    # Test data
    test_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }
    
    print(f"Testing registration with data: {test_data}")
    print(f"URL: {url}")
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            data = response.json()
            print(f"User created: {data.get('user', {}).get('username')}")
            print(f"Access token: {data.get('access', '')[:20]}...")
        else:
            print("❌ Registration failed!")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Raw error response: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_registration()




