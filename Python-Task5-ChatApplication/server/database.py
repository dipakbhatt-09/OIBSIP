"""Database operations for users, chat rooms, and messages."""

import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "chat.db"
)


def get_connection():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create required tables and the default General room."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            )
            """
        )

        # Create the default room if it does not already exist.
        cursor.execute(
            """
            INSERT OR IGNORE INTO rooms (name)
            VALUES (?)
            """,
            ("General",)
        )

        connection.commit()

    finally:
        connection.close()


def create_room(room_name):
    """Create a new chat room and return whether it was successful."""
    room_name = room_name.strip()

    if not room_name:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO rooms (name) VALUES (?)",
            (room_name,)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_rooms():
    """Return all chat room names ordered by creation time."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT name FROM rooms ORDER BY id"
        )

        return [row[0] for row in cursor.fetchall()]

    finally:
        connection.close()


def room_exists(room_name):
    """Check whether a chat room exists."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM rooms WHERE name = ?",
            (room_name,)
        )

        room = cursor.fetchone()
        return room is not None

    finally:
        connection.close()


def save_message(room_name, username, message):
    """Save a chat message in the specified room."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM rooms WHERE name = ?",
            (room_name,)
        )

        room = cursor.fetchone()

        if room:
            cursor.execute(
                """
                INSERT INTO messages
                (room_id, username, message)
                VALUES (?, ?, ?)
                """,
                (room[0], username, message)
            )

            connection.commit()

    finally:
        connection.close()


def get_message_history(room_name, limit=50):
    """Return the latest messages from a room in chronological order."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT username, message, timestamp
            FROM messages
            WHERE room_id = (
                SELECT id
                FROM rooms
                WHERE name = ?
            )
            ORDER BY id DESC
            LIMIT ?
            """,
            (room_name, limit)
        )

        messages = cursor.fetchall()

        return list(reversed(messages))

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")