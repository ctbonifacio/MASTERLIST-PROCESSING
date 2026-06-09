#!/usr/bin/env python3
"""
Database Connection Test Script
Tests connectivity to MySQL at 172.16.131.242:3307
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "172.16.131.242"),
    "port": int(os.getenv("DB_PORT", 3307)),
    "user": os.getenv("DB_USER", "usr4mis"),
    "password": os.getenv("DB_PASSWORD", "usr4MIS#@!"),
    "database": os.getenv("DB_NAME", "masterlist_db"),
}

print("=" * 60)
print("DATABASE CONNECTION TEST")
print("=" * 60)
print(f"\n📌 Connection Details:")
print(f"  Host: {DB_CONFIG['host']}")
print(f"  Port: {DB_CONFIG['port']}")
print(f"  User: {DB_CONFIG['user']}")
print(f"  Database: {DB_CONFIG['database']}")
print()

# Test 1: Basic TCP Connection
print("🔍 Step 1: Testing TCP Connection...")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((DB_CONFIG['host'], DB_CONFIG['port']))
    sock.close()
    
    if result == 0:
        print("✅ TCP Port is OPEN and reachable\n")
    else:
        print(f"❌ TCP Port is CLOSED or unreachable (error code: {result})")
        print("   → Check if MySQL is running on that port")
        print("   → Check firewall rules")
        print("   → Verify host IP is correct\n")
except Exception as e:
    print(f"❌ TCP test failed: {e}\n")

# Test 2: MySQL Authentication
print("🔍 Step 2: Testing MySQL Authentication...")
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ Successfully connected to MySQL!\n")
    
    # Test 3: Database Access
    print("🔍 Step 3: Testing Database Access...")
    cursor = conn.cursor()
    
    # Check if masterlist_db exists
    cursor.execute("SHOW DATABASES LIKE 'masterlist_db'")
    db_exists = cursor.fetchone()
    
    if db_exists:
        print("✅ Database 'masterlist_db' EXISTS\n")
        
        # Test 4: Table Access
        print("🔍 Step 4: Testing Table Access...")
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        print(f"✅ 'user' table accessible - {user_count} records found\n")
        
        cursor.execute("SELECT COUNT(*) FROM masterlist_data")
        data_count = cursor.fetchone()[0]
        print(f"✅ 'masterlist_data' table accessible - {data_count} records found\n")
        
    else:
        print("⚠️  Database 'masterlist_db' does NOT exist")
        print("   → Run: mysql -h 172.16.131.242 -P 3307 -u usr4mis -p < database_schema.sql\n")
    
    cursor.close()
    conn.close()
    
    print("=" * 60)
    print("✅ ALL TESTS PASSED - Connection working!")
    print("=" * 60)

except Error as e:
    print(f"❌ MySQL Connection Failed")
    print(f"   Error: {e}\n")
    
    if "Access denied" in str(e):
        print("   → Wrong username or password")
        print("   → Check .env file credentials\n")
    elif "Connection refused" in str(e) or "No route to host" in str(e):
        print("   → MySQL not running on that host:port")
        print("   → Verify host IP: 172.16.131.242")
        print("   → Verify port: 3307\n")
    elif "Unknown host" in str(e):
        print("   → Hostname/IP is not resolvable")
        print("   → Check network connectivity\n")
    
    print("=" * 60)
    print("❌ CONNECTION FAILED - See errors above")
    print("=" * 60)

except Exception as e:
    print(f"❌ Unexpected error: {e}\n")
