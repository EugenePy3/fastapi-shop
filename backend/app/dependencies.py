from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database import SessionLocal, get_db
from app.core.db_manager import DBManager
from app.models.user import User, UserSession

from app.core.tokens import tokens


SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_db_manager() -> DBManager:
    async with DBManager(SessionLocal) as manager:
        yield manager


DBManagerDep = Annotated[DBManager, Depends(get_db_manager)]


async def get_current_user_from_session(
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


async def require_admin(
    user: User = Depends(get_current_user_from_session)
) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return user

