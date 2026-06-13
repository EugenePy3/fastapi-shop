from fastapi import APIRouter, Depends, Request, Response

from app.core.config import settings
from app.dependencies import DBManagerDep, get_current_user_from_session
from app.models.user import User
from app.schemas.user import LoginRequest, SessionLoginResponse, UserResponse
from app.services.auth_service import AuthServiceSession

router = APIRouter(prefix="/auth", tags=["Session"])


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="lax",
        max_age=settings.session_ttl_minutes * 60,
        domain=settings.session_cookie_domain,
        path="/",
    )


def _clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.session_cookie_name,
        domain=settings.session_cookie_domain,
        samesite="lax",
        secure=settings.session_cookie_secure,
        path="/",
    )


@router.post(
    "/login/session",
    summary="Create Session (Login)",
)
async def login_with_session(
        data: LoginRequest,
        response: Response,
        db: DBManagerDep,
) -> SessionLoginResponse:

    session_service = AuthServiceSession(db)
    user, raw_token = session_service.login(data.name, data.password)
    _set_session_cookie(response, raw_token)

    return SessionLoginResponse(user=user)


@router.post("/logout/session", summary="Delete Session (Logout)")
async def logout_session(
        request: Request,
        response: Response,
        db: DBManagerDep,
) -> dict:

    session_service = AuthServiceSession(db)
    raw_token = request.cookies.get(settings.session_cookie_name)
    session_service.logout(raw_token)
    _clear_session_cookie(response)

    return {"detail": "Logged out"}


@router.get("/me/session", summary="Get Current User (Session)")
async def me_session(
        user: User = Depends(get_current_user_from_session)
) -> UserResponse:

    return user
