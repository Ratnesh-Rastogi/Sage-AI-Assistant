"""
Base tool interface and capability manifest.

SAGE_BLUEPRINT.md Section 49.2 (common interface) and Section 50 (capability
manifest). Every concrete tool — from Phase 5's web search tool to whatever
gets added after — implements BaseTool and declares a ToolManifest.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolManifest:
    """Declares what a tool can do, per Section 50's YAML example."""

    name: str
    description: str
    capabilities: list[str]
    input_schema: list[str] = field(default_factory=list)
    output_schema: list[str] = field(default_factory=list)
    requires_confirmation: bool = False


@dataclass
class ToolResult:
    """Structured result every tool execution returns."""

    status: str  # "success" | "failed"
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    recoverable: bool = True


class BaseTool(ABC):
    """Every tool must be independent (Section 49.1) and implement this interface."""

    manifest: ToolManifest

    @abstractmethod
    async def execute(self, inputs: dict[str, Any]) -> ToolResult:
        """Run the tool. Must never raise for expected failures — return a
        ToolResult with status="failed" instead, per Section 52.2's
        structured error contract. Let unexpected exceptions propagate; the
        Execution Manager is responsible for catching those.
        """
        raise NotImplementedError
