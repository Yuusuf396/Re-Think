#!/usr/bin/env python3
"""Check .env file for potential issues"""
from decouple import config
import os
import sys

print("=== Checking Environment Variables ===")
db_pass = config('DB_PASSWORD', default='')
special_chars = '#$%&*()[]{}|\\:;"\'<>?,/!@^~`'
print(f"DB_PASSWORD length: {len(db_pass)}")
print(f"DB_PASSWORD contains special chars: {any(c in db_pass for c in special_chars)}")
print(f"DB_PASSWORD has spaces: {' ' in db_pass}")
print(f"DB_PASSWORD starts/ends with space: {db_pass != db_pass.strip() if db_pass else False}")

db_url = config('DATABASE_URL', default=None)
print(f"\nDATABASE_URL is set: {db_url is not None}")
if db_url:
    print("  ⚠️  WARNING: DATABASE_URL will override individual DB_ variables!")
    print(f"  Value: {db_url[:50]}..." if len(db_url) > 50 else f"  Value: {db_url}")

print("\n=== Checking .env File Format ===")
env_path = '.env'
if not os.path.exists(env_path):
    print(f"❌ .env file not found at {os.path.abspath(env_path)}")
    sys.exit(1)

with open(env_path, 'r') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
problematic = []

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped or stripped.startswith('#'):
        continue
    
    # Check for common issues
    if '=' not in stripped:
        problematic.append(f"Line {i}: No = sign - '{stripped[:50]}'")
    elif stripped.count('=') > 1:
        problematic.append(f"Line {i}: Multiple = signs - '{stripped[:50]}'")
    elif ' =' in stripped or '= ' in stripped:
        problematic.append(f"Line {i}: Spaces around = - '{stripped[:50]}'")
    elif stripped.startswith('=') or stripped.endswith('='):
        problematic.append(f"Line {i}: Empty key or value - '{stripped[:50]}'")
    
    # Check for DB variables
    if stripped.startswith('DB_') or stripped.startswith('DATABASE_'):
        key, value = stripped.split('=', 1) if '=' in stripped else (stripped, '')
        if not value.strip():
            problematic.append(f"Line {i}: Empty value for {key}")

if problematic:
    print("\n⚠️  Potential Issues Found:")
    for p in problematic:
        print(f"  - {p}")
else:
    print("✅ No obvious format issues found")

print("\n=== Current Database Configuration ===")
print(f"DB_NAME: {config('DB_NAME', default=None)}")
print(f"DB_USER: {config('DB_USER', default='postgres')}")
print(f"DB_HOST: {config('DB_HOST', default='localhost')}")
print(f"DB_PORT: {config('DB_PORT', default='5432')}")
print(f"DB_PASSWORD: {'*' * len(db_pass) if db_pass else '(empty)'}")
