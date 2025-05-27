"""
Module: verify_if_is_email.py

This module contains the function to verify if a string is an email address.

Functions:
    verify_if_is_email: Verify if a string is an email address.
"""

import re


def verify_if_is_email(email: str) -> bool:
    """
    Verify if a string is an email address.

    Args:
        email: The string to verify.

    Returns:
        bool: True if the string is an email address, False otherwise.
    """
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))
