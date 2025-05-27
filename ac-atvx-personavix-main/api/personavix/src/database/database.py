"""
Module: database.py

This module contains the database configuration and connection setup.

Functions:
    get_db: Get a database instance.
"""

# pylint: disable=import-error
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_SCHEMA = os.getenv("DB_SCHEMA")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}"

engine = create_engine(DATABASE_URL, echo=True)  # Set echo=True for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Get a database instance.

    Returns:
        generator: An instance of the database created with SessionLocal.

    Example usage:
        with get_db() as db:
            # perform database operations using db
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
