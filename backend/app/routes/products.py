from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..dependencies import require_admin
from ..models.user import User
from ..services.product_service import ProductService
from ..schemas.product import ProductResponse, ProductListResponse, ProductCreate

router = APIRouter(
    prefix='/api/products',
    tags=['products']
)


@router.get('', response_model=ProductListResponse, status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all_products()


@router.get('/{product_id}', response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product_by_id(product_id)


@router.get('/category/{category_id}', response_model=ProductListResponse, status_code=status.HTTP_200_OK)
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_products_by_category(category_id)


@router.post('', response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, admin: User = Depends(require_admin),
                   db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.create_product(product_data)


@router.delete('/{product_id}', response_model=ProductResponse, status_code=status.HTTP_200_OK)
def remove_product(product_id: int, admin: User = Depends(require_admin),
                   db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.remove_product(product_id)


