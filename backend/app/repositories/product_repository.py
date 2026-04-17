from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.product import Product
from ..schemas.product import ProductCreate


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Product]:
        return (
            self.session.query(Product)
            .options(joinedload(Product.category))
            .all()
        )

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return (
            self.session.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
            .first()
        )

    def get_by_slug(self, slug: str) -> Optional[Product]:
        return self.session.query(Product).filter(Product.slug == slug).first()

    def get_by_category(self, category_id: int) -> List[Product]:
        return (
            self.session.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.category_id == category_id)
            .all()
        )

    def create(self, product_data: ProductCreate) -> Product:
        session_product = Product(**product_data.model_dump())
        self.session.add(session_product)
        self.session.commit()
        self.session.refresh(session_product)
        return session_product

    def get_multiple_by_ids(self, product_ids: List[int]) -> List[Product]:
        return (
            self.session.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id.in_(product_ids))
            .all()
        )

    def remove(self, product: Product) -> Product:
        print(f"DEBUG: type is {type(product)}")
        self.session.delete(product)
        self.session.commit()
        return product
