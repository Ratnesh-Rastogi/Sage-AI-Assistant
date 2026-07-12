"""
Database connection setup.

SAGE_BLUEPRINT.md Section 64: PostgreSQL + SQLAlchemy 2.x (async) + Alembic.
SQLite must never be used as the primary database (Section 10 / 64).
"""
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


def _build_engine() -> AsyncEngine:
    if not settings.DATABASE_URL.startswith("postgresql"):
        raise ValueError(
            "DATABASE_URL must point to PostgreSQL. "
            "SQLite is intentionally unsupported (SAGE_BLUEPRINT.md Section 10)."
        )
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_pre_ping=True,
    )


engine: AsyncEngine = _build_engine()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=None,  # uses AsyncSession by default via async_sessionmaker
    expire_on_commit=False,
)


async def check_database_connection() -> bool:
    """Used by health checks and startup verification."""
    from sqlalchemy import text

    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return True
