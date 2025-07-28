#!/usr/bin/env python3
"""
Simple startup script that works with any database
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Simple startup that works with any database"""
    print("🚀 Simple startup...")
    
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
        
        # 5. Show database info
        print("🔍 Database info...")
        execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

print(f"Database engine: {settings.DATABASES['default']['ENGINE']}")
print(f"Users count: {User.objects.count()}")
users = User.objects.all()
for user in users:
    print(f"  - {user.username} ({user.email})")
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