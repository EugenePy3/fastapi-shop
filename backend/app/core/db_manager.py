from typing import Callable
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories.user_repository import AuthRepository, UserRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_repository import CartRepository


class DBManager:
    def __init__(self, session_factory: Callable[[], Session] = SessionLocal):
        self.session_factory = session_factory
        self.session: Session | None = None
        self.users: UserRepository | None = None
        self.auth: AuthRepository | None = None

    def __enter__(self) -> "DBManager":
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.auth = AuthRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self.session:
            return

        if exc_type:
            self.session.rollback()

        self.session.close()

    def commit(self) -> None:
        if self.session:
            self.session.commit()
