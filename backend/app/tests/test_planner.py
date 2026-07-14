"""Tests for the Planner (SAGE_BLUEPRINT.md Section 21)."""
from app.agent.runtime.intent_analyzer import Intent, IntentAnalysisResult
from app.agent.planner.planner import Planner, StepType
from app.tools.base import BaseTool, ToolManifest, ToolResult
from app.tools.registry import ToolRegistry


class _FakeSearchTool(BaseTool):
    manifest = ToolManifest(name="fake_search", description="", capabilities=["web_search"])

    async def execute(self, inputs):
        return ToolResult(status="success")


def test_conversation_intent_plans_direct_response():
    """Normal case: no tool needed for plain conversation."""
    planner = Planner(ToolRegistry())
    analysis = IntentAnalysisResult(intents=[Intent.CONVERSATION], raw_message="hello")

    plan = planner.build_plan(analysis)

    assert len(plan.steps) == 1
    assert plan.steps[0].step_type == StepType.RESPOND_DIRECTLY


def test_capability_with_no_registered_tool_is_marked_unavailable():
    """Normal case: Phase 2 has no web_search tool registered yet."""
    planner = Planner(ToolRegistry())
    analysis = IntentAnalysisResult(intents=[Intent.WEB_SEARCH], raw_message="search for X")

    plan = planner.build_plan(analysis)

    assert plan.steps[0].step_type == StepType.CAPABILITY_UNAVAILABLE
    assert plan.steps[0].capability == "web_search"


def test_capability_with_registered_tool_produces_tool_call_step():
    """Normal case: extensibility — registering a tool changes the plan
    with zero Planner code changes (Section 26)."""
    registry = ToolRegistry()
    registry.register(_FakeSearchTool())
    planner = Planner(registry)
    analysis = IntentAnalysisResult(intents=[Intent.WEB_SEARCH], raw_message="search for X")

    plan = planner.build_plan(analysis)

    assert plan.steps[0].step_type == StepType.TOOL_CALL
    assert plan.steps[0].tool_name == "fake_search"


def test_multiple_intents_produce_multiple_steps():
    """Section 20's example: search + notes + reminder -> a 3-step plan."""
    planner = Planner(ToolRegistry())
    analysis = IntentAnalysisResult(
        intents=[Intent.WEB_SEARCH, Intent.NOTE_MANAGEMENT, Intent.REMINDER_MANAGEMENT],
        raw_message="search, note, remind",
    )

    plan = planner.build_plan(analysis)

    assert len(plan.steps) == 3


def test_planner_never_executes_tools():
    """Section 21 constraint: Planner must never execute tools — structurally
    guaranteed since build_plan() only returns data, never awaits anything."""
    import inspect

    assert not inspect.iscoroutinefunction(Planner.build_plan)


def test_plan_with_only_tool_steps_is_marked_parallelizable():
    registry = ToolRegistry()
    registry.register(_FakeSearchTool())
    planner = Planner(registry)
    analysis = IntentAnalysisResult(intents=[Intent.WEB_SEARCH], raw_message="x")

    plan = planner.build_plan(analysis)

    assert plan.parallelizable is True
