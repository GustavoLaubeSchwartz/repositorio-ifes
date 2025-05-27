"""
Module: disc_characteristics.py

This module contains the domain models for the characteristics of the disc test.

Classes:
    CaracteristicasDisc (Base): Represents the characteristics of the disc test.
"""

# pylint: disable=import-error, duplicate-code
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    Enum,
    String,
    text,
)
from sqlalchemy.orm import relationship
from personavix.src.database.database import Base
from personavix.src.models.schemas.enums import FatoresDiscEnum


class CaracteristicasDisc(Base):  # pylint: disable=too-few-public-methods
    """
    Represents the characteristics of the disc test.

    Attributes:
        id_caracteristica (int): The unique identifier of the characteristic.
        id_pergunta (int): The unique identifier of the question.
        caracteristica (str): The characteristic.
        fator (str): The factor of the characteristic.
        criado_em (DateTime): The timestamp of the creation of the characteristic record.
        atualizado_em (DateTime): The timestamp of the last update of the characteristic record.
    """

    __tablename__ = "caracteristicas_disc"
    __table_args__ = (
        ForeignKeyConstraint(
            ["id_pergunta"],
            ["perguntas.id_pergunta"],
            ondelete="CASCADE",
            name="fk_caracteristicas_disc_perguntas",
        ),
    )

    id_caracteristica = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    id_pergunta = Column(Integer, nullable=False)
    caracteristica = Column(String(45), nullable=False)
    fator = Column(
        Enum(FatoresDiscEnum, values_callable=lambda obj: [e.value for e in obj])
    )
    criado_em = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    atualizado_em = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    perguntas_ = relationship("Perguntas", back_populates="caracteristicas_disc")
