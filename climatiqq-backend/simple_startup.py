#!/usr/bin/env python3
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🚀 Simple startup...")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    try:
        # Only run migrations - no makemigrations in production
        print("🗄️ Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])

        # Create test and admin users with Django ORM directly (avoid multiple shell calls)
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if not User.objects.filter(username='adebayoayomide').exists():
            user = User.objects.create_user('adebayoayomide', 'adebayo@example.com', '123')
            print(f"✅ Test user created: {user.username}")
        else:
            print("✅ Test user already exists")

        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print(f"✅ Admin user created: {user.username}")
        else:
            print("✅ Admin user already exists")

        print("✅ Startup completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Startup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
