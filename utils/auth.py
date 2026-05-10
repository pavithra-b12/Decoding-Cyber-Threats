import sqlite3
import hashlib
from datetime import datetime
import os

DB_PATH = "data/users.db"

def get_db_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT,
            created_at TEXT,
            last_login TEXT
        )
    """)

    # Create default admin if not exists
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            "admin",
            hash_password("admin123"),
            "admin",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, role FROM users WHERE username=? AND password_hash=?",
        (username, hash_password(password))
    )

    user = cursor.fetchone()

    if user:
        cursor.execute(
            "UPDATE users SET last_login=? WHERE id=?",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user[0])
        )
        conn.commit()

    conn.close()

    if user:
         return (username, user[1])   # (username, role)

    return None

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT username, role FROM users")
    users = cur.fetchall()

    conn.close()
    return users
