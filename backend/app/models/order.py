from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import ForeignKey, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship


from ..database import Base
from ..enums.order_status import OrderStatus


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id')
    )
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.PENDING
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    items: Mapped[list['OrderItem']] = relationship(
        back_populates='order',
        cascade='all, delete-orphan'
    )


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id', ondelete='CASCADE')
    )

    product_id: Mapped[int]
    product_name: Mapped[str]
    product_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    quantity: Mapped[int]

    order: Mapped['Order'] = relationship(back_populates='items')
