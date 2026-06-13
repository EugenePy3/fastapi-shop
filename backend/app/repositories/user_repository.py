from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_user_by_name(self, name: str) -> User | None:
        return await self.session.scalar(
            select(User).where(User.name == name)
        )

    async def create_user(self, name: str, password_hash: str) -> User:
        user = User(name=name, password_hash=password_hash)
        self.session.add(user)
        return user
