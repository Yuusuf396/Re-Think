#!/usr/bin/env python3
"""
Force run ALL Django migrations including auth tables
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

def main():
    """Force run all migrations"""
    print("🔧 Force running ALL migrations...")
    
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
    
    # Run ALL migrations (including Django auth)
    print("🗄️ Running ALL migrations...")
    try:
        # First, run Django's built-in migrations
        execute_from_command_line(['manage.py', 'migrate', 'auth', '--verbosity=2'])
        execute_from_command_line(['manage.py', 'migrate', 'contenttypes', '--verbosity=2'])
        execute_from_command_line(['manage.py', 'migrate', 'sessions', '--verbosity=2'])
        execute_from_command_line(['manage.py', 'migrate', 'admin', '--verbosity=2'])
        
        # Then run our app migrations
        execute_from_command_line(['manage.py', 'migrate', 'tracker', '--verbosity=2'])
        
        # Finally, run all migrations
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        
        print("✅ All migrations completed")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
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
                print("❌ auth_user table does not exist")
                return False
    except Exception as e:
        print(f"⚠️ Could not check auth_user table: {e}")
    
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
        return False
    
    # Final verification
    print("🔍 Final verification...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user;")
            count = cursor.fetchone()
            print(f"✅ Database has {count[0]} users")
            
            # List all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📋 Database tables: {[table[0] for table in tables]}")
            
    except Exception as e:
        print(f"❌ Final verification failed: {e}")
        return False
    
    print("✅ Database setup complete!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 