"""
Module: enums.py

This module contains the enum classes

Classes:
    FatoresDiscEnum (Enum): The possible disc factors.
"""

from enum import Enum


class FatoresDiscEnum(str, Enum):
    """
    This class defines the possible disc factors.

    Attributes:
        DOMINANCIA (str): The dominance factor.
        INFLUENCIA (str): The influence factor.
        ESTABILIDADE (str): The stability factor.
        CONFORMIDADE (str): The conformity factor
    """

    DOMINANCIA = "Dominância"
    INFLUENCIA = "Influência"
    ESTABILIDADE = "Estabilidade"
    CONFORMIDADE = "Conformidade"
