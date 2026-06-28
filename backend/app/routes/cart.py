from fastapi import APIRouter,  status

from ..services.cart_service import CartService
from ..schemas.cart import CartItemCreate, CartItemUpdate, CartResponse, CartItemResponse
from ..dependencies import DBManagerDep, CurrentUserDep
from app.mappers import (
    to_cart_response,
    to_cart_item_response,
)

router = APIRouter(
    prefix='/api/cart',
    tags=['cart']
)


@router.get('', response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_cart(
        db: DBManagerDep,
        user: CurrentUserDep,
):
    service = CartService(db)
    cart = await service.get_cart(user.id)
    return to_cart_response(cart)


@router.post('/items', response_model=CartItemResponse, status_code=status.HTTP_200_OK)
async def add_to_cart(
        item: CartItemCreate,
        db: DBManagerDep,
        user: CurrentUserDep
):
    service = CartService(db)
    item = await service.add_to_cart(
        user.id,
        item.product_id,
        item.quantity,
    )
    return to_cart_item_response(item)


@router.patch('/items/{product_id}', response_model=CartItemResponse, status_code=status.HTTP_200_OK)
async def update_cart_item(
        product_id: int,
        item: CartItemUpdate,
        db: DBManagerDep,
        user: CurrentUserDep,
):
    service = CartService(db)
    item = await service.update_item_quantity(
        user.id,
        product_id,
        item.quantity,
    )
    return to_cart_item_response(item)


@router.delete('/items/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_cart_item(
        product_id: int,
        db: DBManagerDep,
        user: CurrentUserDep,
):
    service = CartService(db)

    await service.remove_item(
        user.id,
        product_id,
    )


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
        db: DBManagerDep,
        user: CurrentUserDep,
):
    service = CartService(db)

    await service.clear_cart(user.id)
