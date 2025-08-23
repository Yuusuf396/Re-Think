#!/usr/bin/env python3
"""
Consolidated System Test Script for GreenTrack - Climatiqq

This script consolidates all testing functionality into one comprehensive
test suite. It tests authentication, API endpoints, database connectivity,
and system health.

Features:
- Environment validation
- Database connectivity testing
- User authentication testing
- API endpoint testing
- System health checks

Usage:
    python test_system.py          # Run all tests
    python test_system.py --auth  # Authentication tests only
    python test_system.py --api   # API tests only
    python test_system.py --db    # Database tests only
"""

import os
import sys
import django
import requests
import argparse
from django.contrib.auth import authenticate, get_user_model
from django.db import connection

def setup_django():
    """Initialize Django environment"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("🔍 Testing environment configuration...")
    
    env_vars = {
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DEBUG': os.getenv('DEBUG', 'False'),
        'PYTHON_VERSION': os.getenv('PYTHON_VERSION', sys.version.split()[0])
    }
    
    all_good = True
    for var, value in env_vars.items():
        if value:
            print(f"   ✅ {var}: SET")
        else:
            print(f"   ❌ {var}: NOT SET")
            all_good = False
    
    if all_good:
        print("   ✅ Environment configuration is valid")
    else:
        print("   ⚠️  Some environment variables are missing")
    
    return all_good

def test_database():
    """Test database connectivity and basic operations"""
    print("🗄️ Testing database connectivity...")
    
    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"   ✅ Database connection: SUCCESS (Result: {result})")
        
        # Test user model access
        User = get_user_model()
        user_count = User.objects.count()
        print(f"   ✅ User model access: SUCCESS ({user_count} users)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        return False

def test_authentication():
    """Test user authentication functionality"""
    print("🔐 Testing authentication system...")
    
    try:
        User = get_user_model()
        
        # Check if test user exists
        try:
            user = User.objects.get(username='adebayoayomide')
            print(f"   ✅ Test user exists: {user.username}")
            print(f"      Email: {user.email}")
            print(f"      Is active: {user.is_active}")
            
            # Test authentication
            auth_user = authenticate(username='adebayoayomide', password='123')
            if auth_user:
                print("   ✅ Authentication: SUCCESS")
            else:
                print("   ❌ Authentication: FAILED")
                return False
                
        except User.DoesNotExist:
            print("   ⚠️  Test user does not exist - creating one...")
            user = User.objects.create_user('adebayoayomide', 'adebayo@example.com', '123')
            print(f"      ✅ Test user created: {user.username}")
            
            # Test authentication for new user
            auth_user = authenticate(username='adebayoayomide', password='123')
            if auth_user:
                print("   ✅ Authentication: SUCCESS")
            else:
                print("   ❌ Authentication: FAILED")
                return False
        
        # Check if admin user exists
        try:
            admin_user = User.objects.get(username='admin')
            print(f"   ✅ Admin user exists: {admin_user.username}")
        except User.DoesNotExist:
            print("   ⚠️  Admin user does not exist")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Authentication test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints if server is running"""
    print("🌐 Testing API endpoints...")
    
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        "/api/v1/health/",
        "/api/v1/auth/login/",
        "/api/v1/ai-suggestions/"
    ]
    
    all_good = True
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint}: SUCCESS (200)")
            elif response.status_code == 401:
                print(f"   ⚠️  {endpoint}: UNAUTHORIZED (401) - requires authentication")
            else:
                print(f"   ❌ {endpoint}: FAILED ({response.status_code})")
                all_good = False
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  {endpoint}: SERVER NOT RUNNING")
            all_good = False
        except Exception as e:
            print(f"   ❌ {endpoint}: ERROR - {e}")
            all_good = False
    
    if all_good:
        print("   ✅ API endpoint tests completed")
    else:
        print("   ⚠️  Some API tests failed")
    
    return all_good

def test_ai_model():
    """Test the AI recommendation model"""
    print("🤖 Testing AI recommendation model...")
    
    try:
        from tracker.ai_model import carbon_ai_model
        
        # Test data
        test_data = {
            'entries': [
                {'carbon_footprint': 25, 'water_usage': 200, 'energy_usage': 15, 'created_at': '2024-01-01T10:00:00Z'},
                {'carbon_footprint': 15, 'water_usage': 150, 'energy_usage': 10, 'created_at': '2024-01-02T10:00:00Z'}
            ]
        }
        
        # Generate suggestions
        result = carbon_ai_model.predict_suggestions(test_data)
        
        if result.get('suggestions'):
            suggestion_count = len(result['suggestions'])
            print(f"   ✅ AI model: SUCCESS ({suggestion_count} suggestions generated)")
            print(f"      Model type: {result.get('model_type', 'Unknown')}")
            print(f"      Confidence: {result.get('confidence', 0)}")
        else:
            print("   ❌ AI model: FAILED - no suggestions generated")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ AI model test failed: {e}")
        return False

def run_all_tests():
    """Run all system tests"""
    print("🧪 GreenTrack - Climatiqq System Test Suite")
    print("=" * 60)
    
    # Environment test
    env_ok = test_environment()
    
    # Django setup
    if not setup_django():
        print("❌ Django setup failed - cannot continue")
        return False
    
    # Database test
    db_ok = test_database()
    
    # Authentication test
    auth_ok = test_authentication()
    
    # AI model test
    ai_ok = test_ai_model()
    
    # API test (only if server might be running)
    api_ok = test_api_endpoints()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 40)
    print(f"   Environment: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"   Database: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"   Authentication: {'✅ PASS' if auth_ok else '❌ FAIL'}")
    print(f"   AI Model: {'✅ PASS' if ai_ok else '❌ FAIL'}")
    print(f"   API Endpoints: {'✅ PASS' if api_ok else '⚠️  PARTIAL'}")
    
    # Overall result
    core_tests = [env_ok, db_ok, auth_ok, ai_ok]
    if all(core_tests):
        print("\n🎉 All core tests passed! System is ready.")
        return True
    else:
        print("\n⚠️  Some core tests failed. Check the issues above.")
        return False

def main():
    """Main test function with command-line argument support"""
    parser = argparse.ArgumentParser(description='GreenTrack System Test Suite')
    parser.add_argument('--auth', action='store_true', help='Authentication tests only')
    parser.add_argument('--api', action='store_true', help='API tests only')
    parser.add_argument('--db', action='store_true', help='Database tests only')
    parser.add_argument('--ai', action='store_true', help='AI model tests only')
    
    args = parser.parse_args()
    
    if args.auth:
        # Authentication tests only
        if not setup_django():
            return False
        return test_authentication()
    
    elif args.api:
        # API tests only
        return test_api_endpoints()
    
    elif args.db:
        # Database tests only
        if not setup_django():
            return False
        return test_database()
    
    elif args.ai:
        # AI model tests only
        if not setup_django():
            return False
        return test_ai_model()
    
    else:
        # Run all tests
        return run_all_tests()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
