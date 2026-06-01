from sqlalchemy import select, delete
from sqlalchemy.orm import Session, joinedload
from ..models.order import Order, OrderItem


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, order_id: int) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.items)
            )
        )
        return self.session.scalar(stmt)

    def get_user_by_id(self, user_id: int) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(
                joinedload(Order.items)
            )
            .order_by(Order.created_at.desc())
        )
        return list(self.session.scalars(stmt).all())

    def create_order(self, user_id: int, total_amount: float) -> Order:
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
        )
        self.session.add(order)

        return order

    def add_item(self,
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

    def update_status(self, order: Order, status: str) -> Order:
        order.status = status
        return order

    def remove(self, order: Order) -> None:
        self.session.delete(order)
