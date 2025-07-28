#!/usr/bin/env python3
"""
Simple database fix - just run the basics
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Simple database setup"""
    print("🔧 Simple database fix...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    try:
        # 1. Make migrations
        print("📝 Making migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # 2. Run migrations
        print("🗄️ Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # 3. Create superuser
        print("👑 Creating superuser...")
        execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created")
else:
    print("Superuser exists")
'''])
        
        # 4. Create test user
        print("👤 Creating test user...")
        execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='adebayoayomide').exists():
    User.objects.create_user('adebayoayomide', 'adebayo@example.com', '123')
    print("Test user created")
else:
    print("Test user exists")
'''])
        
        print("✅ Simple fix completed!")
        return True
        
    except Exception as e:
        print(f"❌ Simple fix failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 