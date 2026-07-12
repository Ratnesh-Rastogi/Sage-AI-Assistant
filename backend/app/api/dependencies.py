"""
Shared FastAPI dependencies.

Per SAGE_BLUEPRINT.md Section 100, dependency injection is used for
database sessions, services, providers, and configuration.
"""
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Settings, get_settings
from app.database.session import get_db_session


async def get_db(
    session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[AsyncSession, None]:
    yield session


def get_app_settings() -> Settings:
    return get_settings()
