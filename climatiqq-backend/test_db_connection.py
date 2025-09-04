#!/usr/bin/env python3
"""
Simple test script to verify Supabase database connection
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_database_connection():
    """Test the database connection using Django settings"""
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        
        # Import Django and setup
        import django
        django.setup()
        
        print("✅ Django setup successful!")
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"✅ Database connection successful!")
            print(f"📋 PostgreSQL Version: {version}")
            
            # Test a simple query
            cursor.execute("SELECT current_database(), current_user, inet_server_addr()")
            db_info = cursor.fetchone()
            print(f"📁 Database: {db_info[0]}")
            print(f"👤 User: {db_info[1]}")
            print(f"🌐 Server: {db_info[2]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🧪 Testing Supabase Database Connection...")
    success = test_database_connection()
    
    if success:
        print("\n🎉 Database connection test passed!")
    else:
        print("\n❌ Database connection test failed!")
        sys.exit(1)
