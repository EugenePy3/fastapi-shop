from typing import Callable, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.repositories.session_repository import SessionRepository

from app.repositories.user_repository import UserRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository


class DBManager:
    """
    Coordinates repositories and manages
    the SQLAlchemy session lifecycle.
    """
    def __init__(self, session_factory: Callable[[], AsyncSession] = AsyncSessionLocal):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

        self.users: UserRepository | None = None
        self.sessions: SessionRepository | None
        self.categories: CategoryRepository | None = None
        self.products: ProductRepository | None = None
        self.carts: CartRepository | None = None
        self.orders: OrderRepository | None = None

    def _init_repositories(self):
        self.users = UserRepository(self.session)
        self.sessions = SessionRepository(self.session)
        self.categories = CategoryRepository(self.session)
        self.products = ProductRepository(self.session)
        self.carts = CartRepository(self.session)
        self.orders = OrderRepository(self.session)

    async def __aenter__(self) -> "DBManager":
        self.session = self.session_factory()
        self._init_repositories()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:

        if not self.session:
            return

        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()

    async def flush(self) -> None:
        if self.session:
            await self.session.flush()

    async def refresh(self, instance: Any) -> None:
        if self.session:
            await self.session.refresh(instance)

    async def delete(self, instance: Any) -> None:
        if self.session:
            await self.session.delete(instance)


