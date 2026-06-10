from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..dependencies import require_admin, DBManagerDep
from ..models.user import User
from ..services.product_service import ProductService
from ..schemas.product import ProductResponse, ProductListResponse, ProductCreate, ProductUpdate

router = APIRouter(
    prefix='/api/products',
    tags=['products']
)


@router.get('', response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def get_products(db: DBManagerDep):
    service = ProductService(db)

    products = await service.get_all_products()

    return ProductListResponse(
        products=products,
        total=len(products)
    )


@router.get('/{product_id}', response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: DBManagerDep):
    service = ProductService(db)

    return await service.get_product_by_id(product_id)


@router.get('/category/{category_id}', response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def get_products_by_category(category_id: int, db: DBManagerDep):
    service = ProductService(db)

    products = await service.get_products_by_category(
        category_id
    )

    return ProductListResponse(
        products=products,
        total=len(products)
    )


@router.post('', response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
        product_data: ProductCreate,
        db: DBManagerDep,
        admin: User = Depends(require_admin)
):
    service = ProductService(db)

    return await service.create_product(product_data)


@router.patch('/{product_id}', response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(
        product_id: int,
        update_data: ProductUpdate,
        db: DBManagerDep,
        admin: User = Depends(require_admin)
):
    service = ProductService(db)

    return await service.update_product(product_id, update_data)


@router.delete('/{product_id}', response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def remove_product(
        product_id: int,
        db: DBManagerDep,
        admin: User = Depends(require_admin)
):
    service = ProductService(db)

    return await service.remove_product(product_id)
