from ..core.db_manager import DBManager
from ..core.exceptions import CartNotFoundError, EmptyCartError, OrderNotFoundError
from ..enums.order_status import OrderStatus
from ..models.order import Order


class OrderService:
    def __init__(self, db: DBManager):
        self.orders = db.orders
        self.carts = db.carts

    async def create_order_from_cart(self, user_id: int) -> Order:
        cart = await self.carts.get_by_user_id(user_id)
        if not cart:
            raise CartNotFoundError(f'Cart for user with id {user_id} not found.')
        if not cart.items:
            raise EmptyCartError('Cannot create an order because your cart is empty.')

        total_amount = sum(
            item.product.price * item.quantity
            for item in cart.items
        )
        order = await self.orders.create_order(
            user_id=user_id,
            total_amount=total_amount
        )
        for item in cart.items:
            await self.orders.add_item(
                order_id=order.id,
                product_id=item.product.id,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity,

            )
        await self.carts.clear_cart(cart.id)

        return order

    async def get_order(self, order_id: int) -> Order:
        order = await self.orders.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(f'Order with id {order_id} not found.')

        return order

    async def get_user_orders(self, user_id: int) -> list[Order]:
        return await self.orders.get_user_orders(user_id)

    async def update_status(self, order_id: int, status: OrderStatus) -> Order:
        order = await self.orders.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(f'Order with id {order_id} not found.')

        return await self.orders.update_status(
            order,
            status,
        )
