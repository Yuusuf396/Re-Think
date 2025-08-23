#!/usr/bin/env python3
"""
Consolidated Database Management Script for GreenTrack - Climatiqq

This script consolidates all database-related functionality into one
comprehensive database management tool. It handles migrations, setup,
debugging, and emergency fixes.

Features:
- Database setup and initialization
- Migration management (create, run, force)
- Database debugging and health checks
- Emergency database fixes
- User management

Usage:
    python manage_db.py setup          # Setup database with migrations and users
    python manage_db.py migrate        # Run migrations only
    python manage_db.py makemigrations # Create migrations only
    python manage_db.py debug          # Debug database issues
    python manage_db.py fix            # Emergency database fixes
    python manage_db.py users          # Manage users
    python manage_db.py status         # Check database status
"""

import os
import sys
import django
import argparse
from django.core.management import execute_from_command_line
from django.db import connection, IntegrityError
from django.contrib.auth import get_user_model

def setup_django():
    """Initialize Django environment"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def check_database_connection():
    """Check if database is accessible"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Database connection: SUCCESS (Result: {result})")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_migrations():
    """Create new migrations for the tracker app"""
    print("📝 Creating migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'tracker', '--verbosity=1'])
        print("✅ Migrations created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create migrations: {e}")
        return False

def run_migrations():
    """Run all pending migrations"""
    print("🗄️ Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=1'])
        print("✅ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to run migrations: {e}")
        return False

def force_migrate():
    """Force run migrations (emergency use)"""
    print("⚠️  Force running migrations...")
    try:
        # Try to fake initial migration if needed
        execute_from_command_line(['manage.py', 'migrate', '--fake-initial'])
        # Run normal migrations
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        print("✅ Force migrations completed!")
        return True
    except Exception as e:
        print(f"❌ Force migrations failed: {e}")
        return False

def create_users():
    """Create test and admin users"""
    print("👥 Creating users...")
    
    try:
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

def debug_database():
    """Debug database issues"""
    print("🔍 Debugging database...")
    
    try:
        # Check connection
        if not check_database_connection():
            return False
        
        # Check Django models
        User = get_user_model()
        print("   ✅ Django models accessible")
        
        # Check user count
        user_count = User.objects.count()
        print(f"   📊 User count: {user_count}")
        
        # Check migrations
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connection
        
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"   ⚠️  {len(plan)} pending migrations:")
            for migration, backwards in plan:
                print(f"      - {migration}")
        else:
            print("   ✅ All migrations are up to date")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Database debug failed: {e}")
        return False

def emergency_fix():
    """Emergency database fixes"""
    print("🚨 Emergency database fixes...")
    
    try:
        # Try to reset migrations
        print("   🔄 Attempting to reset migrations...")
        
        # Check if we can access the database
        if not check_database_connection():
            print("   ❌ Cannot connect to database")
            return False
        
        # Try to fake initial migration
        print("   🎭 Faking initial migration...")
        execute_from_command_line(['manage.py', 'migrate', '--fake-initial'])
        
        # Run migrations
        print("   🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("   ✅ Emergency fixes completed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Emergency fixes failed: {e}")
        return False

def check_status():
    """Check overall database status"""
    print("📊 Database Status Check")
    print("=" * 40)
    
    # Django setup
    if not setup_django():
        print("❌ Django not accessible")
        return False
    
    # Connection check
    connection_ok = check_database_connection()
    
    # Model check
    try:
        User = get_user_model()
        user_count = User.objects.count()
        model_ok = True
    except Exception as e:
        user_count = 0
        model_ok = False
    
    # Migration check
    try:
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connection
        
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        migration_ok = len(plan) == 0
    except Exception as e:
        migration_ok = False
        plan = []
    
    # Status summary
    print(f"   Database Connection: {'✅ OK' if connection_ok else '❌ FAILED'}")
    print(f"   Django Models: {'✅ OK' if model_ok else '❌ FAILED'}")
    print(f"   Migrations: {'✅ UP TO DATE' if migration_ok else '⚠️  PENDING'}")
    print(f"   User Count: {user_count}")
    
    if plan:
        print(f"   Pending Migrations: {len(plan)}")
        for migration, backwards in plan:
            print(f"      - {migration}")
    
    overall_status = connection_ok and model_ok
    if overall_status:
        print("\n✅ Database is healthy!")
    else:
        print("\n⚠️  Database has issues that need attention")
    
    return overall_status

def setup_database():
    """Complete database setup"""
    print("🚀 Setting up database...")
    
    if not setup_django():
        return False
    
    try:
        # Create migrations
        if not create_migrations():
            return False
        
        # Run migrations
        if not run_migrations():
            return False
        
        # Create users
        if not create_users():
            return False
        
        # Verify status
        print("\n🔍 Verifying setup...")
        if check_status():
            print("✅ Database setup completed successfully!")
            return True
        else:
            print("⚠️  Setup completed but database has issues")
            return False
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def main():
    """Main function with command-line argument support"""
    parser = argparse.ArgumentParser(description='GreenTrack Database Management')
    parser.add_argument('command', choices=[
        'setup', 'migrate', 'makemigrations', 'debug', 
        'fix', 'users', 'status'
    ], help='Database management command')
    
    args = parser.parse_args()
    
    print("🗄️ GreenTrack - Climatiqq Database Management")
    print("=" * 50)
    
    if args.command == 'setup':
        return setup_database()
    
    elif args.command == 'migrate':
        if not setup_django():
            return False
        return run_migrations()
    
    elif args.command == 'makemigrations':
        if not setup_django():
            return False
        return create_migrations()
    
    elif args.command == 'debug':
        if not setup_django():
            return False
        return debug_database()
    
    elif args.command == 'fix':
        if not setup_django():
            return False
        return emergency_fix()
    
    elif args.command == 'users':
        if not setup_django():
            return False
        return create_users()
    
    elif args.command == 'status':
        return check_status()
    
    else:
        print(f"❌ Unknown command: {args.command}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
