from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    CategoryNotFoundError,
    CategoryAlreadyExistsError,
    CategoryDeleteError,
    ProductNotFoundError,
    CartItemNotFoundError
)


def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=400,
        content={'detail': str(exc)}
    )


def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,
        content={'detail': str(exc)}
    )


def category_not_found_handler(request: Request, exc: CategoryNotFoundError):
    return JSONResponse(
        status_code=404,
        content={'detail': str(exc)}
    )


def category_already_exists_handler(request: Request, exc: CategoryAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={'detail': str(exc)}
    )


def category_delete_error_handler(request: Request, exc: CategoryDeleteError):
    return JSONResponse(
        status_code=409,
        content={'detail': str(exc)}
    )


def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return JSONResponse(
        status_code=404,
        content={'detail': str(exc)}
    )


def cart_item_not_found_handler(request: Request, exc: CartItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={'detail': str(exc)}
    )




