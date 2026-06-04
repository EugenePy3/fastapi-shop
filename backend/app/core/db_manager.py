from typing import Callable
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories.user_repository import AuthRepository, UserRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository


class DBManager:
    def __init__(self, session_factory: Callable[[], Session] = SessionLocal):
        self.session_factory = session_factory
        self.session: Session | None = None

        self.users: UserRepository | None = None
        self.auth: AuthRepository | None = None
        self.categories: CategoryRepository | None = None
        self.products: ProductRepository | None = None
        self.carts: CartRepository | None = None
        self.orders: OrderRepository | None = None

    def __enter__(self) -> "DBManager":
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.auth = AuthRepository(self.session)
        self.categories = CategoryRepository(self.session)
        self.products = ProductRepository(self.session)
        self.carts = CartRepository(self.session)
        self.orders = OrderRepository(self.session)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self.session:
            return

        try:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()


