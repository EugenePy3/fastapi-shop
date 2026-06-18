from datetime import datetime, timezone

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import UserSession


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, token_hash: str, expires_at: datetime) -> UserSession:
        session_record = UserSession(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.session.add(session_record)

        return session_record

    async def get_by_hash(self, token_hash: str) -> UserSession | None:
        stmt = (
            select(UserSession)
            .where(UserSession.token_hash == token_hash)
        )

        return await self.session.scalar(stmt)

    async def remove_expired(self) -> None:
        """Deletes expired session records."""
        stmt = delete(UserSession).where(
            UserSession.expires_at < datetime.now(timezone.utc)
        )
        await self.session.execute(stmt)
