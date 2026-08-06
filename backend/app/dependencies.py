from typing import Annotated

from fastapi import Depends, Request
from app.core.exceptions import PermissionDeniedError
from app.database import AsyncSessionLocal
from app.core.db_manager import DBManager
from app.models import user
from app.models.user import User
from app.services.session_service import SessionService
from app.utils.session_utils import get_session_token_hash

"""
Application dependencies.

Provides database access,
authentication and authorization dependencies.
"""


async def get_db_manager() -> DBManager:
    async with DBManager(AsyncSessionLocal) as manager:
        yield manager


DBManagerDep = Annotated[
    DBManager,
    Depends(get_db_manager)
]


async def get_current_user_from_session(
        request: Request,
        db: DBManagerDep,
) -> User:
    token_hash = get_session_token_hash(request)
    service = SessionService(db)

    return await service.validate_session(token_hash)


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user_from_session)
]


async def require_admin(
        user: CurrentUserDep,
) -> User:
    if not user.is_admin:
        raise PermissionDeniedError('Admins only')

    return user


AdminUserDep = Annotated[
    User,
    Depends(require_admin)
]
