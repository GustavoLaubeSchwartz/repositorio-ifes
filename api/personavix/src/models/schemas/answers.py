"""
Module: answers.py

This module contains the schemas for the answers to the personality test.

Classes:
    AnswerBase (BaseModel): Represents the base schema for an answer.
    AnswersCreate (AnswerBase): Represents the schema for creating an answer.
    Answers (AnswerBase): Represents the schema for an answer.
    AnswersWithUser (Answer): Represents the schema for an answer with user details.
"""

# pylint: disable=import-error
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, confloat, conint, Field
from pydantic.types import constr
from personavix.src.models.schemas.users import User


class AnswerBase(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Base schema for an answer.

    Attributes:
        dominancia (float): The dominance score.
        influencia (float): The influence score.
        estabilidade (float): The stability score.
        conformidade (float): The conformity score.
        motivo (str): The reason for the answer.
    """

    dominancia: confloat(ge=0, le=100)
    influencia: confloat(ge=0, le=100)
    estabilidade: confloat(ge=0, le=100)
    conformidade: confloat(ge=0, le=100)
    motivo: constr(min_length=1, max_length=45)


class AnswersCreate(AnswerBase):  # pylint: disable=too-few-public-methods
    """Schema for creating an answer.

    This schema extends AnswerBase.

    Attributes:
        id_sessao (int): The unique identifier of the session.
        dominancia (float): The dominance score.
        influencia (float): The influence score.
        estabilidade (float): The stability score.
        conformidade (float): The conformity score.
        motivo (str): The reason for the answer.
    """

    id_sessao: Optional[conint(ge=1)]


class Answer(AnswerBase):  # pylint: disable=too-few-public-methods
    """Schema for an answer.

    This schema extends AnswerBase.

    Attributes:
        id_resposta (int): The unique identifier of the answer.
        id_usuario (int): The unique identifier of the user.
        dominancia (float): The dominance score.
        influencia (float): The influence score.
        estabilidade (float): The stability score.
        conformidade (float): The conformity score.
        motivo (str): The reason for the answer.
        respondido_em (datetime): The date and time the answer was given.
    """

    id_resposta: conint(ge=1)
    id_usuario: conint(ge=1)
    respondido_em: datetime

    class Config:  # pylint: disable=too-few-public-methods
        """Configuration class for Pydantic models.

        This class provides configuration options for Pydantic models, such as enabling ORM mode.

        Attributes:
            orm_mode (bool): Flag indicating whether ORM mode is enabled for the model.

        """

        orm_mode = True


class AnswersWithUser(Answer):  # pylint: disable=too-few-public-methods
    """Schema for an answer with user details.

    This schema extends Answer.

    Attributes:
        usuario (User): The user details.
    """

    usuarios_: User = Field(..., alias="usuarios_")

    class Config:  # pylint: disable=too-few-public-methods
        """Configuration class for Pydantic models.

        This class provides configuration options for Pydantic models, such as enabling ORM mode.

        Attributes:
            orm_mode (bool): Flag indicating whether ORM mode is enabled for the model.
            allow_population_by_field_name (bool): Flag indicating whether to allow population
            by field name.
        """

        orm_mode = True
        allow_population_by_field_name = True
