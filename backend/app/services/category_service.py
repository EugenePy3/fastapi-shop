from ..core.db_manager import DBManager
from ..core.exceptions import CategoryNotFoundError, CategoryDeleteError, CategoryAlreadyExistsError
from ..models import Category
from ..schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: DBManager):
        self.db = db
        self.categories = db.categories

    async def get_all_categories(self) -> list[Category]:
        return await self.categories.get_all()

    async def get_category_by_id(self, category_id: int) -> Category:
        category = await self.categories.get_by_id(category_id)

        if not category:
            raise CategoryNotFoundError(
                f'Category with id {category_id} not found.'
            )

        return category

    async def get_category_by_slug(self, slug: str) -> Category:
        category = await self.categories.get_by_slug(slug)

        if not category:
            raise CategoryNotFoundError(
                f'Category with slug {slug} not found'
            )

        return category

    async def create_category(self, data: CategoryCreate) -> Category:
        existing = await self.categories.get_by_slug(data.slug)

        if existing:
            raise CategoryAlreadyExistsError(
                f'Category with slug {data.slug} already exists'
            )
        category = await self.categories.create(data)

        await self.db.flush()
        await self.db.refresh(category)

        return category

    async def update_category(self, category_id: int, data: CategoryUpdate) -> Category:
        category = await self.categories.get_by_id(category_id)

        if not category:
            raise CategoryNotFoundError(
                f'Category with id {category_id} not found'
            )

        if data.slug:
            existing = await self.categories.get_by_slug(data.slug)
            if existing and existing.id != category_id:
                raise CategoryAlreadyExistsError(
                    f'Category with slug {data.slug} already exists'
                )

        if data.name is not None:
            category.name = data.name
        if data.slug is not None:
            category.slug = data.slug

        await self.db.flush()
        await self.db.refresh(category)

        return category

    async def remove_category(self, category_id: int) -> None:
        category = await self.categories.get_by_id(category_id)

        if not category:
            raise CategoryNotFoundError(
                f'Category with id {category_id} not found'
            )

        product_count = await self.categories.count_products_by_category(category_id)

        if product_count > 0:
            raise CategoryDeleteError(
                f'Cannot delete category: {product_count} products still assigned'
            )

        await self.db.delete(category)
        await self.db.flush()

