#!/usr/bin/env python3
"""
Test WSGI Configuration
Verifies that the Django application can be loaded correctly
"""

import os
import sys

def test_wsgi():
    """Test the WSGI configuration"""
    print("🧪 Testing WSGI Configuration...")
    
    try:
        # Add the backend directory to Python path
        backend_path = os.path.join(os.path.dirname(__file__), 'climatiqq-backend')
        sys.path.insert(0, backend_path)
        
        # Change to backend directory
        os.chdir(backend_path)
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        
        # Import Django
        import django
        django.setup()
        
        # Import the WSGI application
        from config.wsgi import application
        
        print("✅ WSGI Configuration Test Successful!")
        print(f"✅ Django version: {django.get_version()}")
        print(f"✅ Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
        print(f"✅ Application loaded: {type(application)}")
        
        return True
        
    except Exception as e:
        print(f"❌ WSGI Configuration Test Failed: {e}")
        return False

if __name__ == "__main__":
    success = test_wsgi()
    sys.exit(0 if success else 1) 