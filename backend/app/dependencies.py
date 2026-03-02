from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import SessionLocal, get_db
from app.core.db_manager import DBManager
from app.models.user import User, UserSession

from app.core.tokens import tokens


SessionDep = Annotated[Session, Depends(get_db)]


def get_db_manager() -> DBManager:
    with DBManager(SessionLocal) as manager:
        yield manager


DBManagerDep = Annotated[DBManager, Depends(get_db_manager)]


def get_current_user_from_session(
    request: Request, session: SessionDep
) -> User:
    token_hash = _get_session_token_hash(request)
    stored_session = _find_session(session, token_hash)
    now = datetime.utcnow()
    absolute_expires_at = _ensure_not_absolute_expired(session, stored_session, now)
    _extend_if_needed(session, stored_session, now, absolute_expires_at)
    _check_expiry(session, stored_session, now)
    user = _get_session_user(session, stored_session)
    return user


def require_admin(
    user: User = Depends(get_current_user_from_session)
) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return user


def _get_session_token_hash(request: Request) -> str:
    raw_token = request.cookies.get(settings.session_cookie_name)
    if not raw_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No session cookie")
    return tokens.hash_session_token(raw_token)


def _find_session(session: SessionDep, token_hash: str) -> UserSession:
    stmt = select(UserSession).where(UserSession.token_hash == token_hash)
    stored_session = session.scalar(stmt)
    if not stored_session:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session not found")
    return stored_session


def _absolute_deadline(stored_session: UserSession) -> datetime:
    return stored_session.created_at + timedelta(days=settings.session_absolute_timeout_days)


def _ensure_not_absolute_expired(
    session: SessionDep, stored_session: UserSession, now: datetime
) -> datetime:
    absolute_expires_at = _absolute_deadline(stored_session)
    if now >= absolute_expires_at:
        _expire_session(session, stored_session, "Session expired")
    return absolute_expires_at


def _extend_if_needed(
    session: SessionDep, stored_session: UserSession, now: datetime, absolute_expires_at: datetime
) -> None:
    if (now - stored_session.last_refreshed_at) >= timedelta(minutes=settings.session_rolling_interval_minutes):
        new_expiry = now + timedelta(minutes=settings.session_extend_minutes)
        stored_session.expires_at = min(new_expiry, absolute_expires_at)
        stored_session.last_refreshed_at = now
        session.commit()


def _check_expiry(session: SessionDep, stored_session: UserSession, now: datetime) -> None:
    if stored_session.expires_at <= now:
        _expire_session(session, stored_session, "Session expired")


def _get_session_user(session: SessionDep, stored_session: UserSession) -> User:
    user = session.get(User, stored_session.user_id)
    if not user:
        _expire_session(session, stored_session, "User not found")
    return user


def _expire_session(session: SessionDep, stored_session: UserSession, message: str) -> None:
    session.delete(stored_session)
    session.commit()
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, message)


