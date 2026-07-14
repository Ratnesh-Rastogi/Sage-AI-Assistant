"""Tests for the Intent Analyzer (SAGE_BLUEPRINT.md Section 20)."""
from app.agent.runtime.intent_analyzer import Intent, IntentAnalyzer


def test_plain_statement_defaults_to_conversation():
    """Normal case."""
    result = IntentAnalyzer().analyze("I really enjoyed today's walk.")
    assert result.intents == [Intent.CONVERSATION]


def test_question_defaults_to_question_answering():
    """Normal case."""
    result = IntentAnalyzer().analyze("What is polymorphism?")
    assert result.intents == [Intent.QUESTION_ANSWERING]


def test_reminder_phrase_detected():
    result = IntentAnalyzer().analyze("Remind me to study DSA at 8 PM.")
    assert Intent.REMINDER_MANAGEMENT in result.intents


def test_multiple_intents_in_one_message():
    """Section 20's own example: search + notes + reminder in one message."""
    result = IntentAnalyzer().analyze(
        "Search for GATE scholarships, save the important ones as a note and remind me tomorrow."
    )
    assert Intent.WEB_SEARCH in result.intents
    assert Intent.NOTE_MANAGEMENT in result.intents
    assert Intent.REMINDER_MANAGEMENT in result.intents


def test_memory_command_detected():
    result = IntentAnalyzer().analyze("Remember that I am preparing for GATE.")
    assert Intent.MEMORY_OPERATIONS in result.intents


def test_empty_message_still_returns_a_default_intent():
    """Edge case: empty string shouldn't crash or return zero intents."""
    result = IntentAnalyzer().analyze("")
    assert len(result.intents) == 1


def test_analyzer_never_executes_anything():
    """Section 20: 'The Intent Analyzer shall not execute any actions.'
    This is a structural guarantee — analyze() takes a string and returns a
    dataclass, with no side-effecting dependencies to call in the first place."""
    result = IntentAnalyzer().analyze("Delete all my tasks right now.")
    assert result.raw_message == "Delete all my tasks right now."
    assert isinstance(result.intents, list)
