"""
Module: decode_and_verify_token.py

This module receives id token from the user and validates to check if the
user is authenticated and has the required permissions.

Classes:
    - TokenData: Pydantic model for token data.

Functions:
    - decode_and_verify_token: Decodes and verifies the token.
    - get_user_email: Retrieves the user's email from the token.
"""

# pylint: disable=import-error, too-few-public-methods
import os
from http import HTTPStatus
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from personavix.src.models.domain.users import Usuarios
from personavix.src.models.schemas.users import User
from personavix.src.database.database import get_db

load_dotenv()

app = FastAPI()
security = HTTPBearer()


class TokenData(BaseModel):
    """
    This class is a Pydantic model for token data.

    Attributes:
        id_user: The id of the user.
        email: The email of the user.
        permission: The permission level of the user.
        access_flag: The access flag indicating whether the user has access (1) or not (0).
        is_unique_access_link: Indicates if the user has a unique access link.
    """

    id_user: int = None
    email: str = None
    permission: int = None
    access_flag: int = None
    is_unique_access_link: bool = None


def decode_and_verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenData:
    """
    This function decodes and verifies the token.

    Args:
        credentials: The credentials of the user.

    Returns:
        token_data: The token data.
    """
    token = credentials.credentials

    secret_key = os.getenv("SECRET_KEY", "")

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])

        email = payload.get("email")
        is_unique_access_link = payload.get("is_unique_access_link", False)

        if not email:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Could not validate credentials.",
            )

        db = next(get_db())

        user_datas: User = get_user_email(email, db)
        token_data = TokenData(
            id_user=user_datas.id_usuario,
            email=email,
            permission=user_datas.permissao,
            access_flag=user_datas.flag_acesso,
            is_unique_access_link=is_unique_access_link,
        )

        return token_data

    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Expired token."
        ) from e

    except JWTError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token."
        ) from e


def get_user_email(useremail: str, db: Session) -> User:
    """
    This function retrieves the user's email from the token.

    Args:
        email: The email of the user.
        db: Database session. Defaults to Depends(get_db).

    Returns:
        user_datas: The user's email.
    """
    try:
        user_datas: Usuarios = (
            db.query(Usuarios)
            .filter(and_(Usuarios.email == useremail, Usuarios.flag_acesso == 1))
            .first()
        )
        if not user_datas:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f"User {useremail} not found."
            )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to get user."
        ) from e

    return user_datas
