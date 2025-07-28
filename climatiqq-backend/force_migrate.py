#!/usr/bin/env python3
"""
Force run migrations and check database status
"""

import os
import django
from django.core.management import execute_from_command_line
from django.db import connection

def main():
    """Force run migrations"""
    print("🔧 Force running migrations...")
    
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
        return
    
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
    except Exception as e:
        print(f"⚠️ Could not check auth_user table: {e}")
    
    # Run migrations with verbosity
    print("🗄️ Running migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
    
    # Check migration status
    print("📊 Migration status:")
    execute_from_command_line(['manage.py', 'showmigrations'])
    
    # Create test user
    print("👤 Creating test user...")
    execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='adebayoayomide').exists():
    user = User.objects.create_user('adebayoayomide', 'adebayo@example.com', '123')
    print(f"✅ Test user created: {user.username}")
else:
    print("✅ Test user already exists")
'''])
    
    print("✅ Migration process complete!")

if __name__ == "__main__":
    main() 