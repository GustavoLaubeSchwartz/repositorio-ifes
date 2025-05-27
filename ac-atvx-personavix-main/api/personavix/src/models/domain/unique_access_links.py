"""
Module: unique_access_links.py

This module contains the domain models for the unique access links.

Classes:
    LinksAcessoUnico: Represents the settings of the unique access links.
"""

# pylint: disable=import-error, duplicate-code
from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from personavix.src.database.database import Base


class LinksAcessoUnico(Base):  # pylint: disable=too-few-public-methods
    """
    Represents the settings of the unique access links.

    Attributes:
        id_configuracao (int): The unique identifier of the settings.
        tempo_validade (int): The validity time of the link.
        tempo_resposta (int): The time to answer the link.
    """

    __tablename__ = "links_acesso_unico"
    __table_args__ = (
        ForeignKeyConstraint(
            ["id_usuario"],
            ["usuarios.id_usuario"],
            ondelete="CASCADE",
            name="fk_links_acesso_unico_usuarios",
        ),
        ForeignKeyConstraint(
            ["id_resposta"],
            ["respostas.id_resposta"],
            name="fk_links_acesso_unico_respostas",
            ondelete="CASCADE",
        ),
    )

    id_sessao = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    id_usuario = Column(Integer, nullable=False)
    link = Column(String(255), nullable=False)
    senha_hash = Column(String(60))
    respondido = Column(TINYINT, nullable=False, server_default=text("'0'"))
    id_resposta = Column(Integer)
    criado_em = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    respondido_em = Column(
        DateTime,
        nullable=False,
    )

    usuarios_ = relationship("Usuarios", back_populates="links_acesso_unico")
