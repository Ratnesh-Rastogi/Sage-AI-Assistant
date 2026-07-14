"""
Response Formatter + Internal Reasoning Trace.

SAGE_BLUEPRINT.md Section 29: converts validated output into frontend-ready
content. Presentation-only — no business logic here.

SAGE_BLUEPRINT.md Section 30: the internal reasoning trace is a structured
record of system actions (not chain-of-thought), intended for debugging and
not shown to the user unless a dedicated debug mode is enabled.
"""
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class ReasoningTrace:
    intents: list[str]
    tools_used: list[str]
    unavailable_capabilities: list[str]
    warnings: list[str]
    provider: str
    model: str


@dataclass
class AgentResponse:
    response: str
    conversation_id: UUID
    tools_used: list[str] = field(default_factory=list)
    trace: ReasoningTrace | None = None


class ResponseFormatter:
    def format(
        self,
        *,
        content: str,
        conversation_id: UUID,
        tools_used: list[str],
        trace: ReasoningTrace | None = None,
        include_trace: bool = False,
    ) -> AgentResponse:
        return AgentResponse(
            response=content,
            conversation_id=conversation_id,
            tools_used=tools_used,
            trace=trace if include_trace else None,
        )
