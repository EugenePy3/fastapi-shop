from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from ..models.cart import Cart, CartItem


class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: int) -> Cart | None:
        stmt = (
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(
                joinedload(Cart.items)
                .joinedload(CartItem.product))
        )
        return await self.session.scalar(stmt)

    async def create_cart(self, user_id: int) -> Cart:
        cart = Cart(user_id=user_id)
        self.session.add(cart)

        return cart

    async def get_or_create_cart(self, user_id: int) -> Cart:
        cart = await self.get_by_user_id(user_id)

        if cart:
            return cart

        return await self.create_cart(user_id)

    # CartItem

    async def get_item(self, cart_id: int, product_id: int) -> CartItem | None:
        stmt = (
            select(CartItem)
            .where(CartItem.cart_id == cart_id)
            .where(CartItem.product_id == product_id)
        )
        return await self.session.scalar(stmt)

    async def add_item(self, cart_id: int, product_id: int, quantity: int) -> CartItem:
        item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
        )
        self.session.add(item)
        
        return item

    async def remove_item(self, item: CartItem) -> None:
        await self.session.delete(item)

    async def clear_cart(self, cart_id: int) -> None:
        stmt = (
            delete(CartItem)
            .where(CartItem.cart_id == cart_id)
        )
        await self.session.execute(stmt)
