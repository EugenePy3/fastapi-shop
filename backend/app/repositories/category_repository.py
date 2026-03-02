from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.category import Category
from ..schemas.category import CategoryCreate


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Category]:
        return self.session.query(Category).all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.session.query(Category).filter(Category.id == category_id).first()

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return self.session.query(Category).filter(Category.slug == slug).first()

    def create(self, category_data: CategoryCreate) -> Category:
        db_category = Category(**category_data.model_dump())
        self.session.add(db_category)
        self.session.commit()
        self.session.refresh(db_category)
        return db_category
