"""
Tool executions table.

SAGE_BLUEPRINT.md Section 75. Records every tool invocation the Execution
Manager makes — required by Section 22 ("every tool execution must generate
an execution log") and the Runtime Acceptance Criteria (Section 31: "every
tool execution is logged").
"""
from sqlalchemy import JSON, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import TOOL_EXECUTION_STATUSES
from app.database.connection import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class ToolExecution(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tool_executions"

    conversation_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True
    )
    tool_name: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    capability: Mapped[str] = mapped_column(Text, nullable=False)
    input: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    output: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)  # validated against TOOL_EXECUTION_STATUSES
    execution_time_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<ToolExecution tool={self.tool_name} status={self.status}>"


def validate_status(status: str) -> bool:
    return status in TOOL_EXECUTION_STATUSES
