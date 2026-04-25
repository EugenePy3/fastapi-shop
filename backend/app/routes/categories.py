from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..dependencies import require_admin
from ..models.user import User
from ..services.category_service import CategoryService, CategoryUpdate
from ..schemas.category import CategoryResponse, CategoryCreate

router = APIRouter(
    prefix='/api/categories',
    tags=['categories']
)


@router.get('', response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_all_categories()


@router.get('/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_category_by_id(category_id)


@router.post('', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, admin: User = Depends(require_admin),
                    db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create_category(category_data)


@router.put('/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(category_id: int, update_data: CategoryUpdate, admin: User = Depends(require_admin),
                    db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.update_category(category_id, update_data)


@router.delete('/{category_id}', status_code=status.HTTP_200_OK)
def remove_category(category_id: int, admin: User = Depends(require_admin),
                    db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.remove_category(category_id)
