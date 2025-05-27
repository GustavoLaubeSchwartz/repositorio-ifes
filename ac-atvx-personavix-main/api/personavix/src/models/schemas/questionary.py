"""
Module: questionary.py

This module contains the schemas for the questionary of the disc test.

Classes:
    Questionary (BaseModel): Represents the schema for the questionary.
"""

# pylint: disable=import-error, too-few-public-methods, duplicate-code
from pydantic import BaseModel, Field
from personavix.src.models.schemas.questions import Questions
from personavix.src.models.schemas.disc_characteristics import DiscCharacteristics


class Questionary(BaseModel):
    """
    Schema class for a question.

    Attributes:
        questions (list[Questions]): The questions.
        disc_characteristics (list[DiscCharacteristics]): The disc characteristics.
    """

    questions: list[Questions] = Field(..., alias="questions")
    disc_characteristics: list[DiscCharacteristics] = Field(
        ..., alias="disc_characteristics"
    )

    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuration class for Pydantic models.

        This class provides configuration options for Pydantic models, such as enabling ORM mode.

        orm_mode (bool): Flag indicating whether ORM mode is enabled for the model.
            allow_population_by_field_name (bool): Flag indicating whether to allow population
            by field name.
        """

        orm_mode = True
        allow_population_by_field_name = True
