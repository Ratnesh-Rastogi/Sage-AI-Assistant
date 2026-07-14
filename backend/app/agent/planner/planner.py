"""
Planner.

SAGE_BLUEPRINT.md Section 21: converts detected intent into an execution
plan. Decides what needs to happen, which tools are required, and execution
order. The Planner never executes tools, never touches PostgreSQL, and never
modifies memory (Section 21 "Planner Constraints") — it only produces a plan
for the Execution Manager to carry out.

Capability names are looked up in the Tool Registry (Section 26) rather than
hardcoded tool names, so registering a new tool in a later phase requires no
Planner changes.
"""
from dataclasses import dataclass, field
from enum import Enum

from app.agent.runtime.intent_analyzer import Intent, IntentAnalysisResult
from app.tools.registry import ToolRegistry


class StepType(str, Enum):
    RESPOND_DIRECTLY = "respond_directly"
    TOOL_CALL = "tool_call"
    CAPABILITY_UNAVAILABLE = "capability_unavailable"


@dataclass
class PlanStep:
    step_type: StepType
    intent: Intent
    capability: str | None = None
    tool_name: str | None = None
    inputs: dict = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    steps: list[PlanStep]
    parallelizable: bool
    """True when every tool step is independent (Section 22 Policy 1)."""


# Maps an intent to the capability a tool would need to declare to satisfy
# it. Intents with no entry are handled by direct conversation (no tool).
_INTENT_CAPABILITY_MAP: dict[Intent, str] = {
    Intent.WEB_SEARCH: "web_search",
    Intent.NOTE_MANAGEMENT: "create_note",
    Intent.TASK_MANAGEMENT: "create_task",
    Intent.REMINDER_MANAGEMENT: "create_reminder",
    Intent.EMAIL_DRAFTING: "draft_email",
    Intent.SCAM_DETECTION: "scam_analysis",
    Intent.FILE_ANALYSIS: "extract_text",
}

# Intents that never need a tool — always answered directly by the provider.
_DIRECT_INTENTS = {
    Intent.CONVERSATION,
    Intent.QUESTION_ANSWERING,
    Intent.PLANNING,
    Intent.MEMORY_OPERATIONS,  # reads happen automatically; writes are Phase 3
}


class Planner:
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    def build_plan(self, analysis: IntentAnalysisResult) -> ExecutionPlan:
        steps: list[PlanStep] = []

        for intent in analysis.intents:
            if intent in _DIRECT_INTENTS:
                steps.append(PlanStep(step_type=StepType.RESPOND_DIRECTLY, intent=intent))
                continue

            capability = _INTENT_CAPABILITY_MAP.get(intent)
            matching_tools = self.tool_registry.find_by_capability(capability) if capability else []

            if matching_tools:
                # Minimize API calls (Section 21): take the first match.
                # Disambiguating among multiple tools for the same
                # capability is future work once more than one exists.
                chosen = matching_tools[0]
                steps.append(
                    PlanStep(
                        step_type=StepType.TOOL_CALL,
                        intent=intent,
                        capability=capability,
                        tool_name=chosen.manifest.name,
                        inputs={"query": analysis.raw_message},
                    )
                )
            else:
                # No tool registered for this capability yet (expected in
                # Phase 2 — Phases 4/5 add these tools). Non-critical: the
                # Execution Manager will report this and continue.
                steps.append(
                    PlanStep(step_type=StepType.CAPABILITY_UNAVAILABLE, intent=intent, capability=capability)
                )

        if not steps:
            steps.append(PlanStep(step_type=StepType.RESPOND_DIRECTLY, intent=Intent.CONVERSATION))

        tool_steps = [s for s in steps if s.step_type == StepType.TOOL_CALL]
        parallelizable = len(tool_steps) == len(steps) or len(tool_steps) <= 1

        return ExecutionPlan(steps=steps, parallelizable=parallelizable)
