"""
Module: questionary.py

This module contains the routes for handling

Routes:
    /questionary:
        GET: Retrieve all disc characteristics and questions from the database.
"""

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from personavix.src.database.database import get_db
from personavix.src.models.domain.questions import Perguntas
from personavix.src.models.domain.disc_characteristics import CaracteristicasDisc
from personavix.src.models.schemas import questionary
from personavix.logger import setup_logger
from personavix.src.dependencies.decode_and_verify_token import (
    TokenData,
    decode_and_verify_token,
)
from personavix.src.dependencies import guard_clauses

router = APIRouter(prefix="/questionary", tags=["Questionary"])


@router.get(
    "/",
    summary="Get all disc characteristics and questions.",
    description="Retrieves all disc characteristics and questions.",
    response_model=questionary.Questionary,
)
def get_questionary(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Retrieve a list of disc characteristics and questions.

    Args:
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        Questionary: A list of disc characteristics and questions.
    """
    if token_data.is_unique_access_link:
        guard_clauses.verify_permission_is_user(
            token_data.permission, token_data.access_flag
        )

    try:
        setup_logger().info(
            "Getting all disc characteristics in table CaracteristicasDisc."
        )
        all_questions: list[Perguntas] = db.query(Perguntas).all()
        all_disc_characteristics: list[CaracteristicasDisc] = db.query(
            CaracteristicasDisc
        ).all()

        formatted_response = {
            "questions": all_questions,
            "disc_characteristics": all_disc_characteristics,
        }

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error getting questions.",
        ) from e

    return formatted_response
