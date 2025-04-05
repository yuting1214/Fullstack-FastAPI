from contextlib import asynccontextmanager
from fastapi import FastAPI
import anyio
from typing import AsyncGenerator
from backend.fastapi.dependencies.database import init_db, AsyncSessionLocal
from backend.fastapi.crud.message import create_message_dict_async
from backend.data.init_data import models_data

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Increase thread pool size for better I/O performance
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 100  # Increased from default 40 to 100 threads

    # Initialize the database connection
    init_db()

    # Insert the initial data
    async with AsyncSessionLocal() as db:
        try:
            for raw_data in models_data:
                await create_message_dict_async(db, raw_data)
        finally:
            await db.close()

    yield