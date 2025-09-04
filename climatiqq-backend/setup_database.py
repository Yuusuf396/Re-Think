#!/usr/bin/env python3
"""
Database setup script for Climatiqq
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_database():
    """Setup the database with migrations"""
    print("🔄 Setting up database...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        django.setup()
        
        # Run migrations
        print("📦 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Create superuser if none exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            print("👑 Creating superuser...")
            execute_from_command_line(['manage.py', 'createsuperuser', '--noinput'])
            print("✅ Superuser created successfully!")
        else:
            print("✅ Superuser already exists")
            
        print("🎉 Database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_database()




