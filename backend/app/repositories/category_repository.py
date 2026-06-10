from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..models.category import Category
from ..models.product import Product
from ..schemas.category import CategoryCreate


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Category]:
        stmt = select(Category)
        result = await self.session.scalars(stmt)

        return list(result.all())

    async def get_by_id(self, category_id: int) -> Category | None:
        stmt = (
            select(Category)
            .where(Category.id == category_id)
        )
        return await self.session.scalar(stmt)

    async def get_by_slug(self, slug: str) -> Category | None:
        stmt = (
            select(Category)
            .where(Category.slug == slug)
        )
        return await self.session.scalar(stmt)

    async def create(self, category_data: CategoryCreate) -> Category:
        category = Category(**category_data.model_dump())
        self.session.add(category)

        return category

    async def update(self, category: Category) -> Category:
        await self.session.flush()
        await self.session.refresh(category)

        return category

    async def count_products_by_category(self, category_id: int) -> int:
        stmt = (
            select(func.count(Product.id))
            .where(Product.category_id == category_id)
            )
        return await self.session.scalar(stmt)

    async def remove(self, category: Category) -> Category:
        await self.session.delete(category)
        return category
