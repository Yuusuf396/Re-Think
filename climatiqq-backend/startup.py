#!/usr/bin/env python3
"""
Startup script - Initialize database and start server
"""

import os
import sys
import django
import time
from django.core.management import execute_from_command_line
from django.db import connection

def wait_for_database(max_attempts=10, delay=5):
    """Wait for database to be available"""
    print("⏳ Waiting for database connection...")
    for attempt in range(max_attempts):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("✅ Database connection successful!")
                return True
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1}/{max_attempts}: Database not ready ({e})")
            if attempt < max_attempts - 1:
                print(f"⏳ Waiting {delay} seconds...")
                time.sleep(delay)
    print("❌ Database connection failed after all attempts")
    return False

def main():
    """Initialize database and start server"""
    print("🚀 Starting up...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Wait for database
    if not wait_for_database():
        return False
    
    try:
        # 1. Make migrations
        print("📝 Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', 'tracker'])
        
        # 2. Run migrations
        print("🗄️ Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # 3. Create test user
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
        
        # 4. Create admin user
        print("👑 Creating admin user...")
        execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print(f"✅ Admin user created: {user.username}")
else:
    print("✅ Admin user already exists")
'''])
        
        # 5. Verify database
        print("🔍 Verifying database...")
        execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()
print(f"✅ Database has {users.count()} users:")
for user in users:
    print(f"   - {user.username} ({user.email})")
'''])
        
        print("✅ Startup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 