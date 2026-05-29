from decimal import Decimal

from ..core.db_manager import DBManager
from ..schemas.cart import CartResponse, CartItemResponse, CartItemCreate, CartItemUpdate
from ..core.exceptions import ProductNotFoundError, CartItemNotFoundError


class CartService:
    def __init__(self, db: DBManager):
        self.db = db
        self.products = db.products
        self.carts = db.carts

    def add_to_cart(self, user_id: int, item: CartItemCreate) -> CartItemResponse:
        product = self.products.get_by_id(item.product_id)
        if not product:
            raise ProductNotFoundError(f'Product with id {item.product_id} not found')

        existing_item = self.carts.get_cart_item(
            user_id=user_id,
            product_id=item.product_id
        )
        if existing_item:
            existing_item.quantity += item.quantity
            return existing_item

        cart_item = self.carts.create_cart_item(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        return cart_item

    def update_cart_item(self, user_id: int, item: CartItemUpdate) -> CartItemResponse:
        cart_item = self.carts.get_cart_item(
            user_id=user_id,
            product_id=item.product_id,
        )

        if not cart_item:
            raise CartItemNotFoundError(f'Product with id {item.product_id} not found in cart')

        update_item = self.carts.update_cart_item(
            cart_item=cart_item,
            quantity=item.quantity,
        )
        return update_item

    def remove_from_cart(self, user_id: int, product_id: int) -> None:
        cart_item = self.carts.get_cart_item(
            user_id=user_id,
            product_id=product_id
        )
        if not cart_item:
            raise CartItemNotFoundError(f'Product with id {product_id} not found in cart')

        self.carts.delete_cart_item(cart_item)

    def get_cart_details(self, user_id: int) -> CartResponse:
        cart_items = self.carts.get_user_cart(user_id)

        if not cart_items:
            return CartResponse(
                items=[],
                total=0.0,
                items_count=0
            )

        response_items = []

        total_price = Decimal('0.00')
        total_items = 0

        for item in cart_items:
            subtotal = item.product.price * item.quantity

            response_item = CartItemResponse(
                product_id=item.product_id,
                name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
                subtotal=subtotal,
                image_url=item.product.image_url
            )

            response_items.append(response_item)

            total_price += subtotal
            total_items += item.quantity

        return CartResponse(
            items=response_items,
            total=round(total_price, 2),
            items_count=total_items
        )
