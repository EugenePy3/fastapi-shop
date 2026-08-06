from decimal import Decimal
from pathlib import Path
import subprocess

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text, update

from tests.api.categories_api import CategoriesApi

from app.main import app
from app.dependencies import get_db_manager
from app.core.db_manager import DBManager

from tests.api.auth_api import AuthApi
from tests.api.cart_api import CartApi
from tests.api.orders_api import OrdersApi
from tests.api.products_api import ProductsApi

from tests.database import (
    test_engine,
    TestSessionLocal,
)

from app.models.user import User

# ============================================================
# Infrastructure
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

TABLES = """
order_items,
orders,
cart_items,
carts,
sessions,
products,
categories,
users
"""


@pytest.fixture(scope='session', autouse=True)
def apply_migrations():
    subprocess.run(
        ['alembic', 'upgrade', 'head'],
        cwd=ROOT_DIR,
        check=True,
    )
    yield


@pytest.fixture(autouse=True)
async def clean_db():
    async with test_engine.begin() as conn:
        await conn.execute(
            text(
                f'TRUNCATE TABLE {TABLES} RESTART IDENTITY CASCADE'
            )
        )

    yield


async def override_get_db_manager():
    async with DBManager(TestSessionLocal) as manager:
        yield manager


# ============================================================
# HTTP clients
# ============================================================


@pytest.fixture
def user_client():
    app.dependency_overrides[get_db_manager] = override_get_db_manager

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def admin_client():
    app.dependency_overrides[get_db_manager] = override_get_db_manager

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# ============================================================
# API wrappers
# ============================================================


@pytest.fixture
def auth_api(user_client):
    return AuthApi(user_client)


@pytest.fixture
def admin_auth_api(admin_client):
    return AuthApi(admin_client)


# ============================================================
# Test users
# ============================================================


@pytest.fixture
def user_data():
    return {
        'name': 'Eugen',
        'password': '12345678',
    }


@pytest.fixture
def admin_user_data():
    return {
        'name': 'Admin',
        'password': '12345678',
    }


# ============================================================
# Regular user
# ============================================================


@pytest.fixture
async def registered_user(auth_api, user_data):
    response = auth_api.register(**user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture
def authenticated_api(auth_api, registered_user):
    response = auth_api.login(**registered_user)
    assert response.status_code == 200
    return auth_api


# ============================================================
# Administrator
# ============================================================


@pytest.fixture
async def registered_admin(admin_auth_api, admin_user_data):
    response = admin_auth_api.register(**admin_user_data)
    assert response.status_code == 201

    async with TestSessionLocal() as session:
        await session.execute(
            update(User)
            .where(User.name == admin_user_data['name'])
            .values(is_admin=True)
        )
        await session.commit()

    return admin_user_data


@pytest.fixture
def admin_api(admin_auth_api, registered_admin):
    response = admin_auth_api.login(**registered_admin)
    assert response.status_code == 200
    return admin_auth_api


# ============================================================
# Domain API
# ============================================================

@pytest.fixture
def cart_api(authenticated_api):
    return CartApi(authenticated_api.client)


@pytest.fixture
def orders_api(authenticated_api):
    return OrdersApi(authenticated_api.client)


@pytest.fixture
def admin_cart_api(admin_api):
    return CartApi(admin_api.client)


@pytest.fixture
def admin_orders_api(admin_api):
    return OrdersApi(admin_api.client)


@pytest.fixture
def categories_api(admin_api):
    return CategoriesApi(admin_api.client)


@pytest.fixture
def products_api(admin_api):
    return ProductsApi(admin_api.client)


# ============================================================
# Domain entities
# ============================================================


@pytest.fixture
def category(categories_api):
    response = categories_api.create(
        name='Phones',
        slug='phones',
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def product(products_api, category):
    response = products_api.create(
        name='iPhone 17',
        description='Test product',
        price=1000,
        category_id=category['id'],
        image_url=None,
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def admin_cart_with_product(admin_cart_api, product):
    admin_cart_api.add(product['id'], quantity=1)


@pytest.fixture
def admin_order(admin_orders_api, admin_cart_with_product):
    response = admin_orders_api.create()
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def cart_with_product(cart_api, product):
    quantity = 3

    cart_api.add(product["id"], quantity=quantity)

    return {
        "product_id": product["id"],
        "product_name": product["name"],
        "product_price": Decimal(product["price"]),
        "quantity": quantity,
        "subtotal": Decimal(product["price"]) * quantity,
    }


@pytest.fixture
def order(orders_api, cart_with_product):
    response = orders_api.create()
    assert response.status_code == 201
    return response.json()
