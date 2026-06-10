from slugify import slugify

from ..core.db_manager import DBManager
from ..core.exceptions import ProductNotFoundError, CategoryNotFoundError
from ..models import Product
from ..schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: DBManager):
        self.db = db
        self.products = db.products
        self.categories = db.categories

    async def get_all_products(self) -> list[Product]:
        return await self.products.get_all()

    async def get_product_by_id(self, product_id: int) -> Product:
        product = await self.products.get_by_id(product_id)

        if not product:
            raise ProductNotFoundError(f'Product with id {product_id} not found')

        return product

    async def get_products_by_category(self, category_id: int) -> list[Product]:
        category = await self.categories.get_by_id(category_id)

        if not category:
            raise CategoryNotFoundError(f'Category with id {category_id} not found')

        return await self.products.get_by_category(category_id)

    async def create_product(self, data: ProductCreate) -> Product:
        category = await self.categories.get_by_id(data.category_id)

        if not category:
            raise CategoryNotFoundError(f'Category with id {data.category_id} not found')

        product = await self.products.create(data)

        await self.db.flush()

        product.slug = (
            f"{slugify(product.name, lowercase=True)}-{product.id}"
        )

        return product

    async def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        product = await self.products.get_by_id(product_id)

        if not product:
            raise ProductNotFoundError(f'Product with id {product_id} not found')

        if data.category_id is not None:
            category = await self.categories.get_by_id(data.category_id)

            if not category:
                raise CategoryNotFoundError(f'Category with id {data.category_id} not found')

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(product, field, value)

        if data.name is not None:
            product.slug = (
                f"{slugify(product.name, lowercase=True)}-{product.id}"
            )

        await self.db.flush()

        return product

    async def remove_product(self, product_id: int) -> Product:
        product = await self.products.get_by_id(product_id)

        if not product:
            raise ProductNotFoundError(f'Product with id {product_id} not found')

        await self.db.delete(product)
        await self.db.flush()

        return product
