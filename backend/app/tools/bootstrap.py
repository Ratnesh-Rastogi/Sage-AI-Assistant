"""
Tool bootstrap.

Explicitly imports and registers every known tool. Kept as one greppable
list (rather than auto-discovering packages) so it's obvious what's active
and tests can call this deterministically. Adding a tool later means adding
one line here — no other module changes required (Section 26).
"""
from app.tools.system_time.tool import register as register_system_time


def bootstrap_tools() -> None:
    register_system_time()
    # Phase 4/5 tools (notes, tasks, reminders, web search, scam detection,
    # file processing, email drafting) register themselves here as they're built.
