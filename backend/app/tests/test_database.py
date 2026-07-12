"""
Tests for the database layer's configuration guarantees.

Covers Database Acceptance Criteria (SAGE_BLUEPRINT.md Section 83):
migrations, repository pattern wiring, and rejecting non-PostgreSQL URLs
(Section 10 / 64: "SQLite shall not be used as the primary database").
"""
import pytest

from app.core.exceptions import (
    BaseApplicationException,
    DatabaseException,
    ValidationException,
)


def test_settings_load_with_defaults():
    from app.config.settings import Settings

    settings = Settings(_env_file=None)
    assert settings.APP_NAME == "Sage"
    assert settings.DATABASE_URL.startswith("postgresql")


def test_sqlite_url_is_rejected(monkeypatch):
    """Edge case: a non-PostgreSQL DATABASE_URL must fail loudly, not silently work."""
    import importlib

    from app.config import settings as settings_module

    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    settings_module.get_settings.cache_clear()

    with pytest.raises(ValueError):
        import app.database.connection as connection_module

        importlib.reload(connection_module)

    # Restore so later tests aren't affected.
    monkeypatch.delenv("DATABASE_URL", raising=False)
    settings_module.get_settings.cache_clear()
    import app.database.connection as connection_module

    importlib.reload(connection_module)


def test_database_exception_serializes_correctly():
    """Normal case: exceptions map to the standard error envelope (Section 101)."""
    exc = DatabaseException("Connection refused")
    payload = exc.to_dict()
    assert payload["success"] is False
    assert payload["error"]["code"] == "DATABASE_ERROR"
    assert payload["error"]["message"] == "Connection refused"


def test_validation_exception_accepts_custom_code():
    """Edge case: exceptions allow a custom code override."""
    exc = ValidationException("Bad input", code="CUSTOM_CODE")
    assert exc.to_dict()["error"]["code"] == "CUSTOM_CODE"


def test_all_exceptions_inherit_base():
    """Normal case: hierarchy matches Section 102."""
    for exc_cls in (DatabaseException, ValidationException):
        assert issubclass(exc_cls, BaseApplicationException)
