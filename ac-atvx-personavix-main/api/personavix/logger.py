"""
This module provides a function to set up the logger for the API.

The logger is initialized with a stream handler and a file handler.
Log messages are formatted with a specific format and written to both the console and a log file.
The logger level is set to INFO.

Functions:
    setup_logger: Set up the logger with handlers, formatters, and level.
"""

import logging
import sys
import datetime


def setup_logger() -> logging.Logger:
    """
    Set up the logger with handlers, formatters, and level.

    This function initializes the logger with a stream handler and a file handler.
    The log messages will be formatted with a specific format and written to both the console
    and a log file. The logger level is set to INFO.

    Args:
        page: The name of the page that will be logged.

    Returns:
        logging.Logger: The logger object.
    """
    # Get logger
    logger = logging.getLogger("api_logger")
    logger.handlers = []

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | "
        "%(filename)s | "
        "%(levelname)s | "
        "%(funcName)s:%(lineno)d | "
        "%(message)s"
    )

    # Create handlers
    stream_handler = logging.StreamHandler(sys.stdout)

    file_handler = logging.FileHandler(
        f"./personavix/src/logs/{datetime.date.today()}.log"
    )
    logger.propagate = False
    # Set formatter
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    # Disable propagation
    logger.propagate = False

    # Set logger level
    logger.setLevel(logging.INFO)
    return logger
