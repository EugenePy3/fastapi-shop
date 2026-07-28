from fastapi import APIRouter, status
from app.mappers.order_mapper import (
    to_order_response,
    to_order_list_response,
)

from ..dependencies import DBManagerDep, CurrentUserDep, AdminUserDep
from ..schemas.order import OrderResponse, OrderListResponse, OrderStatusUpdate
from ..services.order_service import OrderService

router = APIRouter(
    prefix='/api/order',
    tags=['order']
)


@router.post('', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
        db: DBManagerDep,
        user: CurrentUserDep,
):
    service = OrderService(db)

    order = await service.create_order_from_cart(user.id)
    return to_order_response(order)


@router.get('', response_model=OrderListResponse, status_code=status.HTTP_200_OK)
async def get_my_orders(
        db: DBManagerDep,
        user: CurrentUserDep,
):
    service = OrderService(db)
    orders = await service.get_user_orders(user.id)
    return OrderListResponse(orders=to_order_list_response(orders))


@router.get('/{order_id}', response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(
        order_id: int,
        db: DBManagerDep,
        user: CurrentUserDep,
):
    service = OrderService(db)

    order = await service.get_order(order_id, user)
    return to_order_response(order)


@router.patch('/{order_id}/status', response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def update_order_status(
        order_id: int,
        data: OrderStatusUpdate,
        db: DBManagerDep,
        admin: AdminUserDep,
):
    service = OrderService(db)

    order = await service.update_status(order_id, data.status)
    return to_order_response(order)

