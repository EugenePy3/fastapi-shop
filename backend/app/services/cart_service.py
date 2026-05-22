from sqlalchemy.orm import Session
from ..repositories.product_repository import ProductRepository
from ..repositories.cart_repository import CartRepository
from ..schemas.cart import CartResponse, CartItem, CartItemCreate, CartItemUpdate
from ..core.exceptions import ProductNotFoundError, CartItemNotFoundError


class CartService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.cart_repository = CartRepository(db)

    def add_to_cart(self, user_id: int, item: CartItemCreate) -> CartItem:
        product = self.product_repository.get_by_id(item.product_id)
        if not product:
            raise ProductNotFoundError(f'Product with id {item.product_id} not found')

        existing_item = self.cart_repository.get_cart_item(
            user_id=user_id,
            product_id=item.product_id
        )
        if existing_item:
            existing_item.quantity += item.quantity
            return existing_item

        cart_item = self.cart_repository.create_cart_item(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        self.db.commit()
        return cart_item

    def update_cart_item(self, user_id: int, item: CartItemUpdate) -> CartItem:
        cart_item = self.cart_repository.get_cart_item(
            user_id=user_id,
            product_id=item.product_id,
        )

        if not cart_item:
            raise CartItemNotFoundError(f'Product with id {item.product_id} not found in cart')

        update_item = self.cart_repository.update_cart_item(
            cart_item=cart_item,
            quantity=cart_item.quantity,
        )
        self.db.commit()
        return update_item

    def remove_from_cart(self, user_id: int, product_id: int) -> None:
        cart_item = self.cart_repository.get_cart_item(
            user_id=user_id,
            product_id=product_id
        )
        if not cart_item:
            raise CartItemNotFoundError(f'Product with id {product_id} not found in cart')

        self.cart_repository.delete_cart_item(cart_item)

    def get_cart_details(self, user_id: int, item: CartItem) -> CartResponse:
        cart_items = self.cart_repository.get_user_cart(user_id)

        if not cart_items:
            return CartResponse(
                items=[],
                total=0.0,
                items_count=0)

        response_items = []

        total_price = 0.0
        total_items = 0

        subtotal = item.product.price * item.quantity

        response_item = CartItem(
            product_id=item.product_id,
            name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
            subtotal=item.subtotal,
            image_url=item.product.image_url
        )

        response_items.append(response_item)

        total_price += subtotal
        total_items += item.quantity

        return CartResponse(items=response_items, total=round(total_price, 2),
                            items_count=total_items)

