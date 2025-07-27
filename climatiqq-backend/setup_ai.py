#!/usr/bin/env python3
"""
Quick AI Setup Script
Installs dependencies and trains the AI model in under 5 minutes
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required AI dependencies"""
    print("📦 Installing AI dependencies...")
    
    dependencies = [
        'scikit-learn',
        'numpy',
        'pandas',
        'joblib'
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")
            return False
    
    return True

def train_model():
    """Train the AI model"""
    print("\n🤖 Training AI Model...")
    
    try:
        # Import and train
        from tracker.train_ai_model import main
        main()
        return True
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        return False

def main():
    print("🚀 Rethink AI Setup")
    print("=" * 40)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Train model
    if not train_model():
        print("❌ Failed to train model")
        return
    
    print("\n🎉 AI Setup Complete!")
    print("\n📝 What's ready:")
    print("   ✅ AI model trained and saved")
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