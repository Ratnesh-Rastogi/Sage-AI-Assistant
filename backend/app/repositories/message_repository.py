"""Message repository. See conversation_repository.py for the pattern rationale."""
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Message)

    async def list_for_conversation(self, conversation_id: UUID, limit: int = 50):
        """Most recent messages first is easiest to reason about at the call
        site; callers that need chronological order should reverse the list.
        """
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(query)
        return list(reversed(result.scalars().all()))
