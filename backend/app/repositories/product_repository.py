from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.product import Product
from ..schemas.product import ProductCreate


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
        )

        return self.session.execute(stmt).scalars().all()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id == product_id)
        )

        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_slug(self, slug: str) -> Optional[Product]:
        stmt = select(Product).where(Product.slug == slug)

        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_category(self, category_id: int) -> List[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.category_id == category_id)
        )

        return self.session.execute(stmt).scalars().all()

    def create(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())

        self.session.add(product)
        self.session.flush()
        self.session.refresh(product)

        return product

    def update(self, product: Product) -> Product:
        self.session.add(product)
        self.session.flush()
        self.session.refresh(product)

        return product

    def get_multiple_by_ids(self, product_ids: List[int]) -> List[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id.in_(product_ids))
        )

        return self.session.execute(stmt).scalars().all()

    def remove(self, product: Product) -> Product:
        self.session.delete(product)
        self.session.flush()

        return product
