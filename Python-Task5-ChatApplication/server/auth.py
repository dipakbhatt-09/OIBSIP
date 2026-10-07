"""User registration, password hashing, and login authentication."""

import hashlib
import sqlite3

from database import get_connection


def hash_password(password):
    """Return the SHA-256 hash of a password."""
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def register_user(username, password):
    """Register a new user with a hashed password."""
    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    password_hash = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        connection.commit()

        return True, "Registration successful."

    except sqlite3.IntegrityError:
        return False, "Username already exists."

    finally:
        connection.close()


def login_user(username, password):
    """Authenticate a user using the stored password hash."""
    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    password_hash = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password_hash)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        return True, user

    return False, "Invalid username or password."


if __name__ == "__main__":
    # Basic check that the authentication module loads correctly.
    print("Authentication module ready.")

