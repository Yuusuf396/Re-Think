#!/usr/bin/env python3
"""
Deployment Script for Rethink Backend
Helps prepare the application for production deployment
"""

import os
import sys
import subprocess
import django

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = ['SECRET_KEY', 'DEBUG']
    optional_vars = ['DATABASE_URL', 'ALLOWED_HOSTS', 'CORS_ALLOWED_ORIGINS']
    
    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("Please set these variables before deployment")
        return False
    
    print("✅ Environment variables check passed")
    return True

def collect_static():
    """Collect static files"""
    return run_command("python manage.py collectstatic --noinput", "Collecting static files")

def run_migrations():
    """Run database migrations"""
    return run_command("python manage.py migrate", "Running database migrations")

def create_superuser():
    """Create a superuser if needed"""
    print("👤 Superuser creation (optional)")
    create = input("Do you want to create a superuser? (y/n): ").strip().lower()
    
    if create == 'y':
        return run_command("python manage.py createsuperuser", "Creating superuser")
    else:
        print("⏭️ Skipping superuser creation")
        return True

def check_security():
    """Check security settings"""
    print("🔒 Checking security settings...")
    
    debug = os.getenv('DEBUG', 'False').lower()
    if debug == 'true':
        print("⚠️ WARNING: DEBUG is set to True. This is not recommended for production!")
        print("   Set DEBUG=False in production")
    
    secret_key = os.getenv('SECRET_KEY')
    if secret_key and 'insecure' in secret_key:
        print("⚠️ WARNING: Using default SECRET_KEY. Change this in production!")
    
    print("✅ Security check completed")

def main():
    """Main deployment function"""
    print("🚀 Rethink Backend Deployment")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        return False
    
    # Check security
    check_security()
    
    # Run migrations
    if not run_migrations():
        return False
    
    # Collect static files
    if not collect_static():
        return False
    
    # Create superuser (optional)
    if not create_superuser():
        return False
    
    print("\n🎉 Deployment preparation completed!")
    print("\n📋 Next steps:")
    print("1. Set up your production server")
    print("2. Configure your web server (nginx, etc.)")
    print("3. Set up SSL certificates")
    print("4. Configure your database")
    print("5. Set up monitoring and logging")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 