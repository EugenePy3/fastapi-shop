from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, delete, func
from ..models.category import Category
from ..models.product import Product
from ..schemas.category import CategoryCreate


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Category]:
        stmt = select(Category)
        return list(self.session.scalars(stmt))

    def get_by_id(self, category_id: int) -> Category | None:
        stmt = (
            select(Category)
            .where(Category.id == category_id)
        )
        return self.session.scalar(stmt)

    def get_by_slug(self, slug: str) -> Category | None:
        stmt = (
            select(Category)
            .where(Category.slug == slug)
        )
        return self.session.scalar(stmt)

    def create(self, category_data: CategoryCreate) -> Category:
        category = Category(**category_data.model_dump())
        self.session.add(category)
        self.session.flush()
        self.session.refresh(category)
        return category

    def update(self, category: Category) -> Category:
        self.session.flush()
        self.session.refresh(category)
        return category

    def count_products_by_category(self, category_id: int) -> int:
        stmt = (
            select(func.count(Product.id))
            .where(Product.category_id == category_id)
            )
        return self.session.scalar(stmt)

    def remove(self, category: Category) -> Category:
        self.session.delete(category)
        return category
