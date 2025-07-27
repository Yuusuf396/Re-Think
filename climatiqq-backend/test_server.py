#!/usr/bin/env python
"""
Simple test script to check if Django can start
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import execute_from_command_line

def test_django_startup():
    """Test if Django can start without errors"""
    try:
        # Try to import the main views
        from tracker.views import HealthCheckView, SimpleTestView
        print("✅ Successfully imported basic views")
        
        # Try to import the main models
        from tracker.models import ImpactEntry
        print("✅ Successfully imported basic models")
        
        # Try to import serializers
        from tracker.serializers import ImpactEntrySerializer
        print("✅ Successfully imported basic serializers")
        
        print("✅ Django startup test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Django startup test failed: {e}")
        return False

if __name__ == "__main__":
    test_django_startup() 