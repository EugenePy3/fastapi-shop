from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from decimal import Decimal

from ..models.cart import CartItem
from ..models.order import Order, OrderItem


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: int) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.items)
            )
        )
        result = await self.session.execute(stmt)

        return result.unique().scalar_one_or_none()

    async def get_user_orders(self, user_id: int) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(
                joinedload(Order.items)
            )
            .order_by(Order.created_at.desc())
        )
        result = await self.session.execute(stmt)

        return list(result.scalars().unique().all())

    async def create_order(self, user_id: int, total_amount: Decimal) -> Order:
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
        )
        self.session.add(order)
        return order

    def add_item(
            self,
            order: Order,
            cart_item: CartItem,
    ) -> OrderItem:
        item = OrderItem(
            product_id=cart_item.product.id,
            product_name=cart_item.product.name,
            product_price=cart_item.product.price,
            quantity=cart_item.quantity,
        )
        order.items.append(item)
        return item

    async def update_status(self, order: Order, status: str) -> Order:
        order.status = status
        return order
