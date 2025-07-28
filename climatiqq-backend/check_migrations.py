#!/usr/bin/env python3
"""
Check and run migrations on production database
"""

import os
import django
from django.core.management import execute_from_command_line

def main():
    """Check and run migrations"""
    print("🔍 Checking database migrations...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Check migration status
    print("📊 Checking migration status...")
    execute_from_command_line(['manage.py', 'showmigrations'])
    
    # Run migrations
    print("🗄️ Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Check migration status again
    print("📊 Final migration status...")
    execute_from_command_line(['manage.py', 'showmigrations'])
    
    print("✅ Migration check complete!")

if __name__ == "__main__":
    main() 