from ..core.db_manager import DBManager
from ..models.cart import CartItem, Cart
from ..core.exceptions import ProductNotFoundError, CartItemNotFoundError


class CartService:
    def __init__(self, db: DBManager):
        self.carts = db.carts
        self.products = db.products

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> CartItem:
        cart = await self.carts.get_or_create_cart(user_id)
        product = await self.products.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f'Product with id {product_id} not found')

        item = await self.carts.get_item(
            cart.id,
            product_id
        )
        if item:
            item.quantity += quantity
            return item

        return await self.carts.add_item(
            cart.id,
            product_id,
            quantity
        )

    async def get_cart(self, user_id: int) -> Cart:
        return await self.carts.get_or_create_cart(user_id)

    async def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> CartItem:
        cart = await self.carts.get_or_create_cart(user_id)
        item = await self.carts.get_item(
            cart.id,
            product_id
        )
        if not item:
            raise CartItemNotFoundError(f'Product with id {item.product_id} not found in cart')
        item.quantity = quantity

        return item

    async def remove_item(self, user_id: int, product_id: int) -> None:
        cart = await self.carts.get_or_create_cart(user_id)
        item = await self.carts.get_item(
            cart.id,
            product_id
        )
        if not item:
            raise CartItemNotFoundError(f'Product with id {product_id} not found in cart')

        await self.carts.remove_item(item)

    async def clear_cart(self, user_id: int) -> None:
        cart = await self.carts.get_or_create_cart(user_id)
        await self.carts.clear_cart(cart.id)


