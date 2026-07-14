"""
Conversation repository.

Extends BaseRepository (app/repositories/base_repository.py, built in Phase 1)
per SAGE_BLUEPRINT.md Section 99 — only repositories may touch PostgreSQL.
"""
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.repositories.base_repository import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Conversation)

    async def list_for_user(self, user_id: UUID, include_archived: bool = False):
        query = select(Conversation).where(Conversation.user_id == user_id)
        if not include_archived:
            query = query.where(Conversation.archived.is_(False))
        query = query.order_by(Conversation.updated_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()
