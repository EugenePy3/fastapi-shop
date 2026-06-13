from datetime import datetime, timedelta

from app.core.config import settings
from app.core.db_manager import DBManager
from app.core.exceptions import SessionNotFoundError, SessionExpiredError
from app.models.user import User, UserSession


class SessionService:
    def __init__(self, db: DBManager):
        self.db = db

    # получить сессию
    async def get_session_by_token(self, token_hash: str) -> UserSession:
        session_record = await self.db.sessions.get_by_hash(
            token_hash
        )

        if not session_record:
            raise SessionNotFoundError('Session not found')

        return session_record

    # получить юзера
    async def get_session_user(self, session_record: UserSession) -> User:
        user = await self.db.users.get_user_by_id(
            session_record.user_id
        )

        if not user:
            await self.expire_session(
                session_record,
                "User not found"
            )
        return user

    # удалить сессию
    async def expire_session(self, session_record: UserSession, message: str) -> None:
        await self.db.sessions.remove(
            session_record
        )

        raise SessionExpiredError('Session has expired')

    # продлить
    async def extend_if_needed(
            self,
            session_record: UserSession,
            now: datetime,
            absolute_expires_at: datetime,
    ) -> None:
        if (
                now - session_record.last_refreshed_at
        ) >= timedelta(
            minutes=settings.session_rolling_interval_minutes
        ):
            new_expiry = (
                    now
                    + timedelta(
                        minutes=settings.session_extend_minutes
                    )
            )

            session_record.expires_at = min(
                new_expiry,
                absolute_expires_at,
            )

            session_record.last_refreshed_at = now
