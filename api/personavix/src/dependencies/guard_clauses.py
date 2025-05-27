"""
Module: guard_clauses

This module provides the guard clauses for the permissions.

Functions:
    - verify_permission_is_user: Verify if the permission is user.
    - verify_permission_is_manager: Verify if the permission is manager.
    - verify_permission_is_admin: Verify if the permission is admin.
    - verify_if_user_has_access: Verify if the user has access to the route.
"""

# pylint: disable=import-error
from http import HTTPStatus
from fastapi import HTTPException


def verify_permission_is_user(permission: int, access_flag: int):
    """
    This function verifies if the permission is user.

    Args:
        permission: The permission level.
        access_flag: The access flag indicating whether the user has access (1) or not (0).

    Raises:
        HTTPException: Raised when the permission is not user.
    """
    verify_if_user_has_access(access_flag)

    # 1 is the permission level for user
    if not 1 <= permission <= 3:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Permission is not allowed."
        )


def verify_permission_is_manager(permission: int, access_flag: int):
    """
    This function verifies if the permission is manager.

    Args:
        permission: The permission level.

    Raises:
        HTTPException: Raised when the permission is not manager.
        access_flag: The access flag indicating whether the user has access (1) or not (0).
    """
    verify_if_user_has_access(access_flag)

    # verify if the permission is manager or admin
    if not 2 <= permission <= 3:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Permission is not allowed."
        )


def verify_permission_is_admin(permission: int, access_flag: int):
    """
    This function verifies if the permission is admin.

    Args:
        permission: The permission level.
        access_flag: The access flag indicating whether the user has access (1) or not (0).

    Raises:
        HTTPException: Raised when the permission is not admin.
    """
    verify_if_user_has_access(access_flag)

    # verify if the permission is admin
    if permission != 3:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Permission is not allowed."
        )


def verify_if_user_has_access(access_flag: int):
    """
    This function verifies if the user has access to the route.

    Args:
        access_flag: The access flag indicating whether the user has access (1) or not (0).

    Raises:
        HTTPException: Raised when the permission is not admin.
    """
    if not access_flag:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Does not have access."
        )
