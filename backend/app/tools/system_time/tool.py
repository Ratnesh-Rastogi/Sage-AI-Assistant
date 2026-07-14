"""
system_time — a minimal reference tool.

This exists purely to prove the Tool Registry + Execution Manager pipeline
works end-to-end (Section 26/51/62), following the exact steps Section 26
describes for adding a tool: implement, register, test. It is intentionally
trivial — the real Phase 5 "Advanced Intelligence Tools" (web search, scam
detection, file processing, email drafting) are separate, later work.
"""
from typing import Any

from app.tools.base import BaseTool, ToolManifest, ToolResult
from app.tools.registry import tool_registry
from app.tools.system_time.schemas import SystemTimeInput
from app.tools.system_time.service import get_current_time


class SystemTimeTool(BaseTool):
    manifest = ToolManifest(
        name="system_time",
        description="Returns the current system time in UTC.",
        capabilities=["get_current_time"],
        input_schema=["timezone"],
        output_schema=["iso_timestamp", "timezone"],
        requires_confirmation=False,
    )

    async def execute(self, inputs: dict[str, Any]) -> ToolResult:
        try:
            parsed = SystemTimeInput(**inputs)
        except Exception as exc:  # noqa: BLE001 — surfaced as a structured tool failure
            return ToolResult(status="failed", error=str(exc), recoverable=False)

        result = get_current_time(parsed.timezone)
        return ToolResult(status="success", output=result.model_dump())


def register() -> None:
    tool_registry.register(SystemTimeTool())
