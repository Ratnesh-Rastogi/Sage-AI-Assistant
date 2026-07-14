"""
Intent Analyzer.

SAGE_BLUEPRINT.md Section 20: classifies what the user is trying to
accomplish. Multiple intents may exist within the same message. The Intent
Analyzer never executes anything — classification only.

Phase 2 implements this with transparent keyword heuristics rather than an
LLM call, so intent detection doesn't itself depend on a configured provider
being reachable. The interface is stable, so a future phase can swap in an
LLM-based classifier without touching the Planner.
"""
from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    CONVERSATION = "conversation"
    QUESTION_ANSWERING = "question_answering"
    PLANNING = "planning"
    WEB_SEARCH = "web_search"
    NOTE_MANAGEMENT = "note_management"
    TASK_MANAGEMENT = "task_management"
    REMINDER_MANAGEMENT = "reminder_management"
    MEMORY_OPERATIONS = "memory_operations"
    EMAIL_DRAFTING = "email_drafting"
    SCAM_DETECTION = "scam_detection"
    FILE_ANALYSIS = "file_analysis"


@dataclass
class IntentAnalysisResult:
    intents: list[Intent]
    raw_message: str


# Ordered so more specific phrases are checked before generic ones.
_KEYWORD_RULES: list[tuple[Intent, tuple[str, ...]]] = [
    (Intent.MEMORY_OPERATIONS, ("remember that", "forget that", "what do you know about me", "what memories")),
    (Intent.REMINDER_MANAGEMENT, ("remind me", "reminder", "set a reminder")),
    (Intent.TASK_MANAGEMENT, ("create a task", "add a task", "my tasks", "mark as complete", "to-do", "todo")),
    (Intent.NOTE_MANAGEMENT, ("save this note", "take a note", "my notes", "find my note", "as a note", "as notes")),
    (Intent.EMAIL_DRAFTING, ("write an email", "draft an email", "email to", "follow-up email")),
    (Intent.SCAM_DETECTION, ("is this a scam", "is this legit", "is this website real", "suspicious email")),
    (Intent.FILE_ANALYSIS, ("analyze this file", "summarize this document", "this pdf", "this csv")),
    (Intent.WEB_SEARCH, ("search for", "look up", "what's the latest", "current price of", "who is the current")),
    (Intent.PLANNING, ("help me plan", "step by step", "create a plan for")),
]


class IntentAnalyzer:
    """Rule-based intent classification (Section 20)."""

    def analyze(self, message: str) -> IntentAnalysisResult:
        lowered = message.lower()
        detected: list[Intent] = []

        for intent, keywords in _KEYWORD_RULES:
            if any(keyword in lowered for keyword in keywords):
                detected.append(intent)

        if not detected:
            detected.append(
                Intent.QUESTION_ANSWERING if lowered.strip().endswith("?") else Intent.CONVERSATION
            )

        return IntentAnalysisResult(intents=detected, raw_message=message)
