from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession)
from sqlalchemy.pool import StaticPool

from api.v1.auth_v1 import app
from app.core.database import Base, get_db


# build Testing DATABASE Connectors
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

connect_args = {}
if TEST_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_async_engine(TEST_DATABASE_URL,
                             echo=True,
                             connect_args=connect_args,
                             poolclass=StaticPool,)

Testing_sessionLocal = async_sessionmaker(bind=engine,
                                          class_=AsyncSession,
                                          expire_on_commit=False,
                                          )

# async build tables


@pytest.fixture(scope="session", autouse=True)
async def create_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Override Get DB
async def override_get_db():
    with await Testing_sessionLocal as Session:
        yield Session


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
