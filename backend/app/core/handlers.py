from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    CategoryNotFoundError,
    CategoryAlreadyExistsError,
    CategoryDeleteError
)

from app.core.exceptions import (
    ProductNotFoundError
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


