"""
Health check route.

Used to verify the application starts and the database is reachable
(Backend Acceptance Criteria, SAGE_BLUEPRINT.md Section 107).
"""
from fastapi import APIRouter

from app.database.connection import check_database_connection
from app.logging.logger import get_logger

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health")
async def health_check() -> dict:
    """Basic liveness check — does not touch the database."""
    return {"status": "ok", "service": "sage-backend"}


@router.get("/health/db")
async def health_check_database() -> dict:
    """Readiness check — verifies the PostgreSQL connection is alive."""
    try:
        await check_database_connection()
        return {"status": "ok", "database": "connected"}
    except Exception as exc:  # noqa: BLE001 — surfaced deliberately for a health check
        logger.error("Database health check failed: %s", exc)
        return {"status": "error", "database": "unreachable", "detail": str(exc)}
