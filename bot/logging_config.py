"""
Centralized logging configuration for the Trading Bot.

Provides a reusable logger that writes structured output to both
the console (human-readable) and a rotating log file for auditing.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Default log directory and file
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "trading_bot.log")

# Log format constants
CONSOLE_FORMAT = "%(asctime)s │ %(levelname)-8s │ %(message)s"
FILE_FORMAT = "%(asctime)s │ %(levelname)-8s │ %(name)s │ %(funcName)s:%(lineno)d │ %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    name: str = "trading_bot",
    log_file: str = LOG_FILE,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    max_bytes: int = 5 * 1024 * 1024,  # 5 MB
    backup_count: int = 3,
) -> logging.Logger:
    """
    Create and configure a logger instance.

    Args:
        name: Logger name (typically module name).
        log_file: Path to the log file.
        console_level: Minimum level for console output.
        file_level: Minimum level for file output.
        max_bytes: Maximum size of each log file before rotation.
        backup_count: Number of rotated log files to keep.

    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # ── Console Handler ──────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter(CONSOLE_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(console_handler)

    # ── File Handler (rotating) ──────────────────────────────
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(logging.Formatter(FILE_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(file_handler)

    logger.debug("Logger '%s' initialized → %s", name, log_file)
    return logger
