from sqlalchemy.orm import Session
from typing import List

from ..core.exceptions import CategoryNotFoundError, CategoryDeleteError, CategoryAlreadyExistsError
from ..models import Category
from ..repositories.category_repository import CategoryRepository
from ..schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from fastapi import HTTPException, status


class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_all_categories(self) -> List[CategoryResponse]:
        categories = self.repository.get_all()
        return [CategoryResponse.model_validate(cat) for cat in categories]

    def get_category_by_id(self, category_id: int) -> CategoryResponse:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f'Category with id {category_id} not found')

        return CategoryResponse.model_validate(category)

    def get_category_by_slug(self, category_slug: str) -> CategoryResponse:
        category = self.repository.get_by_slug(category_slug)
        if not category:
            raise CategoryNotFoundError(f'Category with slug {category_slug} not found')

        return CategoryResponse.model_validate(category)

    def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        existing_category = self.repository.get_by_slug(category_data.slug)
        if existing_category:
            raise CategoryAlreadyExistsError(f'Category with slug {category_data.slug} already exists')
        category = self.repository.create(category_data)
        return CategoryResponse.model_validate(category)

    def update_category(self, category_id: int, update_data: CategoryUpdate) -> CategoryResponse:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f'Category with id {category_id} not found')

        existing_category = self.repository.get_by_slug(update_data.slug)
        if existing_category and existing_category.id != category_id:
            raise CategoryAlreadyExistsError(f'Category with slug {update_data.slug} already exists')

        category.name = update_data.name
        category.slug = update_data.slug
        category = self.repository.update(category)

        return CategoryResponse.model_validate(category)

    def remove_category(self, category_id: int) -> Category:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f'Category with id {category_id} not found')
        product_count = self.repository.count_products_by_category(category_id)
        if product_count > 0:
            raise CategoryDeleteError(f'Cannot delete category: {product_count} products are still assigned to it')

        return self.repository.remove(category)


