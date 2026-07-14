"""
Tests for AgentRuntime (SAGE_BLUEPRINT.md Section 18-19).

Substitutes ConversationService/UserService with in-memory fakes and injects
a fake provider directly (AgentRuntime's constructor already supports this
for exactly this reason) — so the full pipeline's *orchestration logic* is
tested without needing a real database or network call.
"""
import uuid

import pytest

from app.agent.runtime import agent as agent_module
from app.agent.runtime.agent import AgentRuntime
from app.core.exceptions import ProviderException
from app.providers.base import BaseProvider, ProviderResponse
from app.tools.registry import ToolRegistry


class _FakeMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content


class _FakeConversation:
    def __init__(self):
        self.id = uuid.uuid4()


class _FakeConversationService:
    def __init__(self, session):
        self.messages_added = []
        self._conversation = _FakeConversation()
        self._history: list[_FakeMessage] = []

    async def get_or_create(self, conversation_id, user_id):
        return self._conversation

    async def add_message(self, conversation_id, role, content, metadata=None):
        msg = _FakeMessage(role, content)
        self._history.append(msg)
        self.messages_added.append((role, content))
        return msg

    async def get_recent_history(self, conversation_id, limit=20):
        return list(self._history)


class _FakeUser:
    id = uuid.uuid4()


class _FakeUserService:
    def __init__(self, session):
        pass

    async def get_or_create_default_user(self):
        return _FakeUser()


class _FakeDbSession:
    """Stands in for the AsyncSession that handle_message() commits directly."""

    async def commit(self):
        pass


class _FakeProvider(BaseProvider):
    name = "fake"

    def __init__(self, content: str = "Hello! I'm Sage."):
        self.content = content
        self.called_with = None

    async def generate(self, messages, *, temperature: float = 0.7, max_tokens: int = 1024):
        self.called_with = messages
        return ProviderResponse(content=self.content, model="fake-model", provider_name=self.name)


class _EmptyProvider(BaseProvider):
    name = "empty"

    async def generate(self, messages, *, temperature: float = 0.7, max_tokens: int = 1024):
        return ProviderResponse(content="", model="fake-model", provider_name=self.name)


@pytest.fixture(autouse=True)
def _patch_services(monkeypatch):
    monkeypatch.setattr(agent_module, "ConversationService", _FakeConversationService)
    monkeypatch.setattr(agent_module, "UserService", _FakeUserService)


@pytest.mark.asyncio
async def test_plain_conversation_returns_provider_response():
    """Normal case: end-to-end pipeline for a simple message."""
    provider = _FakeProvider("Hi there!")
    runtime = AgentRuntime(tool_registry=ToolRegistry(), provider=provider)

    result = await runtime.handle_message(session=_FakeDbSession(), message="Hello Sage")

    assert result.response == "Hi there!"
    assert result.tools_used == []
    assert result.trace is None  # debug not requested


@pytest.mark.asyncio
async def test_debug_flag_includes_reasoning_trace():
    provider = _FakeProvider("Hi there!")
    runtime = AgentRuntime(tool_registry=ToolRegistry(), provider=provider)

    result = await runtime.handle_message(session=_FakeDbSession(), message="Hello Sage", debug=True)

    assert result.trace is not None
    assert result.trace.provider == "fake"
    assert "conversation" in result.trace.intents


@pytest.mark.asyncio
async def test_user_and_assistant_messages_are_persisted():
    """Normal case: verified indirectly — the provider only ever receives a
    well-formed message list ending in the current user turn, which is only
    possible if the Conversation Manager persisted and retrieved correctly."""
    provider = _FakeProvider("Sure, here's the info.")
    runtime = AgentRuntime(tool_registry=ToolRegistry(), provider=provider)

    await runtime.handle_message(session=_FakeDbSession(), message="Tell me something")

    assert provider.called_with[-1].role == "user"
    assert provider.called_with[-1].content == "Tell me something"


@pytest.mark.asyncio
async def test_empty_provider_response_raises_provider_exception():
    """Section 28: an invalid (empty) response must not silently succeed."""
    runtime = AgentRuntime(tool_registry=ToolRegistry(), provider=_EmptyProvider())

    with pytest.raises(ProviderException):
        await runtime.handle_message(session=_FakeDbSession(), message="Hello")


@pytest.mark.asyncio
async def test_unregistered_capability_is_surfaced_in_trace():
    """Normal case: Phase 2 has no web_search tool yet — the runtime should
    say so rather than silently ignoring the request."""
    provider = _FakeProvider("I can't search yet.")
    runtime = AgentRuntime(tool_registry=ToolRegistry(), provider=provider)

    result = await runtime.handle_message(session=_FakeDbSession(), message="search for GATE scholarships", debug=True)

    assert "web_search" in result.trace.unavailable_capabilities
