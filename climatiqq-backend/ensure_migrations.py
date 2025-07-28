#!/usr/bin/env python3
"""
Ensure migrations run properly and create all database tables
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

def main():
    """Ensure all migrations are applied"""
    print("🔧 Ensuring database migrations...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Check database connection
    print("📊 Checking database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Database connected: {version[0]}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Check if auth_user table exists
    print("📋 Checking auth_user table...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
            tables = cursor.fetchall()
            if tables:
                print("✅ auth_user table exists")
            else:
                print("❌ auth_user table does not exist - running migrations...")
    except Exception as e:
        print(f"⚠️ Could not check auth_user table: {e}")
    
    # Run migrations with maximum verbosity
    print("🗄️ Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=3'])
        print("✅ Migrations completed")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    # Check migration status
    print("📊 Migration status:")
    try:
        execute_from_command_line(['manage.py', 'showmigrations'])
    except Exception as e:
        print(f"⚠️ Could not show migrations: {e}")
    
    # Create test user
    print("👤 Creating test user...")
    try:
        execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='adebayoayomide').exists():
    user = User.objects.create_user('adebayoayomide', 'adebayo@example.com', '123')
    print(f"✅ Test user created: {user.username}")
else:
    print("✅ Test user already exists")
'''])
    except Exception as e:
        print(f"❌ Could not create test user: {e}")
    
    # Final check
    print("🔍 Final database check...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user;")
            count = cursor.fetchone()
            print(f"✅ Database has {count[0]} users")
    except Exception as e:
        print(f"❌ Final check failed: {e}")
        return False
    
    print("✅ Database setup complete!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 