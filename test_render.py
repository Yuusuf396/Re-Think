#!/usr/bin/env python3
"""
Test script to see what Render is actually doing
"""

import os
import sys

print("🔍 Render Environment Test")
print("=" * 50)
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print(f"Files in current directory: {os.listdir('.')}")

if os.path.exists('climatiqq-backend'):
    print(f"Backend directory exists: {os.listdir('climatiqq-backend')}")
else:
    print("❌ Backend directory not found")

print("=" * 50)
print("✅ Test completed") 