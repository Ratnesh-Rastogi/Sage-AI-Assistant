"""
Tests for POST /chat (SAGE_BLUEPRINT.md Section 92).

Overrides get_db and get_agent_runtime via FastAPI's dependency_overrides —
this exercises real request validation and response serialization without
needing a live database or LLM provider.
"""
import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.agent.runtime.response_formatter import AgentResponse, ReasoningTrace
from app.api.dependencies import get_agent_runtime, get_db
from app.main import app


class _FakeRuntime:
    def __init__(self, response: AgentResponse):
        self._response = response
        self.last_call_kwargs = None

    async def handle_message(self, **kwargs):
        self.last_call_kwargs = kwargs
        return self._response


@pytest.fixture
async def chat_client():
    conversation_id = uuid.uuid4()
    fake_runtime = _FakeRuntime(
        AgentResponse(response="Hi, I'm Sage.", conversation_id=conversation_id, tools_used=[])
    )

    async def _fake_db():
        yield object()  # never touched, since AgentRuntime itself is faked

    app.dependency_overrides[get_db] = _fake_db
    app.dependency_overrides[get_agent_runtime] = lambda: fake_runtime

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client, fake_runtime, conversation_id

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_returns_response_and_conversation_id(chat_client):
    """Normal case."""
    client, _, conversation_id = chat_client
    response = await client.post("/api/v1/chat", json={"message": "Hello Sage"})

    assert response.status_code == 200
    body = response.json()
    assert body["response"] == "Hi, I'm Sage."
    assert body["conversation_id"] == str(conversation_id)
    assert body["tools_used"] == []
    assert body["trace"] is None


@pytest.mark.asyncio
async def test_chat_rejects_empty_message(chat_client):
    """Invalid case: schema validation (min_length=1)."""
    client, _, _ = chat_client
    response = await client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_rejects_missing_message(chat_client):
    """Invalid case."""
    client, _, _ = chat_client
    response = await client.post("/api/v1/chat", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_passes_provider_override_through(chat_client):
    """Normal case: the `provider` field reaches AgentRuntime.handle_message."""
    client, fake_runtime, _ = chat_client
    await client.post("/api/v1/chat", json={"message": "Hi", "provider": "claude"})
    assert fake_runtime.last_call_kwargs["provider_name"] == "claude"


@pytest.mark.asyncio
async def test_chat_debug_trace_is_included_when_requested(chat_client):
    """Normal case: debug=True surfaces the reasoning trace in the response body."""
    client, _, _ = chat_client
    conversation_id = uuid.uuid4()
    trace = ReasoningTrace(
        intents=["conversation"],
        tools_used=[],
        unavailable_capabilities=[],
        warnings=[],
        provider="fake",
        model="fake-model",
    )
    app.dependency_overrides[get_agent_runtime] = lambda: _FakeRuntime(
        AgentResponse(response="hi", conversation_id=conversation_id, tools_used=[], trace=trace)
    )

    response = await client.post("/api/v1/chat", json={"message": "hi", "debug": True})
    assert response.status_code == 200
    assert response.json()["trace"]["provider"] == "fake"
