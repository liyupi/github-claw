"""Database initialization and helpers for the media processing platform."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "media_platform.db")


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema."""
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            media_type TEXT NOT NULL,
            operation TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            input_path TEXT,
            output_path TEXT,
            output_format TEXT,
            quality INTEGER,
            file_size_before INTEGER,
            file_size_after INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT
        )
        """
    )
    conn.commit()
    conn.close()
