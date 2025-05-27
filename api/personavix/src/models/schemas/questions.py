"""
Module: questions.py

This module contains the schemas for the questions of the disc test.

Classes:
    QuestionsBase (BaseModel): Represents the base schema for a question.
    Questions (QuestionsBase): Represents the schema for a question.
"""

# pylint: disable=import-error, too-few-public-methods, duplicate-code
from datetime import datetime
from pydantic import BaseModel, conint
from pydantic.types import constr


class QuestionsBase(BaseModel):
    """
    Represents the base schema for a question.

    Attributes:
        pergunta (str): The question.
    """

    pergunta: constr(min_length=3, max_length=60)


class Questions(QuestionsBase):
    """
    Schema class for a question.

    Attributes:
        id_pergunta (int): The identifier of the question.
        pergunta (str): The question.
        criado_em (datetime): The creation date of the question.
        atualizado_em (datetime): The update date of the question.
    """

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
