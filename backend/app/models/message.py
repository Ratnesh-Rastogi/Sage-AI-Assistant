"""
Messages table.

SAGE_BLUEPRINT.md Section 69. Stores every user/assistant/system/tool
message in a conversation, plus metadata such as which provider and tools
were used (Section 69 example metadata block).
"""
from sqlalchemy import JSON, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import MESSAGE_ROLES
from app.database.connection import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Message(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "messages"

    conversation_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(Text, nullable=False)  # validated against MESSAGE_ROLES
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    conversation: Mapped["Conversation"] = relationship(  # noqa: F821
        "Conversation", back_populates="messages"
    )

    def __repr__(self) -> str:
        return f"<Message id={self.id} role={self.role}>"


def validate_role(role: str) -> bool:
    """Helper used by the service layer before persisting a message."""
    return role in MESSAGE_ROLES
