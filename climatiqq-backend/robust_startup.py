#!/usr/bin/env python3
"""
Robust startup script with better database handling
"""

import os
import sys
import django
import time
import subprocess
from django.core.management import execute_from_command_line
from django.db import connection

def check_environment():
    """Check environment variables"""
    print("🔍 Checking environment...")
    print(f"   DATABASE_URL: {'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")
    print(f"   SECRET_KEY: {'SET' if os.getenv('SECRET_KEY') else 'NOT SET'}")
    print(f"   DEBUG: {os.getenv('DEBUG', 'False')}")
    print(f"   PYTHON_VERSION: {os.getenv('PYTHON_VERSION', 'Unknown')}")

def wait_for_database(max_attempts=20, delay=10):
    """Wait for database to be available with better error handling"""
    print("⏳ Waiting for database connection...")
    
    for attempt in range(max_attempts):
        try:
            print(f"   Attempt {attempt + 1}/{max_attempts}...")
            
            # Test basic connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                print(f"   ✅ Database connection successful! Result: {result}")
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

def run_migrations():
    """Run database migrations"""
    print("🗄️ Running database migrations...")
    
    try:
        # Make migrations first
        print("   📝 Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', 'tracker', '--verbosity=2'])
        
        # Run migrations
        print("   🔄 Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        
        print("   ✅ Migrations completed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Migration failed: {e}")
        return False

def create_users():
    """Create test and admin users"""
    print("👥 Creating users...")
    
    try:
        # Create test user
        print("   👤 Creating test user...")
        execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='adebayoayomide').exists():
    user = User.objects.create_user('adebayoayomide', 'adebayo@example.com', '123')
    print(f"✅ Test user created: {user.username}")
else:
    print("✅ Test user already exists")
'''])
        
        # Create admin user
        print("   👑 Creating admin user...")
        execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print(f"✅ Admin user created: {user.username}")
else:
    print("✅ Admin user already exists")
'''])
        
        print("   ✅ Users created successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ User creation failed: {e}")
        return False

def verify_database():
    """Verify database setup"""
    print("🔍 Verifying database setup...")
    
    try:
        execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth import get_user_model
from tracker.models import ImpactEntry
User = get_user_model()

print("📊 Database verification:")
print(f"   Users: {User.objects.count()}")
print(f"   Impact entries: {ImpactEntry.objects.count()}")

users = User.objects.all()
print("   User list:")
for user in users:
    print(f"     - {user.username} ({user.email})")
'''])
        
        print("   ✅ Database verification completed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Database verification failed: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 ROBUST STARTUP SCRIPT")
    print("=" * 50)
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        django.setup()
        print("✅ Django setup successful")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    # Check environment
    check_environment()
    
    # Wait for database with more attempts
    if not wait_for_database(max_attempts=20, delay=10):
        print("❌ Cannot proceed without database connection")
        return False
    
    # Run migrations
    if not run_migrations():
        print("❌ Cannot proceed without migrations")
        return False
    
    # Create users
    if not create_users():
        print("❌ Cannot proceed without users")
        return False
    
    # Verify everything
    if not verify_database():
        print("❌ Database verification failed")
        return False
    
    print("✅ ROBUST STARTUP COMPLETED SUCCESSFULLY!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("❌ Startup failed - exiting")
        sys.exit(1)
    else:
        print("✅ Startup successful - ready to start server") 