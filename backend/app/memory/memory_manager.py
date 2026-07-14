"""
Memory Manager — Phase 2 stub.

SAGE_BLUEPRINT.md Section 25: the Memory Manager owns every memory
operation; no other module may directly update memory. Full persistence,
classification, and importance scoring (Sections 37-40) are Phase 3 work.

This stub exists now because the Context Builder's priority list (Section
23) includes "Relevant Memory," and it should depend on this interface from
day one rather than being retrofitted later. `retrieve_relevant` always
returns an empty list until Phase 3 wires it to real storage — it never
fabricates memories.
"""
from app.logging.logger import get_logger

logger = get_logger(__name__)


class MemoryManager:
    """Minimal interface. Write operations intentionally raise until Phase 3
    implements them — silently no-op-ing a "remember this" request would be
    a correctness bug (Section 33.2: the user must always be able to trust
    that a memory command took effect).
    """

    async def retrieve_relevant(self, query: str, limit: int = 5) -> list[str]:
        logger.debug("Memory retrieval requested (Phase 3 not yet implemented): %r", query)
        return []

    async def create(self, *args, **kwargs):
        raise NotImplementedError("Memory creation is implemented in Phase 3.")

    async def update(self, *args, **kwargs):
        raise NotImplementedError("Memory updates are implemented in Phase 3.")

    async def delete(self, *args, **kwargs):
        raise NotImplementedError("Memory deletion is implemented in Phase 3.")


memory_manager = MemoryManager()
