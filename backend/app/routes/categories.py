from fastapi import APIRouter, Depends, status
from typing import List
from ..dependencies import require_admin, DBManagerDep
from ..models.user import User
from ..services.category_service import CategoryService, CategoryUpdate
from ..schemas.category import CategoryResponse, CategoryCreate

router = APIRouter(
    prefix='/api/categories',
    tags=['categories']
)


@router.get('', response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_categories(db: DBManagerDep):
    service = CategoryService(db)
    return await service.get_all_categories()


@router.get('/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_category(
        category_id: int,
        db: DBManagerDep
):
    service = CategoryService(db)
    return await service.get_category_by_id(category_id)


@router.post('', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
        data: CategoryCreate,
        db: DBManagerDep,
        admin: User = Depends(require_admin)
):
    service = CategoryService(db)
    return await service.create_category(data)


@router.patch('/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update_category(
        category_id: int,
        data: CategoryUpdate,
        db: DBManagerDep,
        admin: User = Depends(require_admin)
):
    service = CategoryService(db)
    return await service.update_category(category_id, data)


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_category(
        category_id: int,
        db: DBManagerDep,
        admin: User = Depends(require_admin)
):
    service = CategoryService(db)
    await service.remove_category(category_id)


