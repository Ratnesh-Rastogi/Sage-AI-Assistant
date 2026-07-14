"""Chat API schemas. SAGE_BLUEPRINT.md Section 92."""
from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000)
    conversation_id: UUID | None = None
    provider: str | None = Field(
        default=None, description="Override the configured default AI provider for this request."
    )
    debug: bool = Field(
        default=False, description="Include the internal reasoning trace in the response."
    )


class ReasoningTraceSchema(BaseModel):
    intents: list[str]
    tools_used: list[str]
    unavailable_capabilities: list[str]
    warnings: list[str]
    provider: str
    model: str


class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID
    tools_used: list[str]
    trace: ReasoningTraceSchema | None = None
