"""
Tests for the system_time reference tool.

Covers Tool Testing Requirements (SAGE_BLUEPRINT.md Section 61): valid input,
invalid input, and registry integration.
"""
import pytest

from app.tools.registry import ToolRegistry
from app.tools.system_time.tool import SystemTimeTool


@pytest.mark.asyncio
async def test_execute_returns_success_with_valid_input():
    """Normal case."""
    tool = SystemTimeTool()
    result = await tool.execute({"timezone": "UTC"})
    assert result.status == "success"
    assert "iso_timestamp" in result.output
    assert result.output["timezone"] == "UTC"


@pytest.mark.asyncio
async def test_execute_defaults_timezone_when_omitted():
    """Edge case: missing optional input falls back to the schema default."""
    tool = SystemTimeTool()
    result = await tool.execute({})
    assert result.status == "success"
    assert result.output["timezone"] == "UTC"


@pytest.mark.asyncio
async def test_execute_handles_invalid_input_type_gracefully():
    """Invalid case: wrong input type returns a structured failure, not a raised exception."""
    tool = SystemTimeTool()
    result = await tool.execute({"timezone": {"not": "a string"}})
    assert result.status == "failed"
    assert result.error is not None
    assert result.recoverable is False


def test_tool_registers_and_is_discoverable_by_capability():
    """Integration case: Tool Registry integration (Section 61)."""
    registry = ToolRegistry()
    registry.register(SystemTimeTool())

    found = registry.find_by_capability("get_current_time")
    assert len(found) == 1
    assert found[0].manifest.name == "system_time"

    assert registry.get("system_time") is not None
    assert registry.get("does_not_exist") is None
    assert "get_current_time" in registry.list_capabilities()
