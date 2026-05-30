from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Dict
from ..database import get_db
from ..models import User
from ..services.cart_service import CartService
from ..schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from ..dependencies import get_current_user_from_session, DBManagerDep

router = APIRouter(
    prefix='/api/cart',
    tags=['cart']
)


@router.get('', response_model=CartResponse, status_code=status.HTTP_200_OK)
def get_cart(
        db: DBManagerDep,
        current_user: User = Depends(get_current_user_from_session)
):
    service = CartService(db)
    return service.get_cart_details(current_user.id)


@router.post('/add', status_code=status.HTTP_200_OK)
def add_to_cart(
        cart_data: CartItemCreate,
        db: DBManagerDep,
        current_user: User = Depends(get_current_user_from_session)
):
    service = CartService(db)
    return service.add_to_cart(current_user.id, cart_data)


@router.put('/update', status_code=status.HTTP_200_OK)
def update_cart_item(
        update_data: CartItemUpdate,
        db: DBManagerDep,
        current_user: User = Depends(get_current_user_from_session)
):
    service = CartService(db)
    return service.update_cart_item(current_user.id, update_data)


@router.delete('/remove/{product_id}', status_code=status.HTTP_200_OK)
def remove_from_cart(
        product_id: int,
        db: DBManagerDep,
        current_user: User = Depends(get_current_user_from_session)
):
    service = CartService(db)
    return service.remove_from_cart(current_user.id, product_id)

