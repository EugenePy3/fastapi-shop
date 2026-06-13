from sqlalchemy import String, Text, DateTime, ForeignKey, func, Numeric
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from ..database import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200), nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(
        String(255), index=True, nullable=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

    category: Mapped['Category'] = relationship(back_populates='products')

    def __repr__(self):
        return f'<Product(id={self.id}, name={self.name}, price={self.price})>'

