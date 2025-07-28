#!/usr/bin/env python3
"""
EMERGENCY Database Fix - Creates tables manually if migrations fail
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection, migrations
from django.db.models import Model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from tracker.models import ImpactEntry

def create_tables_manually():
    """Create tables manually if migrations fail"""
    print("🚨 EMERGENCY: Creating tables manually...")
    
    try:
        # Create auth_user table manually
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_user (
                    id SERIAL PRIMARY KEY,
                    password VARCHAR(128) NOT NULL,
                    last_login TIMESTAMP WITH TIME ZONE,
                    is_superuser BOOLEAN NOT NULL,
                    username VARCHAR(150) UNIQUE NOT NULL,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    email VARCHAR(254) NOT NULL,
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined TIMESTAMP WITH TIME ZONE NOT NULL
                );
            """)
            
            # Create auth_group table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_group (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(150) UNIQUE NOT NULL
                );
            """)
            
            # Create auth_permission table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_permission (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    content_type_id INTEGER NOT NULL,
                    codename VARCHAR(100) NOT NULL
                );
            """)
            
            # Create django_content_type table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS django_content_type (
                    id SERIAL PRIMARY KEY,
                    app_label VARCHAR(100) NOT NULL,
                    model VARCHAR(100) NOT NULL,
                    UNIQUE(app_label, model)
                );
            """)
            
            # Create tracker_impactentry table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracker_impactentry (
                    id SERIAL PRIMARY KEY,
                    metric_type VARCHAR(20) NOT NULL,
                    value DOUBLE PRECISION NOT NULL,
                    description VARCHAR(200) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    user_id INTEGER NOT NULL
                );
            """)
            
            print("✅ Tables created manually")
            return True
            
    except Exception as e:
        print(f"❌ Manual table creation failed: {e}")
        return False

def create_superuser():
    """Create a superuser manually"""
    print("👑 Creating superuser...")
    
    try:
        # Check if user exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user WHERE username = 'admin';")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Create superuser manually
                cursor.execute("""
                    INSERT INTO auth_user (
                        username, email, password, is_superuser, 
                        is_staff, is_active, date_joined, first_name, last_name
                    ) VALUES (
                        'admin', 'admin@example.com', 
                        'pbkdf2_sha256$600000$dummy$dummy', 
                        true, true, true, NOW(), '', ''
                    );
                """)
                print("✅ Superuser created")
            else:
                print("✅ Superuser already exists")
                
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False
    
    return True

def create_test_user():
    """Create test user manually"""
    print("👤 Creating test user...")
    
    try:
        # Check if user exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user WHERE username = 'adebayoayomide';")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Create test user manually
                cursor.execute("""
                    INSERT INTO auth_user (
                        username, email, password, is_superuser, 
                        is_staff, is_active, date_joined, first_name, last_name
                    ) VALUES (
                        'adebayoayomide', 'adebayo@example.com', 
                        'pbkdf2_sha256$600000$dummy$dummy', 
                        false, false, true, NOW(), '', ''
                    );
                """)
                print("✅ Test user created")
            else:
                print("✅ Test user already exists")
                
    except Exception as e:
        print(f"❌ Test user creation failed: {e}")
        return False
    
    return True

def main():
    """Emergency database fix"""
    print("🚨 EMERGENCY DATABASE FIX")
    print("=" * 50)
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Check database connection
    print("📊 Checking database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Database connected: {version[0]}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Try normal migrations first
    print("🗄️ Trying normal migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        print("✅ Normal migrations succeeded")
    except Exception as e:
        print(f"⚠️ Normal migrations failed: {e}")
        print("🚨 Switching to emergency mode...")
        
        # Create tables manually
        if not create_tables_manually():
            return False
    
    # Create users
    if not create_superuser():
        return False
    
    if not create_test_user():
        return False
    
    # Final verification
    print("🔍 Final verification...")
    try:
        with connection.cursor() as cursor:
            # Check auth_user table
            cursor.execute("SELECT COUNT(*) FROM auth_user;")
            user_count = cursor.fetchone()[0]
            print(f"✅ Database has {user_count} users")
            
            # List all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            tables = cursor.fetchall()
            print(f"📋 Database tables: {[table[0] for table in tables]}")
            
    except Exception as e:
        print(f"❌ Final verification failed: {e}")
        return False
    
    print("✅ EMERGENCY DATABASE FIX COMPLETE!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 