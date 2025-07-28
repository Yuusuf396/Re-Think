#!/usr/bin/env python3
"""
SQLite Database Setup - Simple and reliable
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Setup SQLite database"""
    print("🗄️ Setting up SQLite database...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
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
        
        print("✅ SQLite setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ SQLite setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 