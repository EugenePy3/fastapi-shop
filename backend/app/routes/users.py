from fastapi import APIRouter, status

from app.dependencies import DBManagerDep
from app.schemas.user import UserCreate, UserResponse
from ..services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="User registration",
)
async def register(
        data: UserCreate,
        db: DBManagerDep,
):
    service = UserService(db)

    return await service.register(
        data.name,
        data.password,
    )
