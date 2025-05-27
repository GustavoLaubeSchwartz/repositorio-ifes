"""
Module: questions.py

This module contains the domain models for the questions of the personality test.

Classes:
    Perguntas (Base): Represents the questions of the personality test.
"""

# pylint: disable=import-error, duplicate-code
from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.orm import relationship
from personavix.src.database.database import Base


class Perguntas(Base):  # pylint: disable=too-few-public-methods
    """
    Represents the questions of the personality test.

    Attributes:
        id_pergunta (int): The unique identifier of the question.
        pergunta (str): The question.
        criado_em (DateTime): The timestamp of the creation of the question record.
        atualizado_em (DateTime): The timestamp of the last update of the question record.
    """

    __tablename__ = "perguntas"

    id_pergunta = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    pergunta = Column(String(60), nullable=False)
    criado_em = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    atualizado_em = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    caracteristicas_disc = relationship(
        "CaracteristicasDisc", back_populates="perguntas_"
    )
