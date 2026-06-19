from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.db_manager import DBManager
from app.core.exceptions import (
    InvalidCredentialsError,
)
from app.core.security import security
from app.core.tokens import tokens


class AuthService:
    def __init__(self, db: DBManager):
        """
        Handles authentication logic:
        - user credential verification
        - session token creation
        - session invalidation (logout)
        """
        self.db = db

    async def login(self, name: str, password: str):
        """
        Authenticates user and creates session token.

        Returns:
            tuple: (User, raw_session_token)
        Raises:
            InvalidCredentialsError: if credentials are invalid
        """
        user = await self.db.users.get_user_by_name(name)

        if not user or not security.verify_password(password, user.password_hash):
            raise InvalidCredentialsError('Invalid username or password.')

        raw_token, token_hash = tokens.generate_session_token()

        now = datetime.now(timezone.utc)

        absolute_expires_at = now + timedelta(days=settings.session_absolute_timeout_days)
        expires_at = min(
            absolute_expires_at,
            now + timedelta(minutes=settings.session_extend_minutes),
        )

        await self.db.sessions.create(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        await self.db.flush()
        return user, raw_token

    async def logout(self, raw_token: str | None) -> None:
        """
        Deletes user session if token exists.
        """
        if not raw_token:
            return

        token_hash = tokens.hash_session_token(raw_token)
        stored = await self.db.sessions.get_by_hash(token_hash)

        if stored:
            await self.db.delete(stored)
            await self.db.flush()


