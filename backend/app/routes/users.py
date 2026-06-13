from fastapi import APIRouter, status

from app.dependencies import DBManagerDep
from app.schemas.user import UserCreate, UserResponse
from ..services.user_service import UserService


router = APIRouter(prefix="/auth", tags=["Users"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="User registration",
)
async def register(
        data: UserCreate,
        db: DBManagerDep
) -> UserResponse:
    service = UserService(db)

    user = await service.register(
        data.name,
        data.password,
    )

    return user




