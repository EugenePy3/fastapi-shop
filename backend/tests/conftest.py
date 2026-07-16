from pathlib import Path
import subprocess

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.dependencies import get_db_manager
from app.core.db_manager import DBManager
from tests.api.auth_api import AuthApi

from tests.database import (
    test_engine,
    TestSessionLocal,
)

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


@pytest.fixture
def client():
    app.dependency_overrides[get_db_manager] = override_get_db_manager

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def auth_api(client):
    return AuthApi(client)


@pytest.fixture
def user_data():
    return {
        'name': 'Eugen',
        'password': '12345678',
    }


@pytest.fixture
def registered_user(auth_api, user_data):
    auth_api.register(**user_data)
    return user_data


@pytest.fixture
def authenticated_api(auth_api, registered_user):
    auth_api.login(**registered_user)
    return auth_api



