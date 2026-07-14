"""
Response Validator.

SAGE_BLUEPRINT.md Section 28: validates before the response reaches the
user. Must improve reliability without fabricating content — it can only
flag/append, never invent replacement text.
"""
from dataclasses import dataclass, field

from app.providers.base import ProviderResponse


@dataclass
class ValidationResult:
    is_valid: bool
    warnings: list[str] = field(default_factory=list)


class ResponseValidator:
    def validate(
        self,
        response: ProviderResponse,
        unavailable_capabilities: list[str] | None = None,
    ) -> ValidationResult:
        warnings: list[str] = []

        if not response.content or not response.content.strip():
            return ValidationResult(is_valid=False, warnings=["Provider returned an empty response."])

        if unavailable_capabilities:
            warnings.append(
                f"Requested capabilities not yet available: {', '.join(unavailable_capabilities)}."
            )

        # Basic markdown sanity check: unbalanced code fences would render badly.
        if response.content.count("```") % 2 != 0:
            warnings.append("Response contains an unbalanced code block fence.")

        return ValidationResult(is_valid=True, warnings=warnings)
