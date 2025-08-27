#!/usr/bin/env python
"""
Django Settings Update Script for Supabase PostgreSQL
Run this script to update your Django settings for Supabase database connection.
"""

import os
import sys
from pathlib import Path

def update_django_settings():
    """Update Django settings for Supabase PostgreSQL"""
    
    print("🚀 Updating Django Settings for Supabase PostgreSQL...")
    
    # Path to your settings file
    settings_file = Path("config/settings.py")
    
    if not settings_file.exists():
        print("❌ Error: config/settings.py not found!")
        return False
    
    # Read current settings
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already configured for PostgreSQL
    if "django.db.backends.postgresql" in content:
        print("✅ PostgreSQL is already configured in settings.py")
        return True
    
    # Find the database configuration section
    db_start = content.find("# Database")
    if db_start == -1:
        db_start = content.find("DATABASE_URL")
    
    if db_start == -1:
        print("❌ Error: Could not find database configuration section")
        return False
    
    # Find the end of database section
    db_end = content.find("\n\n", db_start)
    if db_end == -1:
        db_end = len(content)
    
    # New PostgreSQL configuration
    postgresql_config = '''# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Supabase PostgreSQL Configuration
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL and DATABASE_URL.startswith('postgres'):
    # PostgreSQL configuration for Supabase
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
    print("✅ Using Supabase PostgreSQL database")
else:
    # Fallback to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("🔄 Using SQLite database for development (set DATABASE_URL for Supabase)")'''
    
    # Replace the database section
    new_content = content[:db_start] + postgresql_config + content[db_end:]
    
    # Write updated settings
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Successfully updated Django settings for Supabase PostgreSQL")
    return True

def create_env_template():
    """Create environment template for Supabase"""
    
    print("\n📝 Creating environment template for Supabase...")
    
    env_template = """# Supabase PostgreSQL Configuration
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

# SendGrid Configuration (keep your existing settings)
SENDGRID_API_KEY=SG.your_sendgrid_api_key_here
DEFAULT_FROM_EMAIL=noreply@climatiqq.com
SUPPORT_EMAIL=support@climatiqq.com
FRONTEND_URL=http://localhost:3000

# Email Backend
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Django Settings
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Supabase Additional Settings
SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
SUPABASE_ANON_KEY=[YOUR-ANON-KEY]
SUPABASE_SERVICE_ROLE_KEY=[YOUR-SERVICE-ROLE-KEY]
"""
    
    with open("env.supabase", "w", encoding="utf-8") as f:
        f.write(env_template)
    
    print("✅ Created env.supabase template")
    print("📋 Update this file with your actual Supabase credentials")

def update_requirements():
    """Update requirements.txt for PostgreSQL support"""
    
    print("\n📦 Updating requirements.txt for PostgreSQL...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found!")
        return False
    
    # Read current requirements
    with open(requirements_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if psycopg2 is already there
    if "psycopg2" in content or "psycopg2-binary" in content:
        print("✅ PostgreSQL dependencies already in requirements.txt")
        return True
    
    # Add PostgreSQL dependencies
    postgresql_deps = """
# PostgreSQL Database Support
psycopg2-binary==2.9.9
dj-database-url==2.1.0
"""
    
    # Append to requirements
    with open(requirements_file, 'a', encoding='utf-8') as f:
        f.write(postgresql_deps)
    
    print("✅ Added PostgreSQL dependencies to requirements.txt")
    return True

def create_migration_script():
    """Create database migration script"""
    
    print("\n🔄 Creating database migration script...")
    
    migration_script = """#!/usr/bin/env python
\"\"\"
Database Migration Script: SQLite to Supabase PostgreSQL
Run this script to migrate your data from SQLite to Supabase PostgreSQL.
\"\"\"

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def migrate_to_supabase():
    \"\"\"Migrate database to Supabase PostgreSQL\"\"\"
    
    print("🚀 Starting migration to Supabase PostgreSQL...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Run migrations
    print("📋 Running Django migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser if needed
    print("👤 Creating superuser...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            print("Enter superuser details:")
            username = input("Username: ")
            email = input("Email: ")
            password = input("Password: ")
            
            User.objects.create_superuser(username, email, password)
            print("✅ Superuser created successfully!")
        else:
            print("✅ Superuser already exists")
            
    except Exception as e:
        print(f"⚠️  Warning: Could not create superuser: {e}")
    
    print("🎉 Migration to Supabase PostgreSQL completed!")
    print("📊 Your data is now stored in Supabase PostgreSQL")

if __name__ == '__main__':
    migrate_to_supabase()
"""
    
    with open("migrate_to_supabase.py", "w", encoding="utf-8") as f:
        f.write(migration_script)
    
    print("✅ Created migrate_to_supabase.py script")

def create_supabase_setup_guide():
    """Create Supabase setup guide"""
    
    print("\n📚 Creating Supabase setup guide...")
    
    setup_guide = """# 🚀 Supabase PostgreSQL Setup Guide

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign in with GitHub
4. Click "New Project"
5. Choose your organization
6. Enter project details:
   - **Name**: GreenTrack-Climatiqq
   - **Database Password**: Generate a strong password
   - **Region**: Choose closest to your users
7. Click "Create new project"

## Step 2: Get Database Connection Details

1. In your project dashboard, go to **Settings** → **Database**
2. Copy the connection string:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```
3. Copy your project URL and API keys

## Step 3: Update Environment Variables

1. Copy `env.supabase` to `.env`
2. Update with your actual values:
   ```env
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
   SUPABASE_ANON_KEY=[YOUR-ANON-KEY]
   SUPABASE_SERVICE_ROLE_KEY=[YOUR-SERVICE-ROLE-KEY]
   ```

## Step 4: Set Up Database Schema

1. Go to **SQL Editor** in Supabase dashboard
2. Copy and paste the contents of `supabase_setup.sql`
3. Click "Run" to execute the script
4. Verify tables are created in **Table Editor**

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Run Migration

```bash
python migrate_to_supabase.py
```

## Step 7: Test Connection

```bash
python manage.py runserver
```

## 🎯 What You Get

✅ **PostgreSQL Database** - Professional, scalable database
✅ **Real-time Features** - Live updates and subscriptions
✅ **Better Performance** - Faster queries and aggregations
✅ **Advanced Analytics** - Complex environmental calculations
✅ **Scalability** - Handle thousands of users
✅ **Backup & Recovery** - Automatic backups and point-in-time recovery

## 🔍 Troubleshooting

### Connection Issues
- Verify DATABASE_URL format
- Check if IP is allowed in Supabase
- Ensure SSL is enabled

### Migration Issues
- Backup your SQLite database first
- Check Django migrations are up to date
- Verify all dependencies are installed

## 📞 Support

- Supabase Documentation: [docs.supabase.com](https://docs.supabase.com)
- Django Documentation: [docs.djangoproject.com](https://docs.djangoproject.com)
- GreenTrack Issues: Create an issue in your repository

---

**Happy Environmental Tracking! 🌱♻️**
"""
    
    with open("SUPABASE_SETUP_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(setup_guide)
    
    print("✅ Created SUPABASE_SETUP_GUIDE.md")

def main():
    """Main setup function"""
    
    print("🌱 GreenTrack - Climatiqq Supabase Setup")
    print("=" * 50)
    
    try:
        # Update Django settings
        if not update_django_settings():
            return False
        
        # Create environment template
        create_env_template()
        
        # Update requirements
        if not update_requirements():
            return False
        
        # Create migration script
        create_migration_script()
        
        # Create setup guide
        create_supabase_setup_guide()
        
        print("\n" + "=" * 50)
        print("🎉 Supabase Setup Scripts Created Successfully!")
        print("\n📋 Next Steps:")
        print("1. Create your Supabase project at supabase.com")
        print("2. Update env.supabase with your credentials")
        print("3. Run the SQL setup script in Supabase SQL Editor")
        print("4. Install dependencies: pip install -r requirements.txt")
        print("5. Run migration: python migrate_to_supabase.py")
        print("\n📚 See SUPABASE_SETUP_GUIDE.md for detailed instructions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
