from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.db_manager import DBManager
from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,

)
from app.core.security import security
from app.core.tokens import tokens


class UserService:
    def __init__(self, db: DBManager):
        self.db = db

    def register(self, name: str, password: str):
        existing = self.db.users.get_user_by_name(name)
        if existing:
            raise UserAlreadyExistsError('User already exists')

        user = self.db.users.create_user(
            name=name,
            password_hash=security.hash_password(password),
        )

        self.db.session.commit()
        return user


class AuthServiceSession:
    def __init__(self, db: DBManager):
        self.db = db

    def login(self, name: str, password: str):
        user = self.db.users.get_user_by_name(name)
        if not user or not security.verify_password(password, user.password_hash):
            raise InvalidCredentialsError('Invalid username or password')

        raw_token, token_hash = tokens.generate_session_token()
        now = datetime.now(timezone.utc)
        absolute_expires_at = now + timedelta(days=settings.session_absolute_timeout_days)
        expires_at = min(
            absolute_expires_at,
            now + timedelta(minutes=settings.session_extend_minutes),
        )
        self.db.auth.create_session(user_id=user.id, token_hash=token_hash, expires_at=expires_at)
        self.db.session.commit()
        return user, raw_token

    def logout(self, raw_token: str | None) -> None:
        if not raw_token:
            return
        token_hash = tokens.hash_session_token(raw_token)
        stored = self.db.auth.get_session_by_hash(token_hash)
        if stored:
            self.db.auth.delete_session(stored)
            self.db.session.commit()

