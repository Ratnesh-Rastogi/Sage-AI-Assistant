"""
Execution Manager.

SAGE_BLUEPRINT.md Section 22: the only component allowed to invoke tools.
Executes independent tool steps in parallel (Policy 1), logs every
execution (Policy 5), and — since Phase 2 has no destructive tools yet —
treats all failures as non-critical: they're reported but don't stop the
rest of the plan (Policy 4). `PlanStep.critical` exists so a later phase can
opt specific steps into Policy 3's "terminate execution" behavior.
"""
import asyncio
import time
from dataclasses import dataclass, field
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.planner.planner import ExecutionPlan, PlanStep, StepType
from app.logging.logger import get_logger
from app.repositories.tool_execution_repository import ToolExecutionRepository
from app.tools.base import ToolResult
from app.tools.registry import ToolRegistry

logger = get_logger(__name__)


@dataclass
class StepExecutionResult:
    step: PlanStep
    result: ToolResult | None = None
    error: str | None = None


@dataclass
class ExecutionResult:
    step_results: list[StepExecutionResult] = field(default_factory=list)

    @property
    def tool_outputs(self) -> list[dict]:
        return [
            {"tool": r.step.tool_name, "capability": r.step.capability, "output": r.result.output}
            for r in self.step_results
            if r.result is not None and r.result.status == "success"
        ]

    @property
    def tools_used(self) -> list[str]:
        return [r.step.tool_name for r in self.step_results if r.step.tool_name]

    @property
    def unavailable_capabilities(self) -> list[str]:
        return [
            r.step.capability
            for r in self.step_results
            if r.step.step_type == StepType.CAPABILITY_UNAVAILABLE and r.step.capability
        ]


class ExecutionManager:
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    async def execute(
        self,
        plan: ExecutionPlan,
        session: AsyncSession,
        conversation_id: UUID,
    ) -> ExecutionResult:
        tool_steps = [s for s in plan.steps if s.step_type == StepType.TOOL_CALL]
        other_steps = [s for s in plan.steps if s.step_type != StepType.TOOL_CALL]

        results: list[StepExecutionResult] = []

        for step in other_steps:
            results.append(StepExecutionResult(step=step))
            if step.step_type == StepType.CAPABILITY_UNAVAILABLE:
                logger.info("No tool available for capability '%s'", step.capability)

        if tool_steps:
            if plan.parallelizable and len(tool_steps) > 1:
                tool_results = await asyncio.gather(
                    *[self._run_step(step, session, conversation_id) for step in tool_steps]
                )
            else:
                tool_results = [
                    await self._run_step(step, session, conversation_id) for step in tool_steps
                ]
            results.extend(tool_results)

        return ExecutionResult(step_results=results)

    async def _run_step(
        self, step: PlanStep, session: AsyncSession, conversation_id: UUID
    ) -> StepExecutionResult:
        tool = self.tool_registry.get(step.tool_name) if step.tool_name else None
        if tool is None:
            return StepExecutionResult(
                step=step, error=f"Tool '{step.tool_name}' is not registered."
            )

        started_at = time.perf_counter()
        try:
            result = await tool.execute(step.inputs)
            status = result.status
            error = result.error
        except Exception as exc:  # noqa: BLE001 — a broken tool must not crash the runtime
            logger.exception("Tool '%s' raised an unexpected exception", step.tool_name)
            result = ToolResult(status="failed", error=str(exc), recoverable=False)
            status = "failed"
            error = str(exc)

        execution_time_ms = int((time.perf_counter() - started_at) * 1000)

        await self._log_execution(
            session=session,
            conversation_id=conversation_id,
            step=step,
            status=status,
            output=result.output,
            execution_time_ms=execution_time_ms,
        )

        return StepExecutionResult(step=step, result=result, error=error)

    async def _log_execution(
        self,
        session: AsyncSession,
        conversation_id: UUID,
        step: PlanStep,
        status: str,
        output: dict,
        execution_time_ms: int,
    ) -> None:
        from app.models.tool_execution import ToolExecution

        repo = ToolExecutionRepository(session)
        await repo.add(
            ToolExecution(
                conversation_id=conversation_id,
                tool_name=step.tool_name or "unknown",
                capability=step.capability or "unknown",
                input=step.inputs,
                output=output,
                status=status,
                execution_time_ms=execution_time_ms,
            )
        )
