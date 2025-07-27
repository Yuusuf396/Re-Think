#!/usr/bin/env python3
"""
Quick AI Setup Script
Sets up the rule-based AI model (no heavy dependencies required)
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if basic dependencies are available"""
    print("📦 Checking dependencies...")
    
    try:
        import django
        print("✅ Django available")
    except ImportError:
        print("❌ Django not found")
        return False
    
    try:
        import openai
        print("✅ OpenAI available")
    except ImportError:
        print("❌ OpenAI not found")
        return False
    
    return True

def test_ai_model():
    """Test the rule-based AI model"""
    print("\n🤖 Testing AI Model...")
    
    try:
        # Import and test
        from tracker.test_ai_model import test_ai_model
        success = test_ai_model()
        return success
    except Exception as e:
        print(f"❌ AI model test failed: {str(e)}")
        return False

def main():
    print("🚀 Rethink AI Setup")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Missing dependencies")
        return
    
    # Test AI model
    if not test_ai_model():
        print("❌ AI model test failed")
        return
    
    print("\n🎉 AI Setup Complete!")
    print("\n📝 What's ready:")
    print("   ✅ Rule-based AI model working")
    print("   ✅ Personalized carbon reduction suggestions")
    print("   ✅ Impact and effort ratings")
    print("   ✅ 15+ different suggestion types")
    
    print("\n🚀 Next steps:")
    print("   1. Start your Django server: python manage.py runserver")
    print("   2. Start your React app: npm start")
    print("   3. Add some environmental impact entries")
    print("   4. Visit the AI Suggestions page to see personalized advice!")

if __name__ == "__main__":
    main() 