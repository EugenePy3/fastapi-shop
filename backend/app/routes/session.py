from fastapi import APIRouter, Request, Response, status

from app.core.config import settings
from app.dependencies import DBManagerDep, CurrentUserDep
from app.schemas.user import LoginRequest, SessionLoginResponse, UserResponse, MessageResponse
from app.services.auth_service import AuthService
from app.utils.cookies import set_session_cookie, clear_session_cookie

router = APIRouter(prefix="/auth", tags=["Session"])


@router.post(
    "/login",
    response_model=SessionLoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Create Session (Login)",
)
async def login_with_session(
        data: LoginRequest,
        response: Response,
        db: DBManagerDep,
):
    auth_service = AuthService(db)

    user, raw_token = await auth_service.login(
        data.name,
        data.password
    )
    set_session_cookie(
        response,
        raw_token
    )

    return SessionLoginResponse(user=user)


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Session (Logout)",
)
async def logout_session(
        request: Request,
        response: Response,
        db: DBManagerDep,
):
    session_service = AuthService(db)
    raw_token = request.cookies.get(settings.session_cookie_name)
    await session_service.logout(raw_token)
    clear_session_cookie(response)

    return MessageResponse(
        detail='Logged out...'
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current User (Session)"
)
async def me_session(
        user: CurrentUserDep,
):
    return user
