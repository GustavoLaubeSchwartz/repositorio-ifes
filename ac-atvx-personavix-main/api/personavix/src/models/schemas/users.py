"""
Module: users.py

This module contains the schemas for the users.

Classes:
    UserBase (BaseModel): Represents the base schema for a user.
    UserCreate (UserBase): Represents the schema for creating a user.
    User (UserBase): Represents the schema for a user.
    UserLogin (BaseModel): Represents the schema for logging in a user.
    UserUpdate (BaseModel): Represents the schema for updating a user.
    LoginResponse (BaseModel): Represents the schema for the login response.
"""

# pylint: disable=import-error, too-few-public-methods
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, conint, EmailStr, Field
from pydantic.types import constr


class UserBase(BaseModel):
    """Base schema for a user.

    Attributes:
        nome (str): The name of the user.
        email (str): The email address of the user.
        telefone (str): The telephone number of the user.
        flag_acesso (int): The access flag indicating whether the user has access (1) or not
        (0).
        permissao (int): The permission level of the user.
        setor (str): The sector of the user.
    """

    nome: Optional[constr(min_length=3, max_length=80)]
    email: EmailStr
    telefone: Optional[constr(min_length=8, max_length=30)]
    flag_acesso: conint(ge=0, le=1)
    permissao: conint(ge=1, le=3)
    setor: Optional[constr(min_length=3, max_length=45)]


class UserCreate(UserBase):
    """Schema for creating a user.

    Attributes:
        nome (str): The name of the user.
        email (str): The email address of the user.
        telefone (str): The telephone number of the user.
        flag_acesso (int): The access flag indicating whether the user has access (1) or not
        (0).
        permissao (int): The permission level of the user.
        setor (str): The sector of the user.
        senha_hash (str): The hashed password of the user.
    """

    senha_hash: Optional[constr(min_length=6, max_length=128)]


class User(UserBase):
    """Schema for

    Attributes:
        id_usuario (int): The unique identifier of the user.
        nome (str): The name of the user.
        email (str): The email address of the user.
        telefone (str): The telephone number of the user.
        flag_acesso (int): The access flag indicating whether the user has access (1) or not
        (0).
        permissao (int): The permission level of the user.
        setor (str): The sector of the user.
        criado_em (DateTime): The timestamp of the creation of the user record.
        atualizado_em (DateTime): The timestamp of the last update of the user record.
    """

    id_usuario: conint(ge=1)
    criado_em: datetime
    atualizado_em: datetime

    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuration class for Pydantic models.

        This class provides configuration options for Pydantic models, such as enabling ORM mode.

        Attributes:
            orm_mode (bool): Flag indicating whether ORM mode is enabled for the model.
        """

        orm_mode = True


class UserLogin(BaseModel):
    """
    Schema for logging in a user.

    Attributes:
        email (str): The email address of the user.
        senha (str): The password of the user.
    """

    email: EmailStr
    senha: constr(min_length=6, max_length=128)


class UserUpdate(BaseModel):
    """
    Schema for logging in a user.

    Attributes:
        nome (str): The name of the user.
        email (str): The email address of the user.
        telefone (str): The
    """

    nome: Optional[constr(min_length=3, max_length=80)]
    email: Optional[EmailStr]
    telefone: Optional[constr(min_length=8, max_length=30)]


class LoginResponse(BaseModel):
    """
    Schema for the login response.

    Attributes:
        user_datas (User): The user data.
        access_token (str): The access token.
    """

    user_datas: User = Field(..., alias="user_datas")
    access_token: constr(min_length=1, max_length=255)

    class Config:
        """Configuration class for Pydantic models.

        This class provides configuration options for Pydantic models, such as enabling ORM mode.

        Attributes:
            orm_mode (bool): Flag indicating whether ORM mode is enabled for the model.
            allow_population_by_field_name (bool): Flag indicating whether to allow population
            by field name.
        """

        orm_mode = True
        allow_population_by_field_name = True
