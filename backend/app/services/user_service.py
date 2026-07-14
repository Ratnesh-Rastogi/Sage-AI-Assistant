"""
User service.

SAGE_BLUEPRINT.md Section 67: "Version 1 supports one user." There's no
authentication system (explicitly excluded, Section 3), so this resolves —
creating on first use — the single local user that conversations belong to.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_default_user(self) -> User:
        result = await self.session.execute(select(User).limit(1))
        user = result.scalar_one_or_none()
        if user is not None:
            return user

        user = User()
        self.session.add(user)
        await self.session.flush()
        return user
