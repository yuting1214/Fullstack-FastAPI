from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import ProgrammingError

from src.backend.core import lifespan as startup


@pytest.mark.anyio
async def test_startup_waits_for_database(monkeypatch):
    # Refused twice (database still booting), then reachable.
    flaky_init = AsyncMock(side_effect=[ConnectionRefusedError(), OSError(), None])
    monkeypatch.setattr(startup, "init_db", flaky_init)
    monkeypatch.setattr(startup, "DB_RETRY_INTERVAL", 0)

    await startup.init_db_with_retry()
    assert flaky_init.await_count == 3


@pytest.mark.anyio
async def test_startup_gives_up_when_database_stays_down(monkeypatch):
    monkeypatch.setattr(
        startup, "init_db", AsyncMock(side_effect=ConnectionRefusedError())
    )
    monkeypatch.setattr(startup, "DB_STARTUP_TIMEOUT", 0.05)
    monkeypatch.setattr(startup, "DB_RETRY_INTERVAL", 0.01)

    with pytest.raises(RuntimeError, match="Database not reachable"):
        await startup.init_db_with_retry()


@pytest.mark.anyio
async def test_startup_does_not_retry_non_connection_errors(monkeypatch):
    broken_init = AsyncMock(
        side_effect=ProgrammingError("CREATE TABLE", {}, Exception())
    )
    monkeypatch.setattr(startup, "init_db", broken_init)

    with pytest.raises(ProgrammingError):
        await startup.init_db_with_retry()
    assert broken_init.await_count == 1


@pytest.mark.anyio
async def test_retry_log_omits_connection_details(monkeypatch, caplog):
    leaky_error = OSError("connect to postgresql://user:secret@host failed")
    monkeypatch.setattr(startup, "init_db", AsyncMock(side_effect=[leaky_error, None]))
    monkeypatch.setattr(startup, "DB_RETRY_INTERVAL", 0)

    await startup.init_db_with_retry()
    assert "Database not reachable yet" in caplog.text
    assert "secret" not in caplog.text
