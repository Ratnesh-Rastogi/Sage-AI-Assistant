"""
Conversation Manager.

SAGE_BLUEPRINT.md Section 24: maintains conversation IDs, session metadata,
and history. "Conversation history is NOT long-term memory" (Section 9/24) —
it's stored in its own tables (conversations/messages), separate from the
Memory Manager entirely.
"""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, ValidationException
from app.models.conversation import Conversation
from app.models.message import Message, validate_role
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository


class ConversationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.conversations = ConversationRepository(session)
        self.messages = MessageRepository(session)

    async def get_or_create(self, conversation_id: UUID | None, user_id: UUID) -> Conversation:
        if conversation_id is not None:
            conversation = await self.conversations.get_by_id(conversation_id)
            if conversation is None:
                raise NotFoundException(f"Conversation {conversation_id} does not exist.")
            return conversation

        return await self.conversations.add(Conversation(user_id=user_id))

    async def add_message(
        self, conversation_id: UUID, role: str, content: str, metadata: dict | None = None
    ) -> Message:
        if not validate_role(role):
            raise ValidationException(f"Invalid message role: {role!r}")

        return await self.messages.add(
            Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                message_metadata=metadata or {},
            )
        )

    async def get_recent_history(self, conversation_id: UUID, limit: int = 20) -> list[Message]:
        return await self.messages.list_for_conversation(conversation_id, limit=limit)
