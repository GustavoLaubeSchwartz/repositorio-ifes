"""
Module: unique_access_links.py

This module contains the schemas for the unique access links.

Classes:
    UniqueAccessLinkBase (BaseModel): Represents the base schema for a unique access link.
    UniqueAccessLinkCreate (UniqueAccessLinkBase): Represents the schema for creating
        a unique access link.
    UniqueAccessLinkUpdate (UniqueAccessLinkBase): Represents the schema for updating
        a unique access link.
    UniqueAccessLink (UniqueAccessLinkBase): Represents the schema for a unique access link.
    UniqueAccessLinkLogin (BaseModel): Represents the schema for logging in a unique access link.
    UniqueAccessLinkWithUser (UniqueAccessLink): Represents the schema for a unique access link
        with user information.
    LoginResponse (BaseModel): Represents the schema for the login response.
"""

# pylint: disable=import-error, too-few-public-methods
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, conint, Field
from pydantic.types import constr
from personavix.src.models.schemas.users import User


class UniqueAccessLinkBase(BaseModel):
    """Represents a unique access link.

    Attributes:
        id_usuario (int): The unique identifier of the user.
        link (str): The unique access link.
        id_resposta (int): The unique identifier of the response.
    """

    link: constr(min_length=1, max_length=255)


class UniqueAccessLinkCreate(UniqueAccessLinkBase):
    """Schema for creating a unique access link.

    Attributes:
        user (str): The user's email or user's phone number.
        link (str): The unique access link.
        senha_hash (str): The hashed password of the link.
    """

    user: constr(min_length=6, max_length=128)
    senha_hash: Optional[constr(min_length=6, max_length=128)]


class UniqueAccessLinkUpdate:
    """Schema for updating a unique access link.

    Attributes:
        id_sessao (int): The unique identifier of the session.
        respondido (int): Flag indicating whether the link has been answered.
        id_resposta (int): The unique identifier of the response.
    """

    id_sessao: conint(ge=1)
    respondido: conint(ge=0, le=1)
    id_resposta: conint(ge=1)


class UniqueAccessLink(UniqueAccessLinkBase):
    """
    Schema for a unique access link.

    Attributes:
        id_sessao (int): The unique identifier of the session.
        id_resposta (int): The unique identifier of the response.
        id_usuario (int): The unique identifier of the user.
        link (str): The unique access link.
        respondido (int): The date the link was answered.
        criado_em (datetime): The creation date of the link.
        respondido_em (Optional[datetime]): The date the link was answered.
    """

    id_sessao: conint(ge=1)
    id_resposta: Optional[conint(ge=1)]
    id_usuario: conint(ge=1)
    respondido: conint(ge=0, le=1)
    criado_em: datetime
    respondido_em: Optional[datetime]

    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuration class for Pydantic models.

        This class provides configuration options for Pydantic models, such as enabling ORM mode.

        Attributes:
            orm_mode (bool): Flag indicating whether ORM mode is enabled for the model.
        """

        orm_mode = True


class UniqueAccessLinkLogin(BaseModel):
    """
    Schema for logging in a unique access link.

    Attributes:
        senha (str): The password of the link.
    """

    senha: constr(min_length=6, max_length=128)


class UniqueAccessLinkWithUser(UniqueAccessLink):
    """
    Schema for a unique access link with user information.

    Attributes:
        usuarios_ (User): The user information.
    """

    usuarios_: User = Field(..., alias="usuarios_")

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


class LoginResponse(BaseModel):
    """
    Schema for the login response.

    Attributes:
        session_datas (User): The user data.
        access_token (str): The access token.
    """

    session_datas: UniqueAccessLinkWithUser = Field(..., alias="session_datas")
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
