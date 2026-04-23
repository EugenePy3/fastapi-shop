from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from slugify import slugify
from typing import List

from ..models import Product
from ..repositories.product_repository import ProductRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.product import ProductResponse, ProductListResponse, ProductCreate
from fastapi import HTTPException, status


class SlugService:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def generate(self, base_slug: str) -> str:
        slug_numbers = []
        existing_slugs = self.product_repository.get_slugs_starting_with(base_slug)
        for slug in existing_slugs:
            if slug == base_slug:
                slug_numbers.append(0)
            else:
                if slug.startswith(base_slug + '-'):
                    parts = slug.rsplit('-', 1)
                    if len(parts) == 2 and parts[1].isdigit():
                        slug_numbers.append(int(parts[1]))

        if not slug_numbers:
            return base_slug

        next_number = max(slug_numbers) + 1
        return f'{base_slug}-{next_number}'


class ProductService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)
        self.slug_service = SlugService(self.product_repository)

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
        source_for_slug = product_data.slug or product_data.name
        base_slug = slugify(source_for_slug, lowercase=True)

        product = None

        for retry_slug in range(3):
            try:
                final_slug = self.slug_service.generate(base_slug)
                product_data.slug = final_slug
                product = self.product_repository.create(product_data)
                break

            except IntegrityError:
                self.product_repository.session.rollback()

                if retry_slug == 2:
                    raise

        return ProductResponse.model_validate(product)

    def remove_product(self, product_id: int) -> Product:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with id {product_id} not found'
            )
        return self.product_repository.remove(product)
