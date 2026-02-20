import pytest
from httpx import ASGITransport, AsyncClient
from src.backend.dependencies.database import init_db, async_engine, Base
from src.backend.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def setup_db():
    await init_db()
    yield
    # Clean up tables after each test
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
