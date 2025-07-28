#!/usr/bin/env python3
"""
Debug database connection and environment variables
"""

import os
import sys

def main():
    """Debug database connection"""
    print("🔍 Debugging database connection...")
    
    # Check environment variables
    print("📋 Environment variables:")
    print(f"   DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")
    print(f"   DEBUG: {os.getenv('DEBUG', 'NOT SET')}")
    print(f"   SECRET_KEY: {os.getenv('SECRET_KEY', 'NOT SET')}")
    
    # Try to import Django and check database
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        from django.conf import settings
        print(f"📊 Database configuration:")
        print(f"   ENGINE: {settings.DATABASES['default']['ENGINE']}")
        print(f"   NAME: {settings.DATABASES['default'].get('NAME', 'NOT SET')}")
        print(f"   HOST: {settings.DATABASES['default'].get('HOST', 'NOT SET')}")
        print(f"   PORT: {settings.DATABASES['default'].get('PORT', 'NOT SET')}")
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Database connected: {version[0]}")
            
            # Check if auth_user table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
            tables = cursor.fetchall()
            if tables:
                print("✅ auth_user table exists")
            else:
                print("❌ auth_user table does not exist")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    print("✅ Database debug complete!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 