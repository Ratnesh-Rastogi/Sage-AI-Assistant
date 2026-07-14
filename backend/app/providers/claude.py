"""Claude (Anthropic) provider adapter — calls the Messages API directly."""
import httpx

from app.config.settings import get_settings
from app.core.exceptions import ProviderException
from app.providers.base import BaseProvider, ProviderMessage, ProviderResponse

_API_URL = "https://api.anthropic.com/v1/messages"
_ANTHROPIC_VERSION = "2023-06-01"
_DEFAULT_MODEL = "claude-sonnet-4-6"


class ClaudeProvider(BaseProvider):
    name = "claude"

    def __init__(self, model: str = _DEFAULT_MODEL):
        self.model = model
        self.settings = get_settings()

    def _build_request(self, messages: list[ProviderMessage]) -> tuple[str, dict, dict]:
        if not self.settings.CLAUDE_API_KEY:
            raise ProviderException("CLAUDE_API_KEY is not configured.")

        headers = {
            "x-api-key": self.settings.CLAUDE_API_KEY,
            "anthropic-version": _ANTHROPIC_VERSION,
            "Content-Type": "application/json",
        }

        system_parts = [m.content for m in messages if m.role == "system"]
        conversation = [
            {"role": m.role, "content": m.content} for m in messages if m.role != "system"
        ]

        body: dict = {"model": self.model, "messages": conversation}
        if system_parts:
            body["system"] = "\n".join(system_parts)

        return _API_URL, headers, body

    async def generate(
        self,
        messages: list[ProviderMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> ProviderResponse:
        url, headers, body = self._build_request(messages)
        body["temperature"] = temperature
        body["max_tokens"] = max_tokens

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, headers=headers, json=body)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            raise ProviderException(f"Claude request failed: {exc}") from exc

        try:
            text = "".join(
                block.get("text", "") for block in data["content"] if block.get("type") == "text"
            )
        except (KeyError, TypeError) as exc:
            raise ProviderException(f"Unexpected Claude response shape: {data}") from exc

        usage = data.get("usage", {})
        return ProviderResponse(
            content=text,
            model=data.get("model", self.model),
            provider_name=self.name,
            raw=data,
            usage={
                "prompt_tokens": usage.get("input_tokens", 0),
                "completion_tokens": usage.get("output_tokens", 0),
            },
        )
