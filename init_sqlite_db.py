import sqlite3
import os
from datetime import datetime, timedelta

DATABASE_FILE = "masterlist.db"

def init_database():
    """Initialize SQLite database with schema."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # User table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            first_login DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            password_hash TEXT,
            role TEXT,
            status TEXT DEFAULT 'ACTIVE',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Masterlist data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS masterlist_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank TEXT NOT NULL,
            acc_number TEXT,
            debtor_name TEXT,
            status TEXT DEFAULT 'Pending',
            claim_paid_amount REAL,
            date_import DATE,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            details TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Masterlist upload history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS masterlist_upload_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            record_count INTEGER DEFAULT 0,
            total_amount REAL DEFAULT 0,
            summary_json TEXT
        )
    """)

    # Activity log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            username TEXT,
            action TEXT,
            details TEXT,
            ip_address TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def seed_sample_data():
    """Insert sample data for testing."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check if data exists
    cursor.execute("SELECT COUNT(*) FROM user")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return  # Already seeded
    
    # Insert sample users
    users = [
        ("jvortega", "Jvortega User", "Agent"),
        ("cgmedalla", "Cyntia G. Medalla", "Agent"),
        ("decajes", "Decajes Agent", "Agent"),
        ("ncessopalao", "Nicolas C. Essopalaos", "Agent"),
        ("hpbonabon", "Herminia P. Bonabon", "Supervisor"),
    ]
    
    for username, name, role in users:
        cursor.execute("""
            INSERT OR IGNORE INTO user (username, name, first_login, role, status)
            VALUES (?, ?, ?, ?, 'ACTIVE')
        """, (username, name, datetime.now().isoformat(), role))
    
    # Insert sample masterlist data
    data = [
        ("HSBC UAE", "ACC001", "Debtor One", "Processed", 5000.00),
        ("HSBC UAE", "ACC002", "Debtor Two", "Processed", 3500.00),
        ("HSBC UAE", "ACC003", "Debtor Three", "Pending", 2000.00),
        ("EIB", "EIB001", "Debtor Four", "Processed", 7500.00),
        ("EIB", "EIB002", "Debtor Five", "Error", 1500.00),
    ]
    
    for bank, acc, debtor, status, amount in data:
        cursor.execute("""
            INSERT INTO masterlist_data 
            (bank, acc_number, debtor_name, status, claim_paid_amount, date_import, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (bank, acc, debtor, status, amount, datetime.now().date().isoformat(), f"{status} successfully"))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    seed_sample_data()
    print("✅ SQLite database initialized with sample data")
