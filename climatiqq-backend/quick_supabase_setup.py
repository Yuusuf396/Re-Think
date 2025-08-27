#!/usr/bin/env python
"""
Quick Supabase Setup Script
Run this to set up everything for Supabase PostgreSQL in one go!
"""

import os
import sys
from pathlib import Path

def run_setup():
    """Run the complete Supabase setup"""
    
    print("🚀 Quick Supabase Setup for GreenTrack - Climatiqq")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: Please run this script from your Django project root directory")
        print("   (where manage.py is located)")
        return False
    
    # Run the main setup script
    try:
        print("📋 Running Supabase setup script...")
        exec(open("supabase_django_settings.py").read())
        print("\n✅ Setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 SUPABASE SETUP COMPLETE!")
    print("\n📋 What was created:")
    print("✅ supabase_setup.sql - Database schema script")
    print("✅ env.supabase - Environment template")
    print("✅ migrate_to_supabase.py - Migration script")
    print("✅ SUPABASE_SETUP_GUIDE.md - Complete setup guide")
    print("✅ Updated requirements.txt - Added PostgreSQL support")
    print("✅ Updated config/settings.py - PostgreSQL configuration")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Go to [supabase.com](https://supabase.com) and create a project")
    print("2. Copy your DATABASE_URL from Supabase dashboard")
    print("3. Update env.supabase with your credentials")
    print("4. Run the SQL script in Supabase SQL Editor")
    print("5. Install dependencies: pip install -r requirements.txt")
    print("6. Run migration: python migrate_to_supabase.py")
    
    print("\n📚 For detailed instructions, see SUPABASE_SETUP_GUIDE.md")
    print("\n🌱 Happy Environmental Tracking!")
    
    return True

if __name__ == '__main__':
    success = run_setup()
    sys.exit(0 if success else 1)
