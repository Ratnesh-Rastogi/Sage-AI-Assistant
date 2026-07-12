"""
Users table.

SAGE_BLUEPRINT.md Section 67:
Version 1 supports a single user, but the schema keeps user separation
possible for future multi-user support.
"""
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    settings: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    def __repr__(self) -> str:
        return f"<User id={self.id}>"
