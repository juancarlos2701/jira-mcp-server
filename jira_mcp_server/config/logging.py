"""Logging configuration for the application.

This module provides a centralized function to configure the Python
logging framework based on environment variables. It sets up a
formatter and a handler that directs logs either to a file or
to stderr.
"""

import logging
import os
import sys


def setup_logging() -> None:
    """Set up logging configuration.

    Configures the root logger based on environment variables.

    - ``LOG_LEVEL``: The logging level (e.g., 'DEBUG', 'INFO', 'WARNING').
      Defaults to 'INFO'.
    - ``LOG_FILE``: The name of the file for logging (e.g., 'app.log').
      If provided, the file will be created inside a ``logs/`` directory.
      If not provided, logs are directed to ``sys.stderr``.
    """
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_file = os.environ.get("LOG_FILE", None)

    logger = logging.getLogger()

    # Clear existing handlers to prevent duplicate log entries
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Direct logs to file if specified, otherwise to stderr
    if log_file:
        log_dir = "logs"
        # Ensure the log directory exists
        os.makedirs(log_dir, exist_ok=True)
        # Create the full path for the log file
        log_path = os.path.join(log_dir, log_file)
        handler = logging.FileHandler(log_path)
    else:
        handler = logging.StreamHandler(sys.stderr)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
