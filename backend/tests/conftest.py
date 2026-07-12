from pathlib import Path
import subprocess

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.main import app


ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env.test", override=True)


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=ROOT_DIR,
        check=True,
    )
    yield


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def registered_user(client):
    user = {
        'name': 'Eugen',
        'password': '12345678'
    }
    client.post(
        '/auth/register',
        json=user,
    )
    return user


@pytest.fixture
def authenticated_client(client, registered_user):
    client.post(
        '/auth/login',
        json=registered_user,
    )
    return client
