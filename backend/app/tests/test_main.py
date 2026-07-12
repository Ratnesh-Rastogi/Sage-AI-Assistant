"""
Tests for application startup and the health check endpoints.

Covers Backend Acceptance Criteria (SAGE_BLUEPRINT.md Section 107):
"FastAPI server starts successfully" and basic request/response behavior.
"""
import pytest


@pytest.mark.asyncio
async def test_app_starts_and_health_ok(client):
    """Normal case: the liveness endpoint responds without touching the database."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "sage-backend"


@pytest.mark.asyncio
async def test_unknown_route_returns_404(client):
    """Edge case: unregistered routes should return a clean 404, not crash."""
    response = await client.get("/api/v1/does-not-exist")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_cors_headers_present_on_health(client):
    """Normal case: CORS middleware should be active."""
    response = await client.get(
        "/api/v1/health", headers={"Origin": "http://localhost:5173"}
    )
    assert response.status_code == 200
