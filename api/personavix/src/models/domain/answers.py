"""
Module: answers.py

This module contains the domain models for the answers to the personality test.

Classes:
    Respostas (Base): Represents the answers to the personality test.
"""

# pylint: disable=import-error, duplicate-code
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKeyConstraint,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship
from personavix.src.database.database import Base


class Respostas(Base):  # pylint: disable=too-few-public-methods
    """
    Represents the answers to the personality test.

    Attributes:
        id_resposta (int): The unique identifier of the answer.
        id_usuario (int): The unique identifier of the user.
        dominancia (str): The dominance score.
        influencia (str): The influence score.
        estabilidade (str): The stability score.
        conformidade (str): The conformity score.
        motivo (str): The reason for the answer.
    """

    __tablename__ = "respostas"
    __table_args__ = (
        ForeignKeyConstraint(
            ["id_usuario"],
            ["usuarios.id_usuario"],
            ondelete="CASCADE",
            name="fk_respostas_usuarios",
        ),
    )

    id_resposta = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    id_usuario = Column(Integer, nullable=False)
    dominancia = Column(Float, nullable=False)
    influencia = Column(Float, nullable=False)
    estabilidade = Column(Float, nullable=False)
    conformidade = Column(Float, nullable=False)
    motivo = Column(String(45), nullable=False)
    respondido_em = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    usuarios_ = relationship("Usuarios", back_populates="respostas")
