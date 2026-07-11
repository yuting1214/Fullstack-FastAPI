from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.backend.core.config import global_settings as settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(settings.ASYNC_DB_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
