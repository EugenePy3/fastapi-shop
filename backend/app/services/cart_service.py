from ..core.db_manager import DBManager
from ..models.cart import CartItem, Cart
from ..core.exceptions import ProductNotFoundError, CartItemNotFoundError


class CartService:
    def __init__(self, db: DBManager):
        self.db = db
        self.carts = db.carts
        self.products = db.products

    async def _get_or_create_cart(self, user_id: int) -> Cart:
        cart = await self.carts.get_by_user_id(user_id)

        if cart:
            return cart

        await self.carts.create_cart(user_id)
        await self.db.flush()
        return await self.carts.get_by_user_id(user_id)

    async def _get_item_or_raise(self, cart_id: int, product_id: int) -> CartItem:
        item = await self.carts.get_item(cart_id, product_id)

        if item is None:
            raise CartItemNotFoundError(f'Product with id {product_id} not found in cart')
        return item

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> CartItem:
        cart = await self._get_or_create_cart(user_id)
        product = await self.products.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError(f'Product with id {product_id} not found')

        item = await self.carts.get_item(cart.id, product_id)

        if item:
            item.quantity += quantity
            return item

        item = await self.carts.add_item(cart.id, product, quantity)
        await self.db.flush()
        return item

    async def get_cart(self, user_id: int) -> Cart:
        return await self._get_or_create_cart(user_id)

    async def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> CartItem:
        cart = await self._get_or_create_cart(user_id)
        item = await self._get_item_or_raise(cart.id, product_id)
        item.quantity = quantity
        return item

    async def remove_item(self, user_id: int, product_id: int) -> None:
        cart = await self._get_or_create_cart(user_id)
        item = await self._get_item_or_raise(cart.id, product_id)
        await self.db.delete(item)

    async def clear_cart(self, user_id: int) -> None:
        cart = await self._get_or_create_cart(user_id)
        await self.carts.clear_cart(cart.id)
