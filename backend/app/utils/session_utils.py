from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database import SessionLocal, get_db
from app.core.db_manager import DBManager
from app.models.user import User, UserSession


def _get_session_token_hash(request: Request) -> str:
    raw_token = request.cookies.get(settings.session_cookie_name)
    if not raw_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No session cookie")
    return tokens.hash_session_token(raw_token)


def _absolute_deadline(stored_session: UserSession) -> datetime:
    return stored_session.created_at + timedelta(days=settings.session_absolute_timeout_days)


async def _check_expiry(session: SessionDep, stored_session: UserSession, now: datetime) -> None:
    if stored_session.expires_at <= now:
        _expire_session(session, stored_session, "Session expired")


async def _ensure_not_absolute_expired(
    session: SessionDep, stored_session: UserSession, now: datetime
) -> datetime:
    absolute_expires_at = _absolute_deadline(stored_session)
    if now >= absolute_expires_at:
        _expire_session(session, stored_session, "Session expired")
    return absolute_expires_at