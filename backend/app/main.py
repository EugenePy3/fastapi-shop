from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.exceptions import AppError
from app.core.handlers import app_error_handler

from app.routes import (
    products_router,
    categories_router,
    cart_router,
    order_router,
    auth_router,
    session_router
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_exception_handler(
    AppError,
    app_error_handler,
)

app.mount('/static', StaticFiles(directory=settings.static_dir), name='static')

app.include_router(auth_router)
app.include_router(session_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(cart_router)
app.include_router(order_router)


@app.get('/')
def root():
    return {
        'message': 'Welcome to fastapi shop API',
        'docs': 'api/docs',
    }


@app.get('/health')
def health_check():
    return {'status': 'healthy'}
