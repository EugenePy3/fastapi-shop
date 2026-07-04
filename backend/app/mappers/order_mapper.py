from app.models.order import Order, OrderItem
from app.schemas.order import OrderResponse, OrderItemResponse


def to_order_item_response(item: OrderItem) -> OrderItemResponse:
    return OrderItemResponse(
        id=item.id,
        product_id=item.product_id,
        product_name=item.product_name,
        product_price=item.product_price,
        quantity=item.quantity,
        subtotal=item.product_price * item.quantity,
    )


def to_order_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        status=order.status.value,
        total_amount=order.total_amount,
        created_at=order.created_at,
        items=[
            to_order_item_response(item)
            for item in order.items
        ],
    )


def to_order_list_response(
    orders: list[Order],
) -> list[OrderResponse]:
    return [
        to_order_response(order)
        for order in orders
    ]
