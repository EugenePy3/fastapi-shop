from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..database import Base


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped['User'] = relationship(back_populates='cart')

    items: Mapped[list['CartItem']] = relationship(
        back_populates='cart',
        cascade='all, delete-orphan'
    )


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(primary_key=True)

    cart_id: Mapped[int] = mapped_column(
        ForeignKey('carts.id', ondelete='CASCADE')
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE')
    )
    quantity: Mapped[int] = mapped_column(default=1)

    cart: Mapped['Cart'] = relationship(back_populates='items')

    product: Mapped['Product'] = relationship()
