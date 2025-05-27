"""
Module: answers.py

This module contains the routes for handling answers-related tasks.

Routes:
    /answers:
        GET: Retrieve all answers from the database.
        POST: Register a new test response in the database.
    /answers/{id_answer}:
        GET: Retrieve a specific answer from the database.
"""

# pylint: disable=import-error
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from personavix.src.database.database import get_db
from personavix.src.models.domain.unique_access_links import LinksAcessoUnico
from personavix.src.models.domain.answers import Respostas
from personavix.src.models.schemas import answers
from personavix.logger import setup_logger
from personavix.src.dependencies.decode_and_verify_token import (
    TokenData,
    decode_and_verify_token,
)
from personavix.src.dependencies import guard_clauses


router = APIRouter(prefix="/answers", tags=["Answers"])


@router.get(
    "/",
    summary="Get all answers",
    description="Retrieves all answers from the database.",
    response_model=list[answers.AnswersWithUser],
)
def get_answers(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Retrieve a list of answers.

    Args:
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        List[Answer]: A list of answers.
    """
    guard_clauses.verify_permission_is_manager(
        token_data.permission, token_data.access_flag
    )

    try:
        setup_logger().info("Getting all answers in table Answers.")
        all_answers: list[Respostas] = db.query(Respostas).all()

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error getting answers"
        ) from e

    return all_answers


@router.get(
    "/{id_answer}",
    summary="Get a specific answer",
    description="Retrieve a specific answer from the database.",
    response_model=answers.Answer,
)
def get_answer(
    id_answer: int,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Retrieve a specific answer from the database.

    Args:
        id_answer: The id of the answer to be retrieved.
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        Answer: The answer object.

    Raises:
        HTTPException: Raised when answer with specified id is not found (404).
    """
    if not token_data.is_unique_access_link:
        guard_clauses.verify_permission_is_user(
            token_data.permission, token_data.access_flag
        )

    try:
        setup_logger().info("Getting answer with id %s in table Answers", id_answer)
        answer: Respostas = (
            db.query(Respostas).filter(Respostas.id_resposta == id_answer).first()
        )

        if not answer:
            setup_logger().error(
                "Code:404 Message: Answer with id %s not found", id_answer
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Answer not found"
            )

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error retrieving answer",
        ) from e

    return answer


@router.post(
    "/{id_user}",
    summary="Cadastre a new test response",
    description="Cadastre a new test response in the database.",
    response_model=answers.Answer,
)
def cadastre_a_test_response(
    id_user: int,
    answer: answers.AnswersCreate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(decode_and_verify_token),
):
    """
    Register a new test response in the database.

    Args:
        id_user: The id of the user who is registering the answer.
        answer: The answer to be registered.
        db: Database session dependency. Defaults to Depends(get_db).
        token_data (TokenData): Defaults to Depends(decode_and_verify_token).

    Returns:
        Answer: The registered answer.
    """
    if not token_data.is_unique_access_link:
        guard_clauses.verify_permission_is_user(
            token_data.permission, token_data.access_flag
        )

    try:
        setup_logger().info("Registering a new test response in table Answers.")

        new_answer = Respostas(
            id_usuario=id_user,
            dominancia=answer.dominancia,
            influencia=answer.influencia,
            estabilidade=answer.estabilidade,
            conformidade=answer.conformidade,
            motivo=answer.motivo,
        )
        db.add(new_answer)
        db.commit()
        db.refresh(new_answer)

        if answer.id_sessao:
            link: LinksAcessoUnico = (
                db.query(LinksAcessoUnico)
                .filter(LinksAcessoUnico.id_sessao == answer.id_sessao)
                .first()
            )

            if link:
                link.id_resposta = new_answer.id_resposta
                link.respondido = 1
                db.commit()

    except IntegrityError as e:
        setup_logger().error("Code:400 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Error registering test response"
        ) from e

    except SQLAlchemyError as e:
        setup_logger().error("Code:500 Message: %s", e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error registering test response",
        ) from e

    return new_answer
