"""
Provider factory.

SAGE_BLUEPRINT.md Section 27: "This allows changing providers through
configuration. No business logic should depend on the provider." Callers
(Agent Runtime) ask for "the configured provider" — they never import a
concrete adapter directly.
"""
from app.config.settings import get_settings
from app.core.exceptions import ProviderException
from app.providers.base import BaseProvider
from app.providers.claude import ClaudeProvider
from app.providers.gemini import GeminiProvider
from app.providers.openai import OpenAIProvider
from app.providers.openrouter import OpenRouterProvider

_REGISTRY: dict[str, type[BaseProvider]] = {
    "gemini": GeminiProvider,
    "openai": OpenAIProvider,
    "claude": ClaudeProvider,
    "openrouter": OpenRouterProvider,
}


def get_provider(provider_name: str | None = None) -> BaseProvider:
    """Return an instance of the requested provider, or the configured default.

    Construction never touches the network or requires an API key — adapters
    validate their own configuration lazily, on the first `generate()` call.
    """
    settings = get_settings()
    name = (provider_name or settings.DEFAULT_AI_PROVIDER).lower()

    provider_cls = _REGISTRY.get(name)
    if provider_cls is None:
        raise ProviderException(
            f"Unknown provider '{name}'. Supported providers: {', '.join(_REGISTRY)}."
        )
    return provider_cls()


def list_supported_providers() -> list[str]:
    return list(_REGISTRY)
