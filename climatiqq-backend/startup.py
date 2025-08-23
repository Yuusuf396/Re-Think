#!/usr/bin/env python3
"""
Consolidated Startup Script for GreenTrack - Climatiqq

This script consolidates functionality from multiple startup scripts into one
clean, production-ready startup process. It handles database initialization,
migrations, user creation, and environment validation.

Features:
- Environment variable validation
- Database connection waiting with retry logic
- Automatic migration handling
- Test and admin user creation
- Comprehensive error handling and logging

Usage:
    python startup.py          # Full startup with all features
    python startup.py --quick  # Quick startup (migrations only)
    python startup.py --check  # Environment check only
"""

import os
import sys
import django
import time
import argparse
from django.core.management import execute_from_command_line
from django.db import connection

def check_environment():
    """Validate environment variables and configuration"""
    print("🔍 Checking environment configuration...")
    
    # Check critical environment variables
    env_vars = {
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DEBUG': os.getenv('DEBUG', 'False'),
        'PYTHON_VERSION': os.getenv('PYTHON_VERSION', sys.version.split()[0])
    }
    
    for var, value in env_vars.items():
        status = "✅ SET" if value else "❌ NOT SET"
        print(f"   {var}: {status}")
        if value and var != 'SECRET_KEY':  # Don't show secret key value
            print(f"      Value: {value}")
    
    # Validate Django settings
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        print("   Django Settings: ✅ VALID")
        return True
    except Exception as e:
        print(f"   Django Settings: ❌ INVALID - {e}")
        return False

def wait_for_database(max_attempts=15, delay=5):
    """Wait for database to be available with intelligent retry logic"""
    print("⏳ Waiting for database connection...")
    
    for attempt in range(max_attempts):
        try:
            print(f"   Attempt {attempt + 1}/{max_attempts}...")
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                print(f"   ✅ Database connection successful!")
                return True
                
        except Exception as e:
            print(f"   ⚠️ Attempt {attempt + 1}/{max_attempts}: Database not ready")
            print(f"      Error: {str(e)}")
            
            if attempt < max_attempts - 1:
                print(f"   ⏳ Waiting {delay} seconds before next attempt...")
                time.sleep(delay)
            else:
                print("   ❌ Database connection failed after all attempts")
                return False
    
    return False

def run_migrations(create_migrations=True):
    """Handle database migrations"""
    print("🗄️ Running database migrations...")
    
    try:
        if create_migrations:
            # Create migrations (development mode)
            print("   📝 Creating migrations...")
            execute_from_command_line(['manage.py', 'makemigrations', 'tracker', '--verbosity=1'])
        
        # Run migrations
        print("   🔄 Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=1'])
        
        print("   ✅ Migrations completed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Migration failed: {e}")
        return False

def create_users():
    """Create test and admin users using Django ORM directly"""
    print("👥 Creating users...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Create test user
        print("   👤 Creating test user...")
        if not User.objects.filter(username='adebayoayomide').exists():
            user = User.objects.create_user('adebayoayomide', 'adebayo@example.com', '123')
            print(f"      ✅ Test user created: {user.username}")
        else:
            print("      ✅ Test user already exists")
        
        # Create admin user
        print("   👑 Creating admin user...")
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print(f"      ✅ Admin user created: {user.username}")
        else:
            print("      ✅ Admin user already exists")
        
        print("   ✅ Users created successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ User creation failed: {e}")
        return False

def verify_database():
    """Verify database state and user count"""
    print("🔍 Verifying database state...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        users = User.objects.all()
        print(f"   ✅ Database has {users.count()} users:")
        
        for user in users:
            status = "👑 ADMIN" if user.is_superuser else "👤 USER"
            print(f"      - {user.username} ({user.email}) - {status}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Database verification failed: {e}")
        return False

def main():
    """Main startup function with command-line argument support"""
    parser = argparse.ArgumentParser(description='GreenTrack Startup Script')
    parser.add_argument('--quick', action='store_true', help='Quick startup (migrations only)')
    parser.add_argument('--check', action='store_true', help='Environment check only')
    parser.add_argument('--no-migrations', action='store_true', help='Skip creating migrations')
    
    args = parser.parse_args()
    
    print("🚀 GreenTrack - Climatiqq Startup")
    print("=" * 50)
    
    # Environment check
    if not check_environment():
        print("❌ Environment validation failed")
        return False
    
    if args.check:
        print("✅ Environment check completed")
        return True
    
    # Database connection
    if not wait_for_database():
        print("❌ Database connection failed")
        return False
    
    try:
        # Run migrations
        if not run_migrations(create_migrations=not args.no_migrations):
            return False
        
        # Create users (unless quick mode)
        if not args.quick:
            if not create_users():
                return False
            
            if not verify_database():
                return False
        
        print("✅ Startup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 