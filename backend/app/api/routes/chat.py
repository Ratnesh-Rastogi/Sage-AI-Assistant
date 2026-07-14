"""
Chat routes.

SAGE_BLUEPRINT.md Section 92: POST /chat sends a message to Sage and returns
the Agent Runtime's response. Streaming (WS /chat/stream) is deferred to
Phase 6 (Section 115 groups it with the frontend chat interface).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.runtime.agent import AgentRuntime
from app.api.dependencies import get_agent_runtime, get_db
from app.core.exceptions import BaseApplicationException
from app.schemas.chat import ChatRequest, ChatResponse, ReasoningTraceSchema

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def send_message(
    payload: ChatRequest,
    session: AsyncSession = Depends(get_db),
    runtime: AgentRuntime = Depends(get_agent_runtime),
) -> ChatResponse:
    try:
        result = await runtime.handle_message(
            session=session,
            message=payload.message,
            conversation_id=payload.conversation_id,
            provider_name=payload.provider,
            debug=payload.debug,
        )
    except BaseApplicationException:
        raise  # handled by the application_exception_handler in main.py

    trace = None
    if result.trace is not None:
        trace = ReasoningTraceSchema(
            intents=result.trace.intents,
            tools_used=result.trace.tools_used,
            unavailable_capabilities=result.trace.unavailable_capabilities,
            warnings=result.trace.warnings,
            provider=result.trace.provider,
            model=result.trace.model,
        )

    return ChatResponse(
        response=result.response,
        conversation_id=result.conversation_id,
        tools_used=result.tools_used,
        trace=trace,
    )
