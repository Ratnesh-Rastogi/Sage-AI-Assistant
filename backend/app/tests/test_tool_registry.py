"""Tests for the ToolRegistry itself, independent of any specific tool."""
from app.tools.base import BaseTool, ToolManifest, ToolResult
from app.tools.registry import ToolRegistry


class _FakeToolA(BaseTool):
    manifest = ToolManifest(name="fake_a", description="", capabilities=["shared_cap", "cap_a"])

    async def execute(self, inputs):
        return ToolResult(status="success")


class _FakeToolB(BaseTool):
    manifest = ToolManifest(name="fake_b", description="", capabilities=["shared_cap", "cap_b"])

    async def execute(self, inputs):
        return ToolResult(status="success")


def test_empty_registry_returns_no_tools():
    """Edge case: nothing registered yet."""
    registry = ToolRegistry()
    assert registry.list_tools() == []
    assert registry.find_by_capability("anything") == []
    assert registry.list_capabilities() == []


def test_multiple_tools_can_share_a_capability():
    """Normal case: capability-based discovery can return more than one tool
    (Planner is responsible for picking among them, per Section 26)."""
    registry = ToolRegistry()
    registry.register(_FakeToolA())
    registry.register(_FakeToolB())

    matches = registry.find_by_capability("shared_cap")
    assert {t.manifest.name for t in matches} == {"fake_a", "fake_b"}
    assert len(registry.find_by_capability("cap_a")) == 1


def test_unregister_removes_tool():
    """Normal case: unregistering makes a tool undiscoverable."""
    registry = ToolRegistry()
    registry.register(_FakeToolA())
    assert registry.get("fake_a") is not None

    registry.unregister("fake_a")
    assert registry.get("fake_a") is None
    assert registry.find_by_capability("cap_a") == []


def test_unregister_unknown_tool_is_a_no_op():
    """Edge case: unregistering something never registered shouldn't raise."""
    registry = ToolRegistry()
    registry.unregister("does_not_exist")  # should not raise
