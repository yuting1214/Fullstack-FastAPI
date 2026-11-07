import pytest

from src.backend.core.config import ProdSettings


@pytest.fixture(autouse=True)
def isolate_db_env(monkeypatch):
    # Keep a developer's shell DB settings out of these tests (.env is
    # skipped per instance with _env_file=None).
    for name in (
        "DATABASE_URL",
        "DB_ENGINE",
        "DB_USERNAME",
        "DB_PASS",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
    ):
        monkeypatch.delenv(name, raising=False)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "database_url",
    [
        "postgresql://u:p@db.internal:5432/railway",
        "postgres://u:p@db.internal:5432/railway",
        "postgresql+psycopg://u:p@db.internal:5432/railway",
    ],
)
async def test_database_url_schemes_use_asyncpg(database_url):
    settings = ProdSettings(_env_file=None, DATABASE_URL=database_url)
    assert settings.ASYNC_DB_URL == "postgresql+asyncpg://u:p@db.internal:5432/railway"


@pytest.mark.anyio
async def test_individual_db_vars_still_work():
    settings = ProdSettings(
        _env_file=None,
        DB_ENGINE="postgresql",
        DB_USERNAME="u",
        DB_PASS="p",
        DB_HOST="db",
        DB_PORT="5432",
        DB_NAME="app",
    )
    assert settings.ASYNC_DB_URL == "postgresql+asyncpg://u:p@db:5432/app"


@pytest.mark.anyio
async def test_missing_database_settings_fail_with_clear_message():
    with pytest.raises(ValueError, match="ENV_MODE=prod needs a database"):
        ProdSettings(_env_file=None).ASYNC_DB_URL
