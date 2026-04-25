from sqlalchemy.orm import Session
from slugify import slugify
from typing import List

from ..models import Product
from ..repositories.product_repository import ProductRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.product import ProductResponse, ProductListResponse, ProductCreate, ProductUpdate
from fastapi import HTTPException, status


class ProductService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_all_products(self) -> ProductListResponse:
        products = self.product_repository.get_all()
        products_response = [ProductResponse.model_validate(prod) for prod in products]
        return ProductListResponse(products=products_response, total=len(products_response))

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with id {product_id} not found'
            )
        return ProductResponse.model_validate(product)

    def get_products_by_category(self, category_id: int) -> ProductListResponse:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Category with id {category_id} not found'
            )

        products = self.product_repository.get_by_category(category_id)
        products_response = [ProductResponse.model_validate(prod) for prod in products]
        return ProductListResponse(products=products_response, total=len(products_response))

    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Category with id {product_data.category_id} not found'
            )

        product = self.product_repository.create(product_data)

        base_slug = slugify(product.name, lowercase=True)
        product.slug = f'{base_slug}-{product.id}'
        product = self.product_repository.update(product)

        return ProductResponse.model_validate(product)

    def update_product(self, product_id: int, update_data: ProductUpdate) -> ProductResponse:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with id {product_id} not found'
            )
        if update_data.category_id is not None:
            category = self.category_repository.get_by_id(update_data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Category with id {update_data.category_id} not found')

        updates = update_data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(product, field, value)
        if 'name' in updates:
            base_slug = slugify(product.name, lowercase=True)
            product.slug = f'{base_slug}-{product.id}'

        product = self.product_repository.update(product)
        return ProductResponse.model_validate(product)

    def remove_product(self, product_id: int) -> Product:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with id {product_id} not found'
            )
        return self.product_repository.remove(product)
