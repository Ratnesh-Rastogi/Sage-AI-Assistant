"""Shared pytest fixtures for backend tests."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.tools.bootstrap import bootstrap_tools

# ASGITransport doesn't reliably trigger FastAPI's lifespan startup event
# (where bootstrap_tools() normally runs — see app/main.py), so tests that
# exercise the tool registry need it called explicitly. Idempotent: safe to
# call more than once.
bootstrap_tools()


@pytest.fixture
async def client():
    """An async HTTP client wired directly to the FastAPI app (no live server needed)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
