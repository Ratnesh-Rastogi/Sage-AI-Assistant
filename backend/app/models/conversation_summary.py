"""
Conversation summaries table.

SAGE_BLUEPRINT.md Section 70. The schema is created now (frozen structure,
Section 66), but the summarization background job itself is a Phase 4/10
concern (Section 159 "Conversation Summarization"). Older conversations
should not consume context unnecessarily — this table is where that
compression eventually lives.
"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class ConversationSummary(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "conversation_summaries"

    conversation_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    message_range_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    message_range_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<ConversationSummary conversation_id={self.conversation_id}>"
