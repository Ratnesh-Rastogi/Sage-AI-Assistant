"""
Tests for provider adapters (SAGE_BLUEPRINT.md Section 27).

These test request construction and configuration validation only — no real
network calls are made, since `_build_request()` is fully deterministic and
side-effect free.
"""
import pytest

from app.core.exceptions import ProviderException
from app.providers.base import ProviderMessage
from app.providers.claude import ClaudeProvider
from app.providers.factory import get_provider, list_supported_providers
from app.providers.gemini import GeminiProvider
from app.providers.openai import OpenAIProvider
from app.providers.openrouter import OpenRouterProvider


def _sample_messages() -> list[ProviderMessage]:
    return [
        ProviderMessage(role="system", content="You are Sage."),
        ProviderMessage(role="user", content="Hello"),
    ]


class TestGeminiProvider:
    def test_raises_without_api_key(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "")
        from app.config import settings as settings_module

        settings_module.get_settings.cache_clear()
        provider = GeminiProvider()
        with pytest.raises(ProviderException):
            provider._build_request(_sample_messages())
        settings_module.get_settings.cache_clear()

    def test_builds_request_with_api_key(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key")
        from app.config import settings as settings_module

        settings_module.get_settings.cache_clear()
        provider = GeminiProvider()
        url, headers, body = provider._build_request(_sample_messages())

        assert "test-key" in url
        assert body["systemInstruction"]["parts"][0]["text"] == "You are Sage."
        assert body["contents"][0]["role"] == "user"
        settings_module.get_settings.cache_clear()


class TestOpenAIProvider:
    def test_raises_without_api_key(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "")
        from app.config import settings as settings_module

        settings_module.get_settings.cache_clear()
        provider = OpenAIProvider()
        with pytest.raises(ProviderException):
            provider._build_request(_sample_messages())
        settings_module.get_settings.cache_clear()

    def test_builds_request_with_api_key(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        from app.config import settings as settings_module

        settings_module.get_settings.cache_clear()
        provider = OpenAIProvider()
        url, headers, body = provider._build_request(_sample_messages())

        assert headers["Authorization"] == "Bearer test-key"
        assert body["messages"][0]["role"] == "system"
        settings_module.get_settings.cache_clear()


class TestClaudeProvider:
    def test_raises_without_api_key(self, monkeypatch):
        monkeypatch.setenv("CLAUDE_API_KEY", "")
        from app.config import settings as settings_module

        settings_module.get_settings.cache_clear()
        provider = ClaudeProvider()
        with pytest.raises(ProviderException):
            provider._build_request(_sample_messages())
        settings_module.get_settings.cache_clear()

    def test_system_message_extracted_separately(self, monkeypatch):
        """Claude's Messages API takes `system` as a top-level field, not a
        message with role='system' — this is exactly the kind of
        provider-specific quirk the adapter layer exists to hide."""
        monkeypatch.setenv("CLAUDE_API_KEY", "test-key")
        from app.config import settings as settings_module

        settings_module.get_settings.cache_clear()
        provider = ClaudeProvider()
        url, headers, body = provider._build_request(_sample_messages())

        assert body["system"] == "You are Sage."
        assert all(m["role"] != "system" for m in body["messages"])
        settings_module.get_settings.cache_clear()


class TestOpenRouterProvider:
    def test_raises_without_api_key(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "")
        from app.config import settings as settings_module

        settings_module.get_settings.cache_clear()
        provider = OpenRouterProvider()
        with pytest.raises(ProviderException):
            provider._build_request(_sample_messages())
        settings_module.get_settings.cache_clear()

    def test_builds_request_with_api_key(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
        from app.config import settings as settings_module

        settings_module.get_settings.cache_clear()
        provider = OpenRouterProvider()
        url, headers, body = provider._build_request(_sample_messages())

        assert headers["Authorization"] == "Bearer test-key"
        assert body["messages"][0]["role"] == "system"
        assert "openrouter.ai" in url
        settings_module.get_settings.cache_clear()


class TestProviderFactory:
    def test_default_provider_is_returned_when_unspecified(self, monkeypatch):
        monkeypatch.setenv("DEFAULT_AI_PROVIDER", "openai")
        from app.config import settings as settings_module

        settings_module.get_settings.cache_clear()
        provider = get_provider()
        assert isinstance(provider, OpenAIProvider)
        settings_module.get_settings.cache_clear()

    def test_explicit_provider_name_overrides_default(self):
        provider = get_provider("claude")
        assert isinstance(provider, ClaudeProvider)

    def test_unknown_provider_raises(self):
        with pytest.raises(ProviderException):
            get_provider("not-a-real-provider")

    def test_lists_all_four_supported_providers(self):
        assert set(list_supported_providers()) == {"gemini", "openai", "claude", "openrouter"}
