from sqlalchemy import select, delete
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..models.cart import CartItem


class CartRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_cart(self, user_id: int) -> List[CartItem]:
        stmt = (
            select(CartItem)
            .where(CartItem.user_id == user_id)
            .options(joinedload(CartItem.product))
        )
        return list(self.session.scalars(stmt).all())

    def get_cart_item(self, user_id: int, product_id: int) -> CartItem | None:
        stmt = (
            select(CartItem)
            .where(CartItem.user_id == user_id)
            .where(CartItem.product_id == product_id)
        )
        return self.session.scalar(stmt)

    def create_cart_item(self, user_id: int, product_id: int, quantity: int) -> CartItem:
        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
        )
        self.session.add(cart_item)
        return cart_item

    def update_cart_item(self, cart_item: CartItem, quantity: int) -> CartItem:
        cart_item.quantity = quantity
        return cart_item

    def delete_cart_item(self, cart_item: CartItem) -> None:
        self.session.delete(cart_item)

    def clear_user_cart(self, user_id: int) -> None:
        stmt = (
            delete(CartItem)
            .where(CartItem.user_id == user_id)
        )
        self.session.execute(stmt)
