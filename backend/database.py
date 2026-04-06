import sqlite3
import os

os.makedirs('backend', exist_ok=True)  # Ensure dir if needed

def get_connection():
    conn = sqlite3.connect('backend/db.sqlite3', timeout=30.0)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.execute('PRAGMA busy_timeout=30000')
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('PRAGMA journal_mode=WAL')
    cur.execute("DROP TABLE IF EXISTS otp_verification")
    cur.execute("DROP TABLE IF EXISTS users")
    # cur.execute("UPDATE users SET first_name = username WHERE first_name IS NULL")  # Disabled: no 'username' column in current schema
    cur.execute('''
        CREATE TABLE otp_verification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            otp TEXT,
            is_verified BOOLEAN DEFAULT FALSE
        )
    ''')
    cur.execute(''' 
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Moved to app startup event

