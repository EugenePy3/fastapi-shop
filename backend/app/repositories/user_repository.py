from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.user import User, UserSession


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_name(self, name: str) -> User | None:
        return self.session.scalar(
            select(User).where(User.name == name)
        )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def create_user(self, name: str, password_hash: str) -> User:
        user = User(name=name, password_hash=password_hash)
        self.session.add(user)
        self.session.flush()
        return user


class AuthRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_session(self, user_id: int, token_hash: str, expires_at: datetime) -> UserSession:
        record = UserSession(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
        self.session.add(record)
        self.session.flush()
        return record

    def get_session_by_hash(self, token_hash: str) -> Optional[UserSession]:
        return self.session.scalar(select(UserSession).where(UserSession.token_hash == token_hash))

    def delete_session(self, session_obj: UserSession) -> None:
        self.session.delete(session_obj)



