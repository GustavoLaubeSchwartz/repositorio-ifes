"""
This module contains the 'Usuarios' class,
which represents the 'Usuarios' table in the database.
"""

# pylint: disable=import-error
from sqlalchemy import Column, Integer, DateTime, text, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from personavix.src.database.database import Base


class Usuarios(Base):  # pylint: disable=too-few-public-methods
    """
    Represents cadastered users.

    Attributes:
        id_usuario (int): The unique identifier of the user.
        nome (str): The name of the user.
        email (str): The email address of the user.
        telefone (str): The telephone number of the user.
        flag_acesso (int): The access flag indicating whether the user has access (1) or not
        (0).
        permissao (int): The permission level of the user.
        setor (str): The sector of the user.
        senha_hash (str): The hashed password of the user.
        criado_em (DateTime): The timestamp of the creation of the user record.
        atualizado_em (DateTime): The timestamp of the last update of the user record.
    """

    __tablename__ = "usuarios"

    id_usuario = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    nome = Column(String(80))
    email = Column(String(80))
    telefone = Column(String(30))
    flag_acesso = Column(TINYINT, nullable=False, server_default=text("'0'"))
    permissao = Column(Integer, nullable=False, server_default=text("'0'"))
    setor = Column(String(45))
    senha_hash = Column(String(60))
    criado_em = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    atualizado_em = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    links_acesso_unico = relationship("LinksAcessoUnico", back_populates="usuarios_")
    respostas = relationship("Respostas", back_populates="usuarios_")
