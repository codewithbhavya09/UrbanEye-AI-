"""
database.py
------------
This file handles all the SQLite database operations for UrbanEye AI.
It creates the required tables and provides simple functions to:
- register and check users
- add complaints
- fetch complaints
- update complaint status
"""

import sqlite3
import os
from datetime import datetime

# We import dotenv to read the database path from the .env file
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the database path from .env, or use a default path if not found
DATABASE_PATH = os.getenv("DATABASE_PATH", "database/urbaneye.db")


def create_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    # Make sure the folder for the database exists
    folder_name = os.path.dirname(DATABASE_PATH)
    if folder_name and not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Connect to the SQLite database (it will be created if it does not exist)
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    return connection


def create_tables():
    """
    Creates the 'users' and 'complaints' tables if they do not already exist.
    This function should be called once when the app starts.
    """
    connection = create_connection()
    cursor = connection.cursor()

    # Table to store user login details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Table to store civic issue complaints
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            location TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    connection.commit()
    connection.close()


def add_user(full_name, username, email, hashed_password):
    """
    Adds a new user to the users table.
    Returns True if successful, False if the username already exists.
    """
    connection = create_connection()
    cursor = connection.cursor()

    try:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO users (full_name, username, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, username, email, hashed_password, created_at))
        connection.commit()
        success = True
    except sqlite3.IntegrityError:
        # This error happens if the username already exists
        success = False

    connection.close()
    return success


def get_user_by_username(username):
    """
    Fetches a single user row by username.
    Returns None if the user is not found.
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_row = cursor.fetchone()

    connection.close()
    return user_row


def add_complaint(user_id, image_path, issue_type, confidence, location, severity):
    """
    Adds a new complaint to the complaints table.
    New complaints always start with the status 'Pending'.
    """
    connection = create_connection()
    cursor = connection.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Pending"

    cursor.execute("""
        INSERT INTO complaints
        (user_id, image_path, issue_type, confidence, location, severity, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, image_path, issue_type, confidence, location, severity, status, created_at))

    connection.commit()
    connection.close()


def get_complaints_by_user(user_id):
    """
    Returns all complaints submitted by a specific user, newest first.
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM complaints WHERE user_id = ? ORDER BY id DESC
    """, (user_id,))
    complaints = cursor.fetchall()

    connection.close()
    return complaints


def get_all_complaints():
    """
    Returns all complaints from all users, newest first.
    Used for the dashboard charts.
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    complaints = cursor.fetchall()

    connection.close()
    return complaints


def update_complaint_status(complaint_id, new_status):
    """
    Updates the status of a specific complaint.
    new_status should be one of: 'Pending', 'In Progress', 'Resolved'
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE complaints SET status = ? WHERE id = ?
    """, (new_status, complaint_id))

    connection.commit()
    connection.close()
