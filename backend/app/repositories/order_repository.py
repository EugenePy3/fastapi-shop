from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
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
        return await self.session.scalar(stmt)

    async def get_user_orders(self, user_id: int) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(
                joinedload(Order.items)
            )
            .order_by(Order.created_at.desc())
        )
        result = await self.session.scalars(stmt)

        return list(result.all())

    async def create_order(self, user_id: int, total_amount: float) -> Order:
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
        )
        self.session.add(order)
        await self.session.flush()

        return order

    async def add_item(self,
                       order_id: int,
                       product_id: int,
                       product_name: str,
                       product_price: float,
                       quantity: int) -> OrderItem:
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            product_name=product_name,
            product_price=product_price,
            quantity=quantity,
        )
        self.session.add(item)

        return item

    async def update_status(self, order: Order, status: str) -> Order:
        order.status = status
        return order

    async def remove(self, order: Order) -> None:
        await self.session.delete(order)
