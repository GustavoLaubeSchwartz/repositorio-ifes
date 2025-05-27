"""
Module: disc_characteristics.py

This module contains the domain models for the characteristics of the disc test.

Classes:
    DiscCharacteristickBase (Base): Represents the characteristics of the disc test.
    DiscCharacteristics (DiscCharacteristicsBase): Represents the characteristics
        of the disc test.
"""

# pylint: disable=import-error, too-few-public-methods, duplicate-code
from datetime import datetime
from pydantic import BaseModel, conint
from pydantic.types import constr
from personavix.src.models.schemas.enums import FatoresDiscEnum


class DiscCharacteristickBase(BaseModel):
    """
    Represents a base class for the characteristics of the disc test.

    Attributes:
        fator (FatoresDiscEnum): The factor of the disc test.
        caracteristica (str): The characteristic of the disc test.
    """

    fator: FatoresDiscEnum
    caracteristica: constr(min_length=3, max_length=45)


class DiscCharacteristics(DiscCharacteristickBase):
    """
    Schema class for the characteristics of the disc test.

    Attributes:
        id_caracteristica (int): The identifier of the characteristic.
        id_pergunta (int): The identifier of the question.
        fator (FatoresDiscEnum): The factor of the disc test.
        caracteristica (str): The characteristic of the disc test.
        criado_em (datetime): The creation date of the characteristic.
        atualizado_em (datetime): The update date of the characteristic.
    """

    id_caracteristica: conint(ge=1)
    id_pergunta: conint(ge=1)
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
