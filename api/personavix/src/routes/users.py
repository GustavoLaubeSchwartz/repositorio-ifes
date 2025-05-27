"""
Module: users.py

This module contains the routes for handling users-related tasks.

Routes:
    /users:
        GET: Retrieve all users from the database.
        POST: Create a new user in the database.
    /users/{id_user}:
        GET: Retrieve a specific user from the database.
        PATCH: Update a specific user in the database.
    /users/login/with-token:
        POST: Authenticate a user using a token.
    /users/login:
        POST: Authenticate a user by email and password.
"""

# pylint: disable=import-error
from http import HTTPStatus
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from personavix.src.database.database import get_db
from personavix.src.dependencies.hash_password import hash_password, verify_password
from personavix.src.models.domain.users import Usuarios
from personavix.src.models.schemas import users
from personavix.logger import setup_logger
from personavix.src.dependencies.create_access_token import create_access_token
from personavix.src.dependencies.decode_and_verify_token import (
    TokenData,
    decode_and_verify_token,
)
from personavix.src.dependencies import guard_clauses


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    summary="Get all users",
    description="Retrieves all users from the database.",
    response_model=list[users.User],
)
def get_users(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Retrieve a list of persons.

    Args:
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        List[User]: A list of users.
    """
    guard_clauses.verify_permission_is_admin(
        token_data.permission, token_data.access_flag
    )

    try:
        setup_logger().info("Getting all users in table Usuarios.")
        all_users: list[Usuarios] = db.query(Usuarios).all()

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error retrieving users"
        ) from e

    return all_users


@router.get(
    "/{id_user}",
    summary="Get a specific user",
    description="Retrieves a specific user from the database.",
    response_model=users.User,
)
def get_user(
    id_user: int,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Retrieve a specific user by ID.

    Args:
        id_user: ID of the user to retrieve.
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        Usuarios: The user with the specified ID.

    Raises:
        HTTPException: If the user is not found.
    """
    if token_data.is_unique_access_link:
        guard_clauses.verify_permission_is_user(
            token_data.permission, token_data.access_flag
        )

    try:
        setup_logger().info("Getting person with ID %s in table Pessoas", id_user)
        user: Usuarios = db.query(Usuarios).filter(Usuarios.idPessoa == id_user).first()
        if not user:
            setup_logger().error("Code:404 Message: User with ID %s not found", id_user)
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )
        return user

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error retrieving user"
        ) from e


@router.post(
    "/",
    summary="Create a new user",
    description="Creates a new user in the database.",
    response_model=users.User,
)
def create_user(
    user: users.UserCreate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Create a new user.

    Args:
        user: User data to create.
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        Usuarios: The newly created user.

    Raises:
        HTTPException: If the user cannot be created.
    """
    guard_clauses.verify_permission_is_admin(
        token_data.permission, token_data.access_flag
    )

    try:
        setup_logger().info("Creating new user in table Usuarios")
        if user.senha_hash:
            user.senha_hash = hash_password(user.senha_hash)

        new_user = Usuarios(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError as e:
        setup_logger().error("Code:400 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="User already exists"
        ) from e

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error creating user"
        ) from e


@router.post(
    "/login",
    summary="User login",
    description="Authenticates a user by email and password.",
    response_model=users.LoginResponse,
)
def login_user(
    login_data: users.UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticates a user and generates a JWT token.

    Args:
        login_data: User login data.
        db: Database session dependency. Defaults to Depends(get_db).

    Returns:
        JSONResponse: Response with the authentication cookie.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    try:
        user = db.query(Usuarios).filter(Usuarios.email == login_data.email).first()

        if not user or not verify_password(login_data.senha, user.senha_hash):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials"
            )

        access_token: str = create_access_token(user.email, False, timedelta(hours=24))

        return {"user_datas": user, "access_token": access_token}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error during login"
        ) from e


@router.post(
    "/login/with-token",
    summary="User login",
    description="Authenticates a user using a token.",
    response_model=users.LoginResponse,
)
def get_user_session(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Authenticates a user using a token.

    Args:
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        JSONResponse: Response with the authentication cookie.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    try:
        userEmail = token_data.email

        user = db.query(Usuarios).filter(Usuarios.email == userEmail).first()

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )
        if not user.flag_acesso:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="User not authorized"
            )

        access_token: str = create_access_token(user.email, False, timedelta(hours=24))
        return {"user_datas": user, "access_token": access_token}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error during login with token"
        ) from e


@router.patch(
    "/{id_user}",
    summary="Updates an user",
    description="Updates an user in the database.",
    response_model=users.User,
)
def update_user(
    id_user: int,
    user_datas: users.UserUpdate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Update an user.

    Args:
        id_user: ID of the user to update.
        user_datas: User data to update.
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        Usuarios: The updated user.

    Raises:
        HTTPException: If the user is not found or if an error occurs during the update.
    """
    if token_data.is_unique_access_link:
        guard_clauses.verify_permission_is_user(
            token_data.permission, token_data.access_flag
        )

    try:
        user_to_update = (
            db.query(Usuarios).filter(Usuarios.id_usuario == id_user).first()
        )
        if not user_to_update:
            setup_logger().error("Code:404 Message: User with ID %s not found", id_user)
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User with id {id_user} not found",
            )

        updated_fields = user_datas.dict(exclude_unset=True)
        for field, value in updated_fields.items():
            setattr(user_to_update, field, value)

        db.commit()
        db.refresh(user_to_update)

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error updating user"
        ) from e

    return user_to_update
