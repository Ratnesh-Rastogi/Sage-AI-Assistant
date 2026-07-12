"""
Integration tests (SAGE_BLUEPRINT.md Section 106 / PROJECT_STRUCTURE.md tests/integration).

These exercise the full request flow: FastAPI route -> service -> database engine,
as opposed to the unit tests under backend/app/tests which mock or isolate layers.

Requires a reachable PostgreSQL instance (e.g. `docker compose up postgres`).
Skips gracefully if the database isn't reachable, so `pytest` still runs in
environments without Docker.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from httpx import ASGITransport, AsyncClient  # noqa: E402

from app.database.connection import check_database_connection  # noqa: E402
from app.main import app  # noqa: E402


async def _database_reachable() -> bool:
    try:
        await check_database_connection()
        return True
    except Exception:
        return False


@pytest.mark.asyncio
async def test_health_endpoint_reports_database_status():
    """Normal case: the /health/db route reflects real DB connectivity."""
    reachable = await _database_reachable()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health/db")

    assert response.status_code == 200
    body = response.json()
    expected_status = "ok" if reachable else "error"
    assert body["status"] == expected_status
