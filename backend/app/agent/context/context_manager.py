"""
Context Builder.

SAGE_BLUEPRINT.md Section 23: constructs the final prompt sent to the
configured provider, respecting the context priority order:

    Current User Message > Tool Results > Relevant Memory >
    Recent Conversation > Conversation Summary > Older Context

Only relevant information is included — this module is where token budget
discipline lives, not the Provider Interface.
"""
from app.models.message import Message
from app.providers.base import ProviderMessage

_SYSTEM_INSTRUCTIONS = (
    "You are Sage, a private, self-hosted personal AI assistant. Be direct, "
    "accurate, and transparent about what you know versus what you're "
    "inferring. If you're uncertain, say so rather than fabricating an answer."
)


class ContextBuilder:
    def build(
        self,
        user_message: str,
        tool_outputs: list[dict] | None = None,
        relevant_memories: list[str] | None = None,
        recent_messages: list[Message] | None = None,
        unavailable_capabilities: list[str] | None = None,
    ) -> list[ProviderMessage]:
        system_sections = [_SYSTEM_INSTRUCTIONS]

        if tool_outputs:
            formatted = "\n".join(
                f"- {t['tool']} ({t['capability']}): {t['output']}" for t in tool_outputs
            )
            system_sections.append(f"Tool results available for this turn:\n{formatted}")

        if relevant_memories:
            formatted = "\n".join(f"- {m}" for m in relevant_memories)
            system_sections.append(f"Relevant things you know about the user:\n{formatted}")

        if unavailable_capabilities:
            formatted = ", ".join(unavailable_capabilities)
            system_sections.append(
                f"Note: the user's request implied these capabilities, which "
                f"aren't available yet: {formatted}. Say so plainly rather "
                f"than pretending to have performed the action."
            )

        messages: list[ProviderMessage] = [
            ProviderMessage(role="system", content="\n\n".join(system_sections))
        ]

        for msg in recent_messages or []:
            if msg.role in ("user", "assistant"):
                messages.append(ProviderMessage(role=msg.role, content=msg.content))

        messages.append(ProviderMessage(role="user", content=user_message))
        return messages
