import psycopg2
from decouple import config
import os
import sys
import socket
import json
from datetime import datetime

# #region agent log
log_path = "/Users/yuusufadebayo/Desktop/Re-Think/.cursor/debug.log"


def debug_log(location, message, data, hypothesis_id):
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": hypothesis_id,
                "location": location,
                "message": message,
                "data": data,
                "timestamp": int(datetime.now().timestamp() * 1000)
            }) + "\n")
    except:
        pass
# #endregion


# Add parent directory to path so decouple can find .env file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
# #region agent log
debug_log("testconnections.py:9", "Directory change", {
          "script_dir": script_dir, "project_root": project_root, "cwd_before": os.getcwd()}, "E")
# #endregion
os.chdir(project_root)  # Change to project root so .env is found
# #region agent log
debug_log("testconnections.py:12", "After directory change", {
          "cwd_after": os.getcwd(), "env_file_exists": os.path.exists(".env")}, "E")
# #endregion

# Fetch DB credentials using python-decouple (same as Django settings)
DB_NAME = config("DB_NAME", default=None)
DB_USER = config("DB_USER", default="postgres")
DB_PASSWORD = config("DB_PASSWORD", default="")
DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = int(config("DB_PORT", default=5432))

# #region agent log
debug_log("testconnections.py:22", "Environment variables loaded", {
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": "***" if DB_PASSWORD else "",
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "hostname_length": len(DB_HOST) if DB_HOST else 0,
    "hostname_type": type(DB_HOST).__name__
}, "A")
# #endregion

# #region agent log
try:
    socket.gethostbyname("8.8.8.8")  # Test basic network
    network_test = "ok"
except:
    network_test = "failed"
try:
    socket.gethostbyname("google.com")  # Test DNS
    dns_test = "ok"
except Exception as e:
    dns_test = f"failed: {str(e)}"
try:
    resolved_ip = socket.gethostbyname(DB_HOST) if DB_HOST else None
    hostname_resolution = f"resolved_to_{resolved_ip}" if resolved_ip else "failed"
except Exception as e:
    hostname_resolution = f"failed: {str(e)}"
# Test if supabase.co domain resolves
try:
    socket.gethostbyname("supabase.co")
    supabase_domain_test = "ok"
except Exception as e:
    supabase_domain_test = f"failed: {str(e)}"
# Try nslookup equivalent using socket.getaddrinfo
try:
    addrinfo = socket.getaddrinfo(
        DB_HOST, DB_PORT, socket.AF_INET) if DB_HOST else None
    addrinfo_test = f"found_{len(addrinfo)}_addresses" if addrinfo else "failed"
except Exception as e:
    addrinfo_test = f"failed: {str(e)}"
debug_log("testconnections.py:35", "Network and DNS tests", {
    "network_test": network_test,
    "dns_test": dns_test,
    "supabase_domain_test": supabase_domain_test,
    "hostname_resolution": hostname_resolution,
    "addrinfo_test": addrinfo_test,
    "target_hostname": DB_HOST,
    "hostname_parts": DB_HOST.split(".") if DB_HOST else []
}, "A")
# #endregion

try:
    # #region agent log
    debug_log("testconnections.py:45", "Before connection attempt", {
        "host": DB_HOST,
        "port": DB_PORT,
        "dbname": DB_NAME,
        "user": DB_USER
    }, "B")
    # #endregion
    # Connect to Supabase Postgres
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        sslmode="require"  # Supabase requires SSL
    )
    # #region agent log
    debug_log("testconnections.py:58", "Connection successful",
              {"status": "connected"}, "B")
    # #endregion
    print("✅ Connection successful!")

    # Test query
    with connection.cursor() as cursor:
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print("Current DB time:", result)

    # Close connection
    connection.close()
    print("Connection closed.")

except Exception as e:
    # #region agent log
    debug_log("testconnections.py:65", "Connection failed", {
        "error_type": type(e).__name__,
        "error_message": str(e),
        "error_args": str(e.args) if hasattr(e, 'args') else None
    }, "B")
    # #endregion
    print(f"Failed to connect: {e}")
