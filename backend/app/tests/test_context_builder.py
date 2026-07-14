"""Tests for the Context Builder (SAGE_BLUEPRINT.md Section 23)."""
from app.agent.context.context_manager import ContextBuilder


def test_minimal_build_has_system_and_user_message():
    """Normal case."""
    builder = ContextBuilder()
    messages = builder.build(user_message="Hello Sage")

    assert messages[0].role == "system"
    assert messages[-1].role == "user"
    assert messages[-1].content == "Hello Sage"


def test_tool_outputs_are_included_in_system_context():
    builder = ContextBuilder()
    messages = builder.build(
        user_message="What time is it?",
        tool_outputs=[{"tool": "system_time", "capability": "get_current_time", "output": {"iso_timestamp": "2026-07-13T00:00:00Z"}}],
    )
    assert "system_time" in messages[0].content


def test_relevant_memories_are_included_in_system_context():
    builder = ContextBuilder()
    messages = builder.build(
        user_message="What do I prefer?",
        relevant_memories=["User prefers detailed explanations."],
    )
    assert "detailed explanations" in messages[0].content


def test_unavailable_capabilities_are_flagged_not_hidden():
    """Section 4 'Reliability': never fabricate confidence — the model should
    be told plainly when a capability wasn't actually available."""
    builder = ContextBuilder()
    messages = builder.build(user_message="search for X", unavailable_capabilities=["web_search"])
    assert "web_search" in messages[0].content


def test_recent_history_is_ordered_before_current_message():
    from app.models.message import Message

    builder = ContextBuilder()
    history = [
        Message(role="user", content="first turn"),
        Message(role="assistant", content="first reply"),
    ]
    messages = builder.build(user_message="second turn", recent_messages=history)

    contents = [m.content for m in messages]
    assert contents.index("first turn") < contents.index("first reply") < contents.index("second turn")


def test_no_optional_context_still_produces_valid_messages():
    """Edge case: nothing but the bare user message."""
    builder = ContextBuilder()
    messages = builder.build(user_message="hi")
    assert len(messages) == 2  # system + user
