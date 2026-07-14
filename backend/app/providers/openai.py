"""OpenAI provider adapter — calls the Chat Completions API directly."""
import httpx

from app.config.settings import get_settings
from app.core.exceptions import ProviderException
from app.providers.base import BaseProvider, ProviderMessage, ProviderResponse

_API_URL = "https://api.openai.com/v1/chat/completions"
_DEFAULT_MODEL = "gpt-4o-mini"


class OpenAIProvider(BaseProvider):
    name = "openai"

    def __init__(self, model: str = _DEFAULT_MODEL):
        self.model = model
        self.settings = get_settings()

    def _build_request(self, messages: list[ProviderMessage]) -> tuple[str, dict, dict]:
        if not self.settings.OPENAI_API_KEY:
            raise ProviderException("OPENAI_API_KEY is not configured.")

        headers = {
            "Authorization": f"Bearer {self.settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }
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
            raise ProviderException(f"OpenAI request failed: {exc}") from exc

        try:
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise ProviderException(f"Unexpected OpenAI response shape: {data}") from exc

        usage = data.get("usage", {})
        return ProviderResponse(
            content=text,
            model=data.get("model", self.model),
            provider_name=self.name,
            raw=data,
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
            },
        )
