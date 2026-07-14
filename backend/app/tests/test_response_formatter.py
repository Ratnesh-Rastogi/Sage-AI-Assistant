"""Tests for the Response Formatter (SAGE_BLUEPRINT.md Section 29-30)."""
import uuid

from app.agent.runtime.response_formatter import ReasoningTrace, ResponseFormatter


def _trace() -> ReasoningTrace:
    return ReasoningTrace(
        intents=["conversation"],
        tools_used=[],
        unavailable_capabilities=[],
        warnings=[],
        provider="gemini",
        model="gemini-2.0-flash",
    )


def test_trace_excluded_by_default():
    """Section 30: trace is 'not displayed to the user unless a dedicated
    debug mode is enabled.'"""
    formatter = ResponseFormatter()
    result = formatter.format(
        content="hi", conversation_id=uuid.uuid4(), tools_used=[], trace=_trace(), include_trace=False
    )
    assert result.trace is None


def test_trace_included_when_debug_enabled():
    formatter = ResponseFormatter()
    conv_id = uuid.uuid4()
    result = formatter.format(
        content="hi", conversation_id=conv_id, tools_used=["system_time"], trace=_trace(), include_trace=True
    )
    assert result.trace is not None
    assert result.trace.provider == "gemini"
    assert result.conversation_id == conv_id
    assert result.tools_used == ["system_time"]
