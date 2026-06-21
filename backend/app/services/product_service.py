from slugify import slugify


from ..core.db_manager import DBManager
from ..core.exceptions import ProductNotFoundError, CategoryNotFoundError
from ..models import Product, Category
from ..schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: DBManager):
        self.db = db
        self.products = db.products
        self.categories = db.categories

    @staticmethod
    def _build_slug(product: Product) -> str:
        return f'{slugify(product.name, lowercase=True)}-{product.id}'

    async def _get_product_or_raise(self, product_id: int) -> Product:
        product = await self.products.get_by_id(product_id)

        if not product:
            raise ProductNotFoundError(f'Product with id {product_id} not found')
        return product

    async def _get_category_or_raise(self, category_id: int) -> Category:
        category = await self.categories.get_by_id(category_id)

        if not category:
            raise CategoryNotFoundError(f'Category with id {category_id} not found')
        return category

    async def get_all_products(self) -> list[Product]:
        return await self.products.get_all()

    async def get_product_by_id(self, product_id: int) -> Product:
        product = await self._get_product_or_raise(product_id)
        return product

    async def get_products_by_category(self, category_id: int) -> list[Product]:
        await self._get_category_or_raise(category_id)
        return await self.products.get_by_category(category_id)

    async def create_product(self, data: ProductCreate) -> Product:
        category = await self._get_category_or_raise(data.category_id)

        product = await self.products.create(data)
        product.category = category

        await self.db.flush()

        product.slug = self._build_slug(product)
        return product

    async def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        product = await self._get_product_or_raise(product_id)

        if data.category_id is not None:
            category = await self._get_category_or_raise(data.category_id)
            product.category = category

        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(product, field, value)

        if data.name is not None:
            product.slug = self._build_slug(product)

        await self.db.flush()
        return product

    async def remove_product(self, product_id: int) -> None:
        product = await self._get_product_or_raise(product_id)

        await self.db.delete(product)
        await self.db.flush()

