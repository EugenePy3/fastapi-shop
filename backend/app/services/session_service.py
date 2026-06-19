from datetime import datetime, timezone, timedelta

from app.core.config import settings
from app.core.db_manager import DBManager
from app.core.exceptions import SessionNotFoundError, SessionExpiredError
from app.models.user import User, UserSession
from app.utils.session_utils import absolute_deadline


class SessionService:
    """
    Handles session lifecycle management.

    Responsible for session validation,
    expiration checks, rolling session extension
    and resolving authenticated users.
    """
    def __init__(self, db: DBManager):
        self.db = db

    async def validate_session(
            self,
            token_hash: str,
    ) -> User:
        """
        Validates user session and returns
        the authenticated user.
        """

        now = datetime.now(timezone.utc)

        session_record = await self.get_session_by_hash(token_hash)
        absolute_expires_at = await self.ensure_not_absolute_expired(session_record, now)
        await self.check_expiry(session_record, now)
        await self.extend_if_needed(session_record, now, absolute_expires_at)

        return await self.get_session_user(session_record)

    async def get_session_by_hash(self, token_hash: str) -> UserSession:
        session_record = await self.db.sessions.get_by_hash(
            token_hash
        )

        if not session_record:
            raise SessionNotFoundError('Session not found.')

        return session_record

    async def get_session_user(self, session_record: UserSession) -> User:
        user = await self.db.users.get_user_by_id(
            session_record.user_id
        )

        if not user:
            await self.expire_session(
                session_record,
                "User not found."
            )
        return user

    # Проверяем абсолютный дедлайн (нельзя продлевать бесконечно)
    async def ensure_not_absolute_expired(
            self, session_record: UserSession,
            now: datetime,
    ) -> datetime:

        absolute_expires_at = absolute_deadline(session_record)

        if now >= absolute_expires_at:
            await self.expire_session(session_record, "Session expired.")
        return absolute_expires_at

    #  Проверяем обычное истечение срока действия (expires_at)
    async def check_expiry(
            self, session_record: UserSession,
            now: datetime
    ) -> None:

        if session_record.expires_at <= now:
            await self.expire_session(session_record, "Session expired.")

    async def extend_if_needed(
            self,
            session_record: UserSession,
            now: datetime,
            absolute_expires_at: datetime,
    ) -> None:
        """
        Extends session expiration using rolling
        expiration strategy without exceeding
        the absolute lifetime limit.
        """
        if (
                now - session_record.last_refreshed_at
        ) >= timedelta(
            minutes=settings.session_rolling_interval_minutes
        ):
            new_expiry = now + timedelta(minutes=settings.session_extend_minutes)

            # Не даем уйти за рамки абсолютного дедлайна
            session_record.expires_at = min(
                new_expiry,
                absolute_expires_at,
            )

            session_record.last_refreshed_at = now

    async def expire_session(self, session_record: UserSession, message: str) -> None:
        await self.db.delete(session_record)
        await self.db.flush()

        raise SessionExpiredError(message)
