from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from app.schemas.types import Money


class CartItemCreate(BaseModel):
    product_id: int = Field(
        description='Product ID'
    )
    quantity: int = Field(
        default=1,
        gt=0,
        description='Quantity'
    )


class CartItemUpdate(BaseModel):
    quantity: int = Field(
        gt=0,
        description='Update quantity'
    )


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description='Cart item ID'
    )
    product_id: int = Field(
        description='Product ID'
    )
    name: str = Field(
        description='Product name'
    )
    price: Money = Field(
        description='Product price'
    )
    quantity: int = Field(
        description='Quantity in cart'
    )
    subtotal: Money = Field(
        description='Total price for this item (price * quantity)'
    )
    image_url: str | None = Field(
        default=None,
        description='Product image url'
    )


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description='Cart ID'
    )
    created_at: datetime = Field(
        description='Cart creation date'
    )
    items: list[CartItemResponse] = Field(
        description='List of item in cart'
    )
    total: Money = Field(
        description='Total cart price'
    )
    items_count: int = Field(
        description='Total number of items in cart'
    )
