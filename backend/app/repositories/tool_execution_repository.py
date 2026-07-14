"""Tool execution repository — the Execution Manager's audit log (Section 22/75)."""
from app.models.tool_execution import ToolExecution
from app.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ToolExecutionRepository(BaseRepository[ToolExecution]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ToolExecution)
