#!/usr/bin/env python3
"""
Check Dependencies
Verifies all required packages are installed and working
"""

import sys
import importlib

def check_dependency(module_name, package_name=None):
    """Check if a dependency is installed"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError:
        print(f"❌ {package_name or module_name} - NOT INSTALLED")
        return False

def main():
    """Check all dependencies"""
    print("🔍 Checking Dependencies")
    print("=" * 50)
    
    dependencies = [
        ('django', 'Django'),
        ('rest_framework', 'Django REST Framework'),
        ('rest_framework_simplejwt', 'Django REST Framework Simple JWT'),
        ('corsheaders', 'Django CORS Headers'),
        ('dotenv', 'python-dotenv'),
        ('jwt', 'PyJWT'),
        ('openai', 'OpenAI'),
        ('gunicorn', 'Gunicorn'),
        ('whitenoise', 'WhiteNoise'),
        ('dj_database_url', 'dj-database-url'),
        ('psycopg2', 'psycopg2-binary'),
    ]
    
    results = []
    
    for module_name, package_name in dependencies:
        result = check_dependency(module_name, package_name)
        results.append((package_name, result))
    
    # Summary
    print("\n" + "="*50)
    print("📊 DEPENDENCY CHECK SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for package_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {package_name}")
    
    print(f"\nOverall: {passed}/{total} dependencies installed")
    
    if passed == total:
        print("🎉 All dependencies are installed!")
    else:
        print("⚠️ Some dependencies are missing.")
        print("Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 