from sqlalchemy import select, delete
from sqlalchemy.orm import Session, joinedload
from ..models.cart import Cart, CartItem


class CartRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: int) -> Cart | None:
        stmt = (
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(
                joinedload(Cart.items)
                .joinedload(CartItem.product))
        )
        return self.session.scalar(stmt)

    def create_cart(self, user_id: int) -> Cart:
        cart = Cart(user_id=user_id)
        self.session.add(cart)

        return cart

    def get_or_create_cart(self, user_id: int) -> Cart:
        cart = self.get_by_user_id(user_id)

        if cart:
            return cart

        return self.create_cart(user_id)

    # Работа с CartItem

    def get_item(self, cart_id: int, product_id: int) -> CartItem | None:
        stmt = (
            select(CartItem)
            .where(CartItem.cart_id == cart_id)
            .where(CartItem.product_id == product_id)
        )
        return self.session.scalar(stmt)

    def add_item(self, cart_id: int, product_id: int, quantity: int) -> CartItem:
        item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
        )
        self.session.add(item)
        
        return item

    def remove_item(self, item: CartItem) -> None:
        self.session.delete(item)

    def clear_cart(self, cart_id: int) -> None:
        stmt = (
            delete(CartItem)
            .where(CartItem.cart_id == cart_id)
        )
        self.session.execute(stmt)
