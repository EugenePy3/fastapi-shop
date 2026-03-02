from fastapi import APIRouter, HTTPException, status

from app.dependencies import DBManagerDep
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import UserService
from app.core.exceptions import AppError, UserAlreadyExistsError


router = APIRouter(prefix="/auth", tags=["Users"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="User registration",
)
def register(data: UserCreate, db: DBManagerDep) -> UserRead:
    service = UserService(db)

    try:
        user = service.register(data.name, data.password)
        return user

    except UserAlreadyExistsError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        ) from err

    except AppError as err:
        detail = str(err) or "Bad request"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        ) from err
