from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from ..models.product import Product
from ..schemas.product import ProductCreate


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
        )
        result = await self.session.scalars(stmt)

        return list(result.all())

    async def get_by_id(self, product_id: int) -> Product | None:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id == product_id)
        )

        return await self.session.scalar(stmt)

    async def get_by_slug(self, slug: str) -> Product | None:
        stmt = select(Product).where(Product.slug == slug)

        return await self.session.scalar(stmt)

    async def get_by_category(self, category_id: int) -> list[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.category_id == category_id)
        )
        result = await self.session.scalars(stmt)

        return list(result.all())

    async def create(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())

        self.session.add(product)
        # await self.session.flush()
        # await self.session.refresh(product)

        return product

    async def update(self, product: Product) -> Product:
        self.session.add(product)

        return product

    async def get_multiple_by_ids(self, product_ids: list[int]) -> list[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id.in_(product_ids))
        )
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def remove(self, product: Product) -> Product:
        await self.session.delete(product)
        # await self.session.flush()

        return product
