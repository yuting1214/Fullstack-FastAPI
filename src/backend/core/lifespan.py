from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TypedDict

import anyio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.backend.dependencies.database import async_engine, AsyncSessionLocal, init_db
from src.backend.crud.message import create_message_dict_async
from src.backend.data.init_data import models_data


class AppState(TypedDict):
    db_session_factory: async_sessionmaker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[AppState]:
    # Increase thread pool for sync operations
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 100

    # Initialize database tables asynchronously
    await init_db()

    # Seed initial data
    async with AsyncSessionLocal() as db:
        for raw_data in models_data:
            await create_message_dict_async(db, raw_data)

    yield {"db_session_factory": AsyncSessionLocal}

    # Shutdown: dispose engine
    await async_engine.dispose()
