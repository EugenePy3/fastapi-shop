from typing import Callable, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal

from app.repositories.user_repository import AuthRepository, UserRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository


class DBManager:
    def __init__(self, session_factory: Callable[[], AsyncSession] = SessionLocal):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

        # Инициализируем репозитории как None,
        # они заполнятся при входе в контекстный менеджер
        self.users: UserRepository | None = None
        self.auth: AuthRepository | None = None
        self.categories: CategoryRepository | None = None
        self.products: ProductRepository | None = None
        self.carts: CartRepository | None = None
        self.orders: OrderRepository | None = None

    def _init_repositories(self):
        # Передаем асинхронную сессию во все репозитории
        self.users = UserRepository(self.session)
        self.auth = AuthRepository(self.session)
        self.categories = CategoryRepository(self.session)
        self.products = ProductRepository(self.session)
        self.carts = CartRepository(self.session)
        self.orders = OrderRepository(self.session)

    async def __aenter__(self) -> "DBManager":
        # Создаем асинхронную сессию
        self.session = self.session_factory()
        self._init_repositories()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self.session:
            return

        try:
            if exc_type:
                # Если внутри блока "async with" произошла ошибка, откатываем изменения
                await self.session.rollback()
            else:
                # Если всё прошло успешно, фиксируем транзакцию
                await self.session.commit()
        finally:
            # В любом случае закрываем сессию для освобождения пула соединений
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


