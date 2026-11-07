import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TypedDict

import anyio
from asyncpg.exceptions import CannotConnectNowError
from fastapi import FastAPI
from sqlalchemy.exc import InterfaceError, OperationalError
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.backend.core.config import global_settings
from src.backend.dependencies.database import async_engine, AsyncSessionLocal, init_db
from src.backend.crud.message import create_message_dict_async
from src.backend.data.init_data import models_data

logger = logging.getLogger("uvicorn.error")

# On a one-click deploy the app and its database boot together, so the
# database may not accept connections yet. Retry briefly instead of exiting.
DB_STARTUP_TIMEOUT = 60
DB_RETRY_INTERVAL = 2
# Connection-level failures only (refused, DNS not ready, server starting up);
# anything else, like bad SQL or wrong credentials, fails fast.
DB_CONNECT_ERRORS = (OSError, OperationalError, InterfaceError, CannotConnectNowError)


async def init_db_with_retry() -> None:
    with anyio.move_on_after(DB_STARTUP_TIMEOUT) as scope:
        while True:
            try:
                await init_db()
                return
            except DB_CONNECT_ERRORS as exc:
                # Log the exception type only: its message can include the URL.
                logger.warning(
                    "Database not reachable yet (%s); retrying in %ss",
                    type(exc).__name__,
                    DB_RETRY_INTERVAL,
                )
                await anyio.sleep(DB_RETRY_INTERVAL)
    if scope.cancelled_caught:
        raise RuntimeError(
            f"Database not reachable after {DB_STARTUP_TIMEOUT}s; giving up"
        )


class AppState(TypedDict):
    db_session_factory: async_sessionmaker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[AppState]:
    # Zero-config deploys: surface generated docs credentials in the
    # deploy logs so one-click users can log in without setting env vars.
    if global_settings.docs_password_generated:
        print(
            "\n/docs credentials auto-generated"
            " (set USER_NAME / PASSWORD env vars to override):\n"
            f"  username: {global_settings.USER_NAME}\n"
            f"  password: {global_settings.PASSWORD}\n",
            flush=True,
        )

    # Increase thread pool for sync operations
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 100

    try:
        # Initialize database tables, waiting for a database that is still booting
        await init_db_with_retry()

        # Seed initial data
        async with AsyncSessionLocal() as db:
            for raw_data in models_data:
                await create_message_dict_async(db, raw_data)

        yield {"db_session_factory": AsyncSessionLocal}
    finally:
        # Dispose the engine on shutdown and on failed startup alike
        await async_engine.dispose()
