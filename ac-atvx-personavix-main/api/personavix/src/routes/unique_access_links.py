"""
Module: unique_access_links.py

This module contains the schemas for the unique access links.

Routes:
    /unique-access-links:
        GET: Retrieve all unique access links from the database.
        POST: Create a unique access link in the database.

    /unique-access-links/{session_link}:
        GET: Retrieve a unique access link by session ID from the database.

    /unique-access-links/login/{id_session}:
        POST: Authenticate a unique access link by password.
"""

# pylint: disable=import-error
from http import HTTPStatus
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from personavix.src.database.database import get_db
from personavix.src.models.domain.users import Usuarios
from personavix.src.models.domain.unique_access_links import LinksAcessoUnico
from personavix.src.models.schemas import unique_access_links
from personavix.src.models.schemas import users
from personavix.logger import setup_logger
from personavix.src.dependencies.hash_password import hash_password
from personavix.src.dependencies.verify_if_is_email import verify_if_is_email
from personavix.src.dependencies.hash_password import verify_password
from personavix.src.routes.users import create_user
from personavix.src.dependencies.create_access_token import create_access_token
from personavix.src.dependencies.decode_and_verify_token import (
    TokenData,
    decode_and_verify_token,
)
from personavix.src.dependencies import guard_clauses


router = APIRouter(prefix="/unique-access-links", tags=["Unique Access Links"])


@router.get(
    "/",
    summary="Get all unique access links",
    description="Retrieves all unique access links from the database.",
    response_model=list[unique_access_links.UniqueAccessLink],
)
def get_unique_access_links(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Retrieve a list of unique access links.

    Args:
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        List[UniqueAccessLink]: A list of unique access links.
    """
    guard_clauses.verify_permission_is_admin(
        token_data.permission, token_data.access_flag
    )

    try:
        setup_logger().info(
            "Getting all unique access links in table LinksAcessoUnico."
        )
        all_unique_access_links: list[LinksAcessoUnico] = db.query(
            LinksAcessoUnico
        ).all()

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error getting unique access links",
        ) from e

    return all_unique_access_links


@router.get(
    "/{session_link}",
    summary="Get a unique access link by session ID",
    description="Retrieves a unique access link by session ID from the database.",
    response_model=unique_access_links.UniqueAccessLinkWithUser,
)
def get_unique_access_link_by_session_link(
    session_link: str, db: Session = Depends(get_db)
):
    """
    This function retrieves a unique access link by session link from the database.

    Args:
        session_link (str): The session link.
        db: Database session dependency. Defaults to Depends(get_db).

    Returns:
        UniqueAccessLink: The unique access link that was retrieved.
    """
    try:
        setup_logger().info(
            "Getting a unique access link by session ID in table LinksAcessoUnico."
        )
        unique_access_link: LinksAcessoUnico = (
            db.query(LinksAcessoUnico)
            .filter(LinksAcessoUnico.link == session_link)
            .first()
        )

        if not unique_access_link:
            setup_logger().error(
                "Code:404 Message: Unique access link not found by session ID"
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Unique access link not found"
            )

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error getting unique access link by session ID",
        ) from e

    return unique_access_link


@router.post(
    "/",
    summary="Create a unique access link",
    description="Creates a unique access link in the database.",
    response_model=unique_access_links.UniqueAccessLink,
)
def create_unique_access_link(
    link: unique_access_links.UniqueAccessLinkCreate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Create a unique access link.

    Args:
        link (UniqueAccessLinkCreate): The unique access link to be created.
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        UniqueAccessLink: The unique access link that was created.
    """
    guard_clauses.verify_permission_is_admin(
        token_data.permission, token_data.access_flag
    )

    try:
        setup_logger().info("Creating a unique access link in table LinksAcessoUnico.")

        user = link.user

        if verify_if_is_email(user):
            existing_user = db.query(Usuarios).filter(Usuarios.email == user).first()
        else:
            existing_user = db.query(Usuarios).filter(Usuarios.telefone == user).first()

        if not existing_user:
            user_data = {
                "nome": None,
                "email": None,
                "telefone": None,
                "flag_acesso": 0,
                "permissao": 1,
                "setor": None,
                "senha_hash": None,
            }
            if verify_if_is_email(link.user):
                user_data["email"] = link.user
            else:
                user_data["telefone"] = link.user

            existing_user = create_user(users.UserCreate(**user_data), db)

        link_data = link.dict()
        link_data["id_usuario"] = existing_user.id_usuario
        link_data["senha_hash"] = hash_password(link.senha_hash)
        link_data.pop("user", None)

        new_unique_access_link = LinksAcessoUnico(**link_data)
        db.add(new_unique_access_link)
        db.commit()
        db.refresh(new_unique_access_link)

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error creating unique access link"
        ) from e

    return new_unique_access_link


@router.post(
    "/login/{id_session}",
    summary="Unique acesse link login",
    description="Authenticates a user by email and password.",
    response_model=unique_access_links.LoginResponse,
)
def unique_access_link_login(
    id_session: int,
    login_data: unique_access_links.UniqueAccessLinkLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate a link by password.

    Args:
        id_session (int): The unique identifier of the session.
        login_data (UniqueAccessLink): The login data.
        db: Database session dependency. Defaults to Depends(get_db).

    Returns:
        UniqueAccessLink: The unique access link that was authenticated.
    """
    try:
        setup_logger().info("Authenticating user by unique access link")
        unique_access_link = (
            db.query(LinksAcessoUnico)
            .filter(LinksAcessoUnico.id_sessao == id_session)
            .first()
        )

        if not unique_access_link or not verify_password(
            login_data.senha, unique_access_link.senha_hash
        ):
            setup_logger().error(
                "Code:401 Message: Invalid credentials for unique access link login"
            )
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials"
            )

        access_token: str = create_access_token(
            unique_access_link.usuarios_.email, True, timedelta(hours=24)
        )

        return {"session_datas": unique_access_link, "access_token": access_token}

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error during login with unique access link",
        ) from e
