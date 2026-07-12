"""Tests for the structured logging system (SAGE_BLUEPRINT.md Section 13)."""
import logging
import os

from app.logging.logger import configure_logging, get_logger


def test_configure_logging_creates_log_directory(tmp_path, monkeypatch):
    from app.config import settings as settings_module

    log_dir = str(tmp_path / "logs")
    monkeypatch.setenv("LOG_DIR", log_dir)
    settings_module.get_settings.cache_clear()

    import app.logging.logger as logger_module

    logger_module._configured = False
    configure_logging()

    assert os.path.isdir(log_dir)

    monkeypatch.delenv("LOG_DIR", raising=False)
    settings_module.get_settings.cache_clear()


def test_get_logger_returns_named_logger():
    logger = get_logger("sage.test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "sage.test"
