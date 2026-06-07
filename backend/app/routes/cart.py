from fastapi import APIRouter, Depends, status
from ..models import User
from ..services.cart_service import CartService
from ..schemas.cart import CartItemCreate, CartItemUpdate, CartResponse, CartItemResponse
from ..dependencies import get_current_user_from_session, DBManagerDep

router = APIRouter(
    prefix='/api/cart',
    tags=['cart']
)


@router.get('', response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_cart(
        db: DBManagerDep,
        user: User = Depends(get_current_user_from_session),
):
    service = CartService(db)
    return await service.get_cart(user.id)


@router.post('/items', response_model=CartItemResponse, status_code=status.HTTP_200_OK)
async def add_to_cart(
        item: CartItemCreate,
        db: DBManagerDep,
        user: User = Depends(get_current_user_from_session)
):
    service = CartService(db)
    return await service.add_to_cart(
        user.id,
        item.product_id,
        item.quantity,
    )


@router.patch('/items/{product_id}', response_model=CartItemResponse, status_code=status.HTTP_200_OK)
async def update_cart_item(
        product_id: int,
        item: CartItemUpdate,
        db: DBManagerDep,
        user: User = Depends(get_current_user_from_session)
):
    service = CartService(db)
    return await service.update_item_quantity(
        user.id,
        product_id,
        item.quantity,
    )


@router.delete('/items/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_cart_item(
        product_id: int,
        db: DBManagerDep,
        user: User = Depends(get_current_user_from_session)
):
    service = CartService(db)

    await service.remove_item(
        user.id,
        product_id,
    )


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
        db: DBManagerDep,
        user: User = Depends(get_current_user_from_session),
):
    service = CartService(db)

    await service.clear_cart(user.id)
