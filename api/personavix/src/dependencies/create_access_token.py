"""
Module: create_access_token.py

This module is responsible for creating the access token for the user.

Functions:
    - create_access_token: Create an access token for the user.
"""

import os
from datetime import datetime, timedelta
from jose import jwt


def create_access_token(
    email: str, is_unique_access_link: bool, expires_delta: timedelta
) -> str:
    """
    Create an access token for the user.

    Args:
        email: The email of the user.
        is_unique_access_link: A boolean indicating if the token is for a unique access link.
        expires_delta: The expiration time of the token.

    Returns:
        str: O token JWT gerado.
    """
    secret_key = os.getenv("SECRET_KEY")

    to_encode = {
        "email": email,
        "is_unique_access_link": is_unique_access_link,
    }
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm="HS256")
