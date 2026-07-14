"""
Tool Registry.

SAGE_BLUEPRINT.md Section 26/51: the Planner never references concrete tool
implementations — it asks the registry "I need web_search capability" and
the registry decides which tool satisfies it. Adding a new tool requires
only: implement it, register it here, write tests (Section 51/62).
"""
from app.tools.base import BaseTool


class ToolRegistry:
    """Central, capability-indexed store of every registered tool."""

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.manifest.name] = tool

    def unregister(self, tool_name: str) -> None:
        self._tools.pop(tool_name, None)

    def get(self, tool_name: str) -> BaseTool | None:
        return self._tools.get(tool_name)

    def find_by_capability(self, capability: str) -> list[BaseTool]:
        """Returns every registered tool that declares the given capability."""
        return [
            tool for tool in self._tools.values() if capability in tool.manifest.capabilities
        ]

    def list_tools(self) -> list[BaseTool]:
        return list(self._tools.values())

    def list_capabilities(self) -> list[str]:
        seen: set[str] = set()
        for tool in self._tools.values():
            seen.update(tool.manifest.capabilities)
        return sorted(seen)


# Process-wide registry instance. Concrete tools register themselves here at
# import time (see tools/system_time/tool.py for the reference example);
# Phase 4/5 tools will do the same.
tool_registry = ToolRegistry()
