from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from .database import init_db
from .routes import products_router, categories_router, cart_router, auth_router, session_router

from app.core.handlers import (
    user_already_exists_handler,
    invalid_credentials_handler,
    category_not_found_handler,
    category_already_exists_handler,
    category_delete_error_handler,
    product_not_found_handler,
    cart_item_not_found_handler
)


from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    CategoryNotFoundError,
    CategoryAlreadyExistsError,
    CategoryDeleteError,
    ProductNotFoundError,
    CartItemNotFoundError
)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_exception_handler(
    UserAlreadyExistsError,
    user_already_exists_handler
)

app.add_exception_handler(
    InvalidCredentialsError,
    invalid_credentials_handler
)

app.add_exception_handler(
    CategoryNotFoundError,
    category_not_found_handler
)
app.add_exception_handler(
    CategoryAlreadyExistsError,
    category_already_exists_handler
)
app.add_exception_handler(
    CategoryDeleteError,
    category_delete_error_handler
)

app.add_exception_handler(
    ProductNotFoundError,
    product_not_found_handler
)

app.add_exception_handler(
    CartItemNotFoundError,
    cart_item_not_found_handler
)

app.mount('/static', StaticFiles(directory=settings.static_dir), name='static')

app.include_router(auth_router)
app.include_router(session_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(cart_router)


@app.on_event('startup')
def on_startup():
    init_db()


@app.get('/')
def root():
    return {
        'message': 'Welcome to fastapi shop API',
        'docs': 'api/docs',
    }


@app.get('/health')
def health_check():
    return {'status': 'healthy'}



