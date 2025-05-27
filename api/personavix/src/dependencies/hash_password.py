"""
Module: hash_password.py

This module is responsible for hashing the password of the user.

Functions:
    - hash_password: Hash the password of the user.
    - verify_password: Verify the password of the user.
"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Hash the password of the user.

    Args:
        password: str: The password of the user.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the password of the user.

    Args:
        plain_password: str: The plain text password.
        hashed_password: str: The hashed password stored in the database.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
