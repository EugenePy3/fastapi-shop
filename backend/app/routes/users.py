from fastapi import APIRouter, status

from app.dependencies import DBManagerDep
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import UserService


router = APIRouter(prefix="/auth", tags=["Users"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="User registration",
)
def register(data: UserCreate, db: DBManagerDep) -> UserRead:
    service = UserService(db)
    user = service.register(data.name, data.password)
    return user




