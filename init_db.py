#!/usr/bin/env python3
"""Seeds tinycorp.db with a users table. Run once before starting app.py
(app.py also calls this automatically on first run)."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tinycorp.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )
    # Regular employee accounts (not useful for the flag) + an admin
    # account whose password nobody is ever told.
    cur.executemany(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        [
            ("jsmith", "sunshine99", "employee"),
            ("mkaya", "istanbul2024", "employee"),
            ("admin", "Tr0ub4dor&3xtraSecure!", "admin"),
        ],
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Initialized {DB_PATH}")
