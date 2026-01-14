import psycopg2
import os
import sys
from decouple import config

# Change to project root directory so .env file is found
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)

# Fetch DB credentials using python-decouple (same as Django settings)
DB_NAME = config("DB_NAME", default=None)
DB_USER = config("DB_USER", default="postgres")
DB_PASSWORD = config("DB_PASSWORD", default="")
DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = int(config("DB_PORT", default=5432))

# Validate required fields
if not DB_NAME:
    print("❌ Error: DB_NAME is required but not set in .env file")
    sys.exit(1)

if not DB_HOST:
    print("❌ Error: DB_HOST is required but not set in .env file")
    sys.exit(1)

try:
    print(f"Attempting to connect to {DB_HOST}:{DB_PORT}...")
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        sslmode="require"
    )

    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    result = cur.fetchone()
    print("✅ Connected! Current DB time:", result[0])

    cur.close()
    conn.close()
    print("Connection closed.")

except psycopg2.OperationalError as e:
    error_msg = str(e)
    if "nodename nor servname provided" in error_msg or "could not translate host name" in error_msg:
        print("❌ DNS Resolution Error: Could not resolve hostname")
        print(f"   Host: {DB_HOST}")
        print("\n   Troubleshooting:")
        print("   1. Verify the hostname in your .env file matches your Supabase project")
        print("   2. Check if your Supabase project is active (not paused)")
        print("   3. Test DNS resolution: nslookup " + DB_HOST)
        print("   4. For local dev, use DB_HOST=localhost or DB_HOST=db (for Docker)")
    elif "password authentication failed" in error_msg:
        print("❌ Authentication Error: Invalid username or password")
        print(f"   User: {DB_USER}")
        print("   Check DB_USER and DB_PASSWORD in your .env file")
    elif "database" in error_msg.lower() and "does not exist" in error_msg.lower():
        print("❌ Database Error: Database does not exist")
        print(f"   Database: {DB_NAME}")
        print("   Check DB_NAME in your .env file")
    else:
        print(f"❌ Connection Error: {error_msg}")
    sys.exit(1)

except Exception as e:
    print(f"❌ Unexpected Error: {type(e).__name__}: {e}")
    sys.exit(1)
