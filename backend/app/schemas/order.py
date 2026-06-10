from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from app.enums.order_status import OrderStatus


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description='Order item ID'
    )
    product_id: int = Field(
        description='Product ID'
    )
    product_name: str = Field(
        description='Product name snapshot'
    )
    product_price: float = Field(
        description='Product price snapshot'
    )
    quantity: int = Field(
        description='Quantity'
    )
    subtotal: float = Field(
        description='Subtotal for item'
    )


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description='Order ID'
    )
    user_id: int = Field(
        description='User ID'
    )
    status: str = Field(
        description='Order status'
    )
    total_amount: float = Field(
        description='Total order amount'
    )
    created_at: datetime = Field(
        description='Order creation date'
    )
    items: list[OrderItemResponse] = Field(
        description='Order items'
    )


class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(description='New order status')


class OrderListResponse(BaseModel):
    orders: list[OrderResponse] = Field(description="List of orders")
