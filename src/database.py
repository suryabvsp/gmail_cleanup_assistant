import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "data" / "gmail.db"


def get_connection():
    DB_FILE.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        message_id TEXT PRIMARY KEY,
        thread_id TEXT,
        sender TEXT,
        sender_domain TEXT,
        subject TEXT,
        date TEXT,
        size_estimate INTEGER,
        has_attachment INTEGER,
        labels TEXT,
        category TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_email(email):
    conn = get_connection()

    conn.execute("""
    INSERT OR REPLACE INTO emails (
        message_id,
        thread_id,
        sender,
        sender_domain,
        subject,
        date,
        size_estimate,
        has_attachment,
        labels,
        category
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email["message_id"],
        email["thread_id"],
        email["sender"],
        email["sender_domain"],
        email["subject"],
        email["date"],
        email["size_estimate"],
        int(email["has_attachment"]),
        email["labels"],
        email["category"],
    ))

    conn.commit()
    conn.close()

def get_email_count():
    conn = get_connection()

    count = conn.execute(
        "SELECT COUNT(*) FROM emails"
    ).fetchone()[0]

    conn.close()

    return count

def email_exists(message_id):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT 1
        FROM emails
        WHERE message_id = ?
        """,
        (message_id,),
    ).fetchone()

    conn.close()

    return row is not None