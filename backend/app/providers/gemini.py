"""
Gemini provider adapter.

Calls Google's Generative Language API directly over HTTPS so Sage doesn't
take on a heavyweight SDK dependency for something the Provider Interface
already abstracts (SAGE_BLUEPRINT.md Section 8/27).
"""
import httpx

from app.config.settings import get_settings
from app.core.exceptions import ProviderException
from app.providers.base import BaseProvider, ProviderMessage, ProviderResponse

_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
_DEFAULT_MODEL = "gemini-2.0-flash"


class GeminiProvider(BaseProvider):
    name = "gemini"

    def __init__(self, model: str = _DEFAULT_MODEL):
        self.model = model
        self.settings = get_settings()

    def _build_request(self, messages: list[ProviderMessage]) -> tuple[str, dict, dict]:
        if not self.settings.GEMINI_API_KEY:
            raise ProviderException("GEMINI_API_KEY is not configured.")

        url = f"{_API_BASE}/{self.model}:generateContent?key={self.settings.GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}

        system_parts = [m.content for m in messages if m.role == "system"]
        contents = [
            {
                "role": "model" if m.role == "assistant" else "user",
                "parts": [{"text": m.content}],
            }
            for m in messages
            if m.role != "system"
        ]

        body: dict = {"contents": contents}
        if system_parts:
            body["systemInstruction"] = {"parts": [{"text": "\n".join(system_parts)}]}

        return url, headers, body

    async def generate(
        self,
        messages: list[ProviderMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> ProviderResponse:
        url, headers, body = self._build_request(messages)
        body["generationConfig"] = {"temperature": temperature, "maxOutputTokens": max_tokens}

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, headers=headers, json=body)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            raise ProviderException(f"Gemini request failed: {exc}") from exc

        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as exc:
            raise ProviderException(f"Unexpected Gemini response shape: {data}") from exc

        usage = data.get("usageMetadata", {})
        return ProviderResponse(
            content=text,
            model=self.model,
            provider_name=self.name,
            raw=data,
            usage={
                "prompt_tokens": usage.get("promptTokenCount", 0),
                "completion_tokens": usage.get("candidatesTokenCount", 0),
            },
        )
