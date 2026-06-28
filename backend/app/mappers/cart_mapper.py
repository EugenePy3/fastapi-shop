from app.models.cart import Cart, CartItem
from app.schemas.cart import CartResponse, CartItemResponse


def to_cart_item_response(item: CartItem) -> CartItemResponse:
    return CartItemResponse(
        id=item.id,
        product_id=item.product.id,
        name=item.product.name,
        price=item.product.price,
        quantity=item.quantity,
        subtotal=item.product.price * item.quantity,
        image_url=item.product.image_url,
    )


def to_cart_response(cart: Cart) -> CartResponse:
    items = [
        to_cart_item_response(item)
        for item in cart.items
    ]

    return CartResponse(
        id=cart.id,
        created_at=cart.created_at,
        items=items,
        total=sum(item.subtotal for item in items),
        items_count=sum(item.quantity for item in items),
    )
