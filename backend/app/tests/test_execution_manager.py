"""
Tests for the Execution Manager (SAGE_BLUEPRINT.md Section 22).

Uses a minimal fake AsyncSession — BaseRepository.add() only calls
session.add() (sync, ORM-bookkeeping only) and session.flush() (async), so a
fake with no-op versions of both is enough to test execution logic without a
real database.
"""
import uuid

import pytest

from app.agent.planner.planner import ExecutionPlan, PlanStep, StepType
from app.agent.runtime.intent_analyzer import Intent
from app.agent.execution.tool_executor import ExecutionManager
from app.tools.base import BaseTool, ToolManifest, ToolResult
from app.tools.registry import ToolRegistry


class _FakeSession:
    def __init__(self):
        self.added = []

    def add(self, instance):
        self.added.append(instance)

    async def flush(self):
        pass


class _SucceedingTool(BaseTool):
    manifest = ToolManifest(name="succeeding_tool", description="", capabilities=["demo_success"])

    async def execute(self, inputs):
        return ToolResult(status="success", output={"ok": True})


class _FailingTool(BaseTool):
    manifest = ToolManifest(name="failing_tool", description="", capabilities=["demo_fail"])

    async def execute(self, inputs):
        return ToolResult(status="failed", error="deliberate failure", recoverable=True)


class _CrashingTool(BaseTool):
    manifest = ToolManifest(name="crashing_tool", description="", capabilities=["demo_crash"])

    async def execute(self, inputs):
        raise RuntimeError("boom")


def _registry_with(*tools) -> ToolRegistry:
    registry = ToolRegistry()
    for tool in tools:
        registry.register(tool)
    return registry


@pytest.mark.asyncio
async def test_direct_response_step_produces_no_tool_execution():
    """Normal case: non-tool steps pass through untouched."""
    manager = ExecutionManager(ToolRegistry())
    plan = ExecutionPlan(
        steps=[PlanStep(step_type=StepType.RESPOND_DIRECTLY, intent=Intent.CONVERSATION)],
        parallelizable=True,
    )
    result = await manager.execute(plan, _FakeSession(), uuid.uuid4())
    assert result.tool_outputs == []
    assert result.tools_used == []


@pytest.mark.asyncio
async def test_successful_tool_call_is_logged_and_returns_output():
    """Normal case + Section 22 Policy 5: every execution generates a log entry."""
    registry = _registry_with(_SucceedingTool())
    manager = ExecutionManager(registry)
    plan = ExecutionPlan(
        steps=[
            PlanStep(
                step_type=StepType.TOOL_CALL,
                intent=Intent.WEB_SEARCH,
                capability="demo_success",
                tool_name="succeeding_tool",
            )
        ],
        parallelizable=True,
    )
    session = _FakeSession()
    result = await manager.execute(plan, session, uuid.uuid4())

    assert result.tool_outputs[0]["output"] == {"ok": True}
    assert result.tools_used == ["succeeding_tool"]
    assert len(session.added) == 1  # one ToolExecution log row


@pytest.mark.asyncio
async def test_failing_tool_is_non_critical_and_still_logged():
    """Section 22 Policy 4: non-critical failures are reported, not fatal."""
    registry = _registry_with(_FailingTool())
    manager = ExecutionManager(registry)
    plan = ExecutionPlan(
        steps=[
            PlanStep(
                step_type=StepType.TOOL_CALL,
                intent=Intent.WEB_SEARCH,
                capability="demo_fail",
                tool_name="failing_tool",
            )
        ],
        parallelizable=True,
    )
    session = _FakeSession()
    result = await manager.execute(plan, session, uuid.uuid4())

    assert result.tool_outputs == []  # failed tool contributes no output
    assert result.step_results[0].error == "deliberate failure"
    assert len(session.added) == 1


@pytest.mark.asyncio
async def test_crashing_tool_does_not_crash_the_execution_manager():
    """A broken tool must not take down the whole runtime (Section 4 'Error Recovery')."""
    registry = _registry_with(_CrashingTool())
    manager = ExecutionManager(registry)
    plan = ExecutionPlan(
        steps=[
            PlanStep(
                step_type=StepType.TOOL_CALL,
                intent=Intent.WEB_SEARCH,
                capability="demo_crash",
                tool_name="crashing_tool",
            )
        ],
        parallelizable=True,
    )
    result = await manager.execute(plan, _FakeSession(), uuid.uuid4())
    assert result.step_results[0].error == "boom"


@pytest.mark.asyncio
async def test_capability_unavailable_step_is_reported_without_execution():
    manager = ExecutionManager(ToolRegistry())
    plan = ExecutionPlan(
        steps=[
            PlanStep(step_type=StepType.CAPABILITY_UNAVAILABLE, intent=Intent.WEB_SEARCH, capability="web_search")
        ],
        parallelizable=True,
    )
    result = await manager.execute(plan, _FakeSession(), uuid.uuid4())
    assert result.unavailable_capabilities == ["web_search"]


@pytest.mark.asyncio
async def test_multiple_independent_tool_steps_all_execute():
    """Section 22 Policy 1: independent tools should execute in parallel —
    functionally verified by checking both results come back correctly,
    since asyncio.gather's true concurrency isn't observable in a unit test."""
    registry = _registry_with(_SucceedingTool(), _FailingTool())
    manager = ExecutionManager(registry)
    plan = ExecutionPlan(
        steps=[
            PlanStep(step_type=StepType.TOOL_CALL, intent=Intent.WEB_SEARCH, capability="demo_success", tool_name="succeeding_tool"),
            PlanStep(step_type=StepType.TOOL_CALL, intent=Intent.FILE_ANALYSIS, capability="demo_fail", tool_name="failing_tool"),
        ],
        parallelizable=True,
    )
    result = await manager.execute(plan, _FakeSession(), uuid.uuid4())
    assert len(result.step_results) == 2
