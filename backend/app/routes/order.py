from fastapi import APIRouter, Depends, status

from ..dependencies import DBManagerDep, get_current_user_from_session, require_admin, CurrentUserDep, AdminUserDep
from ..models import User
from ..schemas.order import OrderResponse, OrderListResponse, OrderStatusUpdate
from ..services.order_service import OrderService

router = APIRouter(
    prefix='/api/order',
    tags=['order']
)


@router.post('', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
        db: DBManagerDep,
        user: User = CurrentUserDep,
):
    service = OrderService(db)

    return await service.create_order_from_cart(user.id)


@router.get('', response_model=OrderListResponse, status_code=status.HTTP_200_OK)
async def get_my_orders(
        db: DBManagerDep,
        user: User = CurrentUserDep,
):
    service = OrderService(db)
    orders = await service.get_user_orders(user.id)

    return OrderListResponse(
        orders=orders
    )


@router.get('/{order_id}/status', response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(
        order_id: int,
        db: DBManagerDep,
        user: User = CurrentUserDep,
):
    service = OrderService(db)

    return await service.get_order(
        order_id,
        user,
    )


@router.patch('order_id/status', response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def update_order_status(
        order_id: int,
        data: OrderStatusUpdate,
        db: DBManagerDep,
        admin: User = AdminUserDep,
):
    service = OrderService(db)

    return await service.update_status(
        order_id,
        data.status,
    )

