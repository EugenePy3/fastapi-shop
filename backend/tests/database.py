import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

load_dotenv(
    os.path.join(ROOT_DIR, '.env.testing'),
    override=True,
)

DATABASE_URL = os.environ['DATABASE_URL']

test_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)
