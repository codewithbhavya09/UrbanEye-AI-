"""
auth_utils.py
--------------
This file contains helper functions related to user authentication.
It handles password hashing and password checking so that we never
store plain text passwords in the database.
"""

import hashlib


def hash_password(plain_password):
    """
    Converts a plain text password into a secure hashed string
    using SHA-256 hashing.

    We use hashing so that even if someone sees the database,
    they cannot read the actual passwords.
    """
    # Encode the password into bytes, then hash it
    hashed_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return hashed_password


def check_password(plain_password, hashed_password_from_db):
    """
    Checks if a plain text password matches the hashed password
    stored in the database.

    Returns True if they match, False otherwise.
    """
    # Hash the plain password the same way and compare the two hashes
    hashed_input_password = hash_password(plain_password)
    return hashed_input_password == hashed_password_from_db


def is_valid_email(email):
    """
    Performs a very simple check to see if the email looks valid.
    This is not a full email validation, just a basic beginner-friendly check.
    """
    if "@" in email and "." in email:
        return True
    return False


def is_valid_username(username):
    """
    Checks that the username is not empty and has no spaces.
    """
    if len(username.strip()) == 0:
        return False
    if " " in username:
        return False
    return True
