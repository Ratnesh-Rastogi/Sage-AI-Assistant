"""
Structured logging configuration for Sage.

Per SAGE_BLUEPRINT.md Section 13:
- Uses Python's standard logging module
- Structured log format
- Supports DEBUG / INFO / WARNING / ERROR / CRITICAL
- Logs written to logs/ with daily rotation
"""
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from app.config.settings import get_settings

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured = False


def configure_logging() -> None:
    """Configure root logging handlers exactly once per process."""
    global _configured
    if _configured:
        return

    settings = get_settings()
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(settings.LOG_DIR, "sage.log"),
        when="midnight",
        backupCount=14,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL.upper())
    root_logger.handlers = [console_handler, file_handler]

    # Quiet noisy third-party loggers unless we're debugging.
    if settings.LOG_LEVEL.upper() != "DEBUG":
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger. Call configure_logging() first at startup."""
    return logging.getLogger(name)
