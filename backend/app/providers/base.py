"""
Provider Interface.

SAGE_BLUEPRINT.md Section 27: a unified abstraction over all supported LLM
providers. The rest of Sage — specifically the Context Builder and Agent
Runtime — communicates only with this interface, never with a provider SDK
directly. Changing providers is a configuration change, not a code change.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal

Role = Literal["system", "user", "assistant"]


@dataclass
class ProviderMessage:
    """A single message in the conversation sent to the provider."""

    role: Role
    content: str


@dataclass
class ProviderResponse:
    """Normalized response shape, regardless of which provider produced it."""

    content: str
    model: str
    provider_name: str
    raw: dict[str, Any] = field(default_factory=dict)
    usage: dict[str, int] = field(default_factory=dict)


class BaseProvider(ABC):
    """Every provider adapter (Gemini, OpenAI, Claude, OpenRouter) implements this."""

    name: str = "base"

    @abstractmethod
    async def generate(
        self,
        messages: list[ProviderMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> ProviderResponse:
        """Send messages to the provider and return a normalized response.

        Implementations should raise app.core.exceptions.ProviderException
        on missing configuration or upstream failure — never fabricate a
        response (SAGE_BLUEPRINT.md Section 4: "Reliability").
        """
        raise NotImplementedError
