from datetime import datetime, timedelta

from fastapi import Request

from app.core.config import settings
from app.core.exceptions import MissingSessionCookieError
from app.core.tokens import tokens
from app.models.user import UserSession


def get_session_token_hash(request: Request) -> str:
    """
    Extracts session token from cookies
    and returns its hash.
    """
    raw_token = request.cookies.get(settings.session_cookie_name)

    if not raw_token:
        raise MissingSessionCookieError('Session cookie bot found')
    return tokens.hash_session_token(raw_token)


def absolute_deadline(stored_session: UserSession) -> datetime:
    return stored_session.created_at + timedelta(days=settings.session_absolute_timeout_days)
