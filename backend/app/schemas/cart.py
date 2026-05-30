from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CartItemCreate(BaseModel):
    product_id: int = Field(..., description='Product ID')
    quantity: int = Field(1, gt=0, description='Quantity (must be greater than 0)')


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, description='Update quantity (must be greater than 0)')


class CartItemResponse(BaseModel):
    id: int = Field(..., description='Cart item ID')
    product_id: int = Field(..., description='Product ID')
    name: str = Field(..., description='Product name')
    price: float = Field(..., description='Product price')
    quantity: int = Field(..., description='Quantity in cart')
    subtotal: float = Field(..., description='Total price for this item (price * quantity)')
    image_url: Optional[str] = Field(None, description='Product image url')


class CartResponse(BaseModel):
    id: int = Field(..., description='Cart ID')
    created_at: datetime = Field(..., description='Cart creation date')
    items: list[CartItemResponse] = Field(..., description='List of item in cart')
    total: float = Field(..., description='Total cart price')
    items_count: int = Field(..., description='Total number of items in cart')
